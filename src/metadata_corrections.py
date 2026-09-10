"""Corrections approuvées de métadonnées, sans imputation ni changement de schéma.

Depuis n'importe quel répertoire : python -B chemin/vers/src/metadata_corrections.py
Les contrôles et la préparation CSV/XLSX/journal précèdent toute sauvegarde.
Une réexécution valide les mêmes cibles mais ne duplique ni notes ni journal.
"""
import copy
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tempfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data/final/dataset_maitre_trends_tourisme_afrique.csv"
LOG = ROOT / "reports/exports/metadata_corrections_log.csv"
LOG_FIELDS = ["correction_id", "destination", "year", "origin_name",
              "column_changed", "old_value", "new_value", "reason"]
SCAND_NOTE = ("Groupe régional publié par la source ; composition exacte du groupe à vérifier. "
              "Ne pas ventiler en pays et ne pas fusionner automatiquement avec d'autres agrégats scandinaves.")
UNO_NOTE = ("Catégorie institutionnelle publiée dans le Top 30 ; ne pas interpréter comme un pays. "
            "Définition statistique exacte à vérifier dans la source originale.")
MISSING_NOTE = ("Valeur absente du dataset harmonisé ; cause de l'absence non vérifiée dans "
                "la source originale. Ne pas interpréter comme zéro.")
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def require(condition, message):
    # Ne pas désactiver les contrôles en lançant Python avec -O.
    if not condition:
        raise AssertionError(message)


def decode_csv(data):
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline=""))
    rows = list(reader)
    require(reader.fieldnames and all(None not in r and None not in r.values() for r in rows),
            "CSV mal formé")
    return reader.fieldnames, rows


def encode_csv(fields, rows, original=b""):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields,
                            lineterminator="\r\n" if b"\r\n" in original else "\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8-sig" if original.startswith(b"\xef\xbb\xbf") else "utf-8")


def value_hash(rows):
    # Chaînes sources exactes : contrôle plus strict qu'une somme de flottants.
    return hashlib.sha256(json.dumps([r["value"] for r in rows]).encode()).hexdigest()


def correct(rows):
    require(len(rows) == 1080, "1080 lignes attendues")
    result, changes = copy.deepcopy(rows), []
    scand = [i for i, r in enumerate(rows) if r["destination"] == "Tunisie" and r["origin_name"] == "Scandinaves"]
    uno = [i for i, r in enumerate(rows) if r["destination"] == "Kenya" and r["origin_name"] == "United Nations Organization" and r["year"] == "2022"]
    missing = [i for i, r in enumerate(rows) if r["destination"] == "Tunisie" and r["dataset_layer"] == "provenance" and r["value"] == "" and r["year"] in ("2017", "2018")]
    require(len(scand) == 7 and {rows[i]["year"] for i in scand} == {str(y) for y in range(2017, 2024)}, "Cible Scandinaves inattendue")
    require(len(uno) == 1, "Une ligne ONU attendue")
    require(len(missing) == 60, "60 absences tunisiennes attendues")
    origins = [{rows[i]["origin_name"] for i in missing if rows[i]["year"] == y} for y in ("2017", "2018")]
    require(len(origins[0]) == 30 and origins[0] == origins[1], "30 mêmes origines attendues sur deux années")
    specs = [("TUN_SCANDINAVES", scand, {"granularity": ("country", "regional_aggregate"), "quality_flag": ("exact_country", "exact_aggregate")}, SCAND_NOTE),
             ("KEN_UNO", uno, {"granularity": ("country", "institutional_category")}, UNO_NOTE),
             ("TUN_MISSING", missing, {"quality_flag": ("exact_country", "missing_unverified")}, MISSING_NOTE)]
    for cid, indexes, fields, note in specs:
        for i in indexes:
            r = result[i]
            require(r["dataset_layer"] == "provenance", "Couche inattendue")
            if cid == "KEN_UNO":
                require(r["quality_flag"] == "exact_top30", "Drapeau ONU inattendu")
            if cid == "TUN_MISSING":
                require(r["granularity"] == "country", "Granularité absence inattendue")
            updates = {}
            for column, (old, new) in fields.items():
                require(r[column] in (old, new), f"État inattendu : {cid}, {column}")
                updates[column] = new
            require(r["notes"].count(note) <= 1, "Note déjà dupliquée")
            updates["notes"] = r["notes"] if note in r["notes"] else r["notes"] + (" " if r["notes"] else "") + note
            for column, new in updates.items():
                if r[column] != new:
                    changes.append(dict(correction_id=cid, destination=r["destination"], year=r["year"],
                                        origin_name=r["origin_name"], column_changed=column,
                                        old_value=r[column], new_value=new, reason=note))
                    r[column] = new
    require(len(result) == len(rows) == 1080, "Ajout/suppression de ligne")
    require(value_hash(rows) == value_hash(result), "Valeurs numériques modifiées")
    allowed = {(i, c) for _, indexes, fields, _ in specs for i in indexes for c in (*fields, "notes")}
    for i, (old, new) in enumerate(zip(rows, result)):
        for column in old:
            require(old[column] == new[column] or (i, column) in allowed, f"Modification interdite : {i}, {column}")
    for _, indexes, fields, note in specs:
        for i in indexes:
            require(all(result[i][c] == pair[1] for c, pair in fields.items()), "Correction incomplète")
            require(note in result[i]["notes"], "Note absente")
    require(all(result[i]["value"] == "" for i in missing), "Imputation interdite")
    return result, changes


def prepare_xlsx(data, before, after):
    """Remplace uniquement des cellules textuelles dans le ZIP, sans reconstruire Excel.

    Les feuilles sont repérées par leurs relations ; toutes les autres entrées
    (styles, tables, KPI, nombres, etc.) sont conservées octet pour octet.
    Toute incompatibilité bloque l'opération avant la sauvegarde.
    """
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = {info.filename: archive.read(info.filename) for info in archive.infolist()}
        rels = {r.attrib["Id"]: r.attrib["Target"] for r in ET.fromstring(entries["xl/_rels/workbook.xml.rels"])}
        sheets = {}
        for s in ET.fromstring(entries["xl/workbook.xml"]).find(NS + "sheets"):
            target = rels[s.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]]
            sheets[s.attrib["name"]] = target.lstrip("/") if target.startswith("/") else "xl/" + target
        shared = ["".join(s.itertext()) for s in ET.fromstring(entries["xl/sharedStrings.xml"])] if "xl/sharedStrings.xml" in entries else []
        patches = {}

        def cells(sheet):
            return {c.attrib["r"]: c for c in ET.fromstring(entries[sheets[sheet]]).iter(NS + "c")}

        def text(cell):
            if cell is None:
                return ""
            if cell.attrib.get("t") == "inlineStr":
                return "".join(cell.find(NS + "is").itertext())
            v = cell.find(NS + "v")
            value = v.text or "" if v is not None else ""
            return shared[int(value)] if cell.attrib.get("t") == "s" else value

        def patch(sheet, ref, new):
            old = cells(sheet)[ref]
            require(old.attrib.get("t") in ("str", "s", "inlineStr") and old.find(NS + "f") is None, "Cellule XLSX non textuelle : " + ref)
            if text(old) != new:
                patches.setdefault(sheets[sheet], {})[ref] = new

        master = cells("Dataset_maitre")
        fields = list(before[0])
        require([text(master.get(f"{chr(65+j)}1")) for j in range(len(fields))] == fields, "Schéma XLSX différent")
        require(max(int(re.search(r"\d+", ref)[0]) for ref in master) == 1081, "Nombre de lignes XLSX différent")
        for i, (old, new) in enumerate(zip(before, after), 2):
            for j, field in enumerate(fields):
                ref = f"{chr(65+j)}{i}"
                current = text(master.get(ref))
                if field in ("value", "year"):
                    from decimal import Decimal
                    require((current == old[field] == "") or (current != "" and old[field] != "" and Decimal(current) == Decimal(old[field])), f"Nombre XLSX différent : {ref}")
                else:
                    require(current in (old[field], new[field]), f"Métadonnée XLSX divergente : {ref}")
                    if current != new[field]:
                        patch("Dataset_maitre", ref, new[field])
        for ref, c in cells("Audit_maitre").items():
            if ref.startswith("A") and text(c) in {r["destination"] for r in after}:
                flags = sorted({r["quality_flag"] for r in after if r["destination"] == text(c) and r["dataset_layer"] == "provenance"})
                patch("Audit_maitre", "K" + ref[1:], ", ".join(flags))
        rules = {
            "granularity": "destination_total, country, regional_aggregate, aggregate_total, diaspora, institutional_category. Catégories institutionnelles et agrégées distinctes des pays ; Reunion Island reste country comme marché distinct, sans fusion avec France.",
            "quality_flag": "missing_unverified : valeur absente du dataset harmonisé, cause non vérifiée dans la source originale ; ne pas assimiler à missing_in_source ni à zéro. Les autres drapeaux restent conservés.",
            "source_name": "Producteur/source conservé. Égypte–États-Unis : User-provided source file inchangé ; attribution CAPMAS historique non vérifiable avec les pièces présentes dans le dépôt.",
        }
        for ref, c in cells("Dictionnaire").items():
            if ref.startswith("A") and text(c) in rules:
                patch("Dictionnaire", "C" + ref[1:], rules[text(c)])
        additions = {
            "B4": " Les 60 absences tunisiennes 2017–2018 portent missing_unverified : cause dans la source non vérifiée.",
            "B6": " Attribution CAPMAS historique : liaison aux dix observations USA non vérifiable avec les pièces du dépôt ; source_name reste User-provided source file.",
            "B7": " Kenya : ONU reste dans le Top 30, en institutional_category. Maurice : Reunion Island reste country, marché distinct sans fusion avec France.",
            "B8": " Tunisie : les 7 lignes Scandinaves deviennent regional_aggregate / exact_aggregate ; composition exacte à vérifier, sans ventilation ni fusion automatique.",
        }
        for ref, addition in additions.items():
            current = text(cells("Methodologie")[ref])
            patch("Methodologie", ref, current if addition in current else current + addition)
        if not patches:
            return data
        # Remplacement local : pas de sérialisation générale de l'arbre XML.
        output = dict(entries)
        for path, changes in patches.items():
            xml = entries[path].decode("utf-8")
            for ref, new in changes.items():
                pattern = rf'<x:c\b[^>]*\br="{ref}"[^>]*>.*?</x:c>'
                def replace(match):
                    opening = match[0].split(">", 1)[0]
                    opening = re.sub(r'\s+t="[^"]*"', '', opening)
                    return opening + ' t="inlineStr"><x:is><x:t xml:space="preserve">' + escape(new) + '</x:t></x:is></x:c>'
                xml, count = re.subn(pattern, replace, xml, flags=re.S)
                require(count == 1, "Cellule XML introuvable ou ambiguë : " + ref)
            old_cells = {c.attrib["r"]: c for c in ET.fromstring(entries[path]).iter(NS + "c")}
            new_cells = {c.attrib["r"]: c for c in ET.fromstring(xml).iter(NS + "c")}
            require(old_cells.keys() == new_cells.keys(), "Structure XLSX modifiée")
            for ref in old_cells:
                if ref not in changes:
                    require(ET.tostring(old_cells[ref]) == ET.tostring(new_cells[ref]), "Cellule non ciblée modifiée")
                else:
                    require(text(new_cells[ref]) == changes[ref], "Échec correction XML")
            output[path] = xml.encode("utf-8")
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w") as target:
            target.comment = archive.comment
            for info in archive.infolist():
                target.writestr(info, output[info.filename])
        return stream.getvalue()


def save_validated(payloads):
    """Prépare les fichiers, puis remplace atomiquement chacun ; restaure en cas d'erreur.

    Les remplacements multi-fichiers ne constituent pas une transaction résistante
    à une coupure système ; relancer le script permet de vérifier leur cohérence.
    """
    originals = {p: p.read_bytes() if p.exists() else None for p in payloads}
    staged, replaced = {}, []
    try:
        for path, data in payloads.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
                staged[path] = Path(handle.name)
                handle.write(data)
        for path, temporary in staged.items():
            os.replace(temporary, path)
            replaced.append(path)
    except Exception:
        for path in reversed(replaced):
            if originals[path] is None:
                path.unlink()
            else:
                path.write_bytes(originals[path])
        raise
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)


def main():
    original = MASTER.read_bytes()
    fields, before = decode_csv(original)
    after, changes = correct(before)
    csv_data = encode_csv(fields, after, original) if changes else original
    require(decode_csv(csv_data)[1] == after, "Échec validation sérialisation CSV")
    xlsx = MASTER.with_suffix(".xlsx")
    xlsx_original = xlsx.read_bytes()
    xlsx_data = prepare_xlsx(xlsx_original, before, after)
    log_rows = []
    if LOG.exists():
        log_fields, log_rows = decode_csv(LOG.read_bytes())
        require(log_fields == LOG_FIELDS, "Schéma journal inattendu")
    for change in changes:
        if change not in log_rows:
            log_rows.append(change)
    payloads = {}
    if log_rows and (not LOG.exists() or decode_csv(LOG.read_bytes())[1] != log_rows):
        payloads[LOG] = encode_csv(LOG_FIELDS, log_rows)
    if xlsx_data != xlsx_original:
        payloads[xlsx] = xlsx_data
    if csv_data != original:
        payloads[MASTER] = csv_data
    save_validated(payloads)
    print(json.dumps({"lignes_avant": len(before), "lignes_apres": len(after),
                      "hash_value": value_hash(after), "cellules_modifiees": len(changes),
                      "lignes_modifiees": len({(c['destination'], c['year'], c['origin_name']) for c in changes}),
                      "cellules_par_correction": {cid: sum(c['correction_id'] == cid for c in changes) for cid in ('TUN_SCANDINAVES', 'KEN_UNO', 'TUN_MISSING')},
                      "granularity": sorted({r['granularity'] for r in after}),
                      "quality_flag": sorted({r['quality_flag'] for r in after}),
                      "fichiers_enregistres": [str(p.relative_to(ROOT)) for p in payloads]}, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
