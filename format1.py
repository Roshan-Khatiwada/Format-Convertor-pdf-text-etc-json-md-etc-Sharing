from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from liteparse import LiteParse

FORMAT1_OUTPUT_ROOT = Path("format1output")

#philipins data format to myanmar format
# This script OCRs the provided PDF, converts it to JSON,
# and writes split outputs into format1output matching the
# field and section structure used by the format1 templates.
#..end..

TEMPLATES: list[tuple[str, dict[str, Any]]] = [
    (
        "P1.1 Dosage form and characteristics",
        {
            "section_code": "p1.1",
            "dossier_type": "product",
            "_instruction": "Drug Product Description — dosage form and characteristics only. Order: header, description, dosage_form.",
            "components": [
                {
                    "section_code": "P 1",
                    "type": "section_header",
                    "title": "DESCRIPTION AND COMPOSITION",
                    "section_number": "P 1",
                    "section_title": "DESCRIPTION AND COMPOSITION",
                },
                {
                    "section_code": "P 1.1",
                    "type": "section_header",
                    "title": "Drug Product Description",
                    "section_number": "P 1.1",
                    "section_title": "Drug Product Description",
                },
                {
                    "section_code": "dosage_form_and_characteristics",
                    "type": "table",
                    "title": "Dosage form and characteristics",
                    "prompt": "Extract dosage form and characteristics into a 2-column table (Field, Value). Typical fields: Product Name, Generic Name, CAS Register No., Description/Appearance, Label Claim, Shelf Life, Storage Condition. Use dossier text exactly; correct obvious OCR spacing/punctuation only.",
                    "columns": ["Field", "Value"],
                    "example": [
                        ["Product Name", "TACROMUS-1"],
                        ["Generic Name", "Tacrolimus Capsules USP 1 mg"],
                        ["CAS Register No.", "104987-11-3"],
                        ["Description", "A white colour powder filled in Green/Ivory colour '3' size hard gelatin capsule."],
                        ["Label Claim", "Each hard gelatin capsule contains: Tacrolimus USP 1 mg; Excipients q.s; Approved colour used in hard gelatin capsule shell."],
                        ["Shelf Life", "24 months"],
                        ["Storage Condition", "Store below 30°C. Protect from light. Keep the medicine out of reach of children."],
                    ],
                    "section_number": "a",
                    "section_title": "Dosage form and characteristics",
                },
            ],
        },
    ),
    (
        "P1.2  Accompanying reconstitution diluent",
        {
            "section_code": "p1.2",
            "dossier_type": "product",
            "_instruction": "Drug Product Description — reconstitution diluent only. If none, state clearly (e.g. Not applicable).",
            "components": [
                {
                    "section_code": "P 1",
                    "type": "section_header",
                    "title": "DESCRIPTION AND COMPOSITION",
                    "section_number": "P 1",
                    "section_title": "DESCRIPTION AND COMPOSITION",
                },
                {
                    "section_code": "P 1.2",
                    "type": "section_header",
                    "title": "Drug Product Description",
                    "section_number": "P 1.2",
                    "section_title": "Drug Product Description",
                },
                {
                    "section_code": "accompanying_reconstitution_diluents",
                    "type": "text",
                    "title": "Accompanying reconstitution diluent(s) if any",
                    "prompt": "State whether any accompanying reconstitution diluent(s) are supplied with the product. If none, write 'Not applicable.' (or dossier equivalent). One short sentence only.",
                    "example": "Not applicable.",
                    "section_number": "a",
                    "section_title": "Accompanying reconstitution diluent(s) if any",
                },
            ],
        },
    ),
    (
        "P1.3 Type of container and closure used for the dosage form",
        {
            "section_code": "p1.3",
            "dossier_type": "product",
            "_instruction": "Drug Product Description — container and closure for dosage form and reconstitution diluent (if applicable).",
            "components": [
                {
                    "section_code": "P 1",
                    "type": "section_header",
                    "title": "DESCRIPTION AND COMPOSITION",
                    "section_number": "P 1",
                    "section_title": "DESCRIPTION AND COMPOSITION",
                },
                {
                    "section_code": "P 1.3",
                    "type": "section_header",
                    "title": "Drug Product Description",
                    "section_number": "P 1.3",
                    "section_title": "Drug Product Description",
                },
                {
                    "section_code": "container_closure_system",
                    "type": "text",
                    "title": "Type of container and closure used for the dosage form and reconstitution diluent, if applicable",
                    "prompt": "Describe the immediate container-closure system and pack configuration exactly as per dossier (e.g., Alu/Alu strip, count per strip, strips per carton, pack insert). Do not include composition or stability data.",
                    "example": "10 capsules packed in an Alu/Alu strip. Such 3 strips packed in a carton with pack insert.",
                    "section_number": "a",
                    "section_title": "Type of container and closure used for the dosage form and reconstitution diluent, if applicable",
                },
            ],
        },
    ),
    (
        "P1.4 Composition",
        {
            "section_code": "p1.4",
            "dossier_type": "product",
            "_instruction": "Drug Product Composition — name, quantity (metric), function, quality. Table g: category_header + sub_tests grouping mandatory.",
            "components": [
                {
                    "section_code": "P 1",
                    "type": "section_header",
                    "title": "DESCRIPTION AND COMPOSITION",
                    "section_number": "P 1",
                    "section_title": "DESCRIPTION AND COMPOSITION",
                },
                {
                    "section_code": "P 1.4",
                    "type": "section_header",
                    "title": "Drug Product Composition",
                    "section_number": "P 1.4",
                    "section_title": "Drug Product Composition",
                },
                {
                    "section_code": "composition_summary",
                    "type": "table",
                    "table_mode": "grid",
                    "columns": ["Label", "Value"],
                    "title": "Composition summary",
                    "prompt": "Short composition summary (Label/Value): product name, 'Each ... contains' statement, API strength, excipients q.s. No full batch formula here.",
                    "example": [
                        ["Product Name", "TACROMUS-1"],
                        ["Each Hard Gelatin capsule contains", ""],
                        ["Tacrolimus USP", "1 mg"],
                        ["Excipients", "q.s."],
                    ],
                    "section_number": "a",
                    "section_title": "Composition summary",
                },
                {
                    "section_code": "unit_formula",
                    "type": "table",
                    "columns": [
                        "S.No",
                        "Ingredients",
                        "Reference",
                        "Label Claim",
                        "Overages",
                        "Quantity per Batch (kg)",
                        "Quantity per Cap (mg)",
                        "Function",
                    ],
                    "title": "Name and quantity stated in metric weight or measures, function and quality",
                    "prompt": "Full qualitative and quantitative composition table. One row per ingredient; include totals/footer rows if present. Preserve pharmacopoeia references (USP, BP, IHS) and overage percentages exactly.",
                    "section_number": "b",
                    "section_title": "Name and quantity stated in metric weight or measures, function and quality",
                },
                {
                    "section_code": "abbreviations",
                    "type": "text",
                    "title": "Abbreviations",
                    "prompt": "List abbreviations used in the composition section (e.g., USP, BP, IHS, q.s., NMT, NLT) with expansions as stated in the dossier.",
                    "section_number": "c",
                    "section_title": "Abbreviations",
                },
            ],
        },
    ),
]


def parse_pdf_to_components(pdf_path: Path) -> list[dict[str, Any]]:
    parser = LiteParse()
    result = parser.parse(pdf_path)

    components: list[dict[str, Any]] = []
    sn = 1

    for page in result.pages:
        for item in page.text_items:
            text = getattr(item, "text", "").strip()
            if not text:
                continue

            components.append(
                {
                    "type": "text",
                    "section_title": None,
                    "page": page.page_num,
                    "sn": sn,
                    "content": text,
                }
            )
            sn += 1

    return components


def extract_sections(components: list[dict[str, Any]]) -> dict[str, list[str]]:
    lines = [item["content"] for item in components]
    sections = {"a": [], "b": [], "c": [], "d": [], "e": [], "rest": []}
    current = "rest"

    for line in lines:
        trimmed = line.strip()
        lower = trimmed.lower()

        if lower.startswith("a.") or lower == "a":
            current = "a"
            remainder = trimmed[2:].strip()
            if remainder:
                sections[current].append(remainder)
            continue
        if lower.startswith("b.") or lower == "b":
            current = "b"
            remainder = trimmed[2:].strip()
            if remainder:
                sections[current].append(remainder)
            continue
        if lower.startswith("c.") or lower == "c":
            current = "c"
            remainder = trimmed[2:].strip()
            if remainder:
                sections[current].append(remainder)
            continue
        if lower.startswith("d.") or lower == "d":
            current = "d"
            remainder = trimmed[2:].strip()
            if remainder:
                sections[current].append(remainder)
            continue
        if lower.startswith("e.") or lower == "e":
            current = "e"
            remainder = trimmed[2:].strip()
            if remainder:
                sections[current].append(remainder)
            continue

        sections[current].append(trimmed)

    return sections


def join_lines(lines: list[str]) -> str:
    return "\n".join(line for line in lines if line)


def find_line(lines: list[str], prefixes: list[str]) -> str:
    for line in lines:
        low = line.lower()
        for prefix in prefixes:
            if low.startswith(prefix.lower()):
                return line
    return ""


def build_dosage_rows(sections: dict[str, list[str]]) -> list[list[str]]:
    lines = sections["b"] + sections["c"]
    rows: list[list[str]] = []

    product_name = find_line(lines, ["product name:"])
    if product_name:
        rows.append(["Product Name", product_name.split(":", 1)[1].strip()])

    description = find_line(lines, ["description", "light yellow", "tablet", "capsule"])
    if description:
        rows.append(["Description", description])

    label_claim = find_line(lines, ["each", "each film coated tablet contains", "each hard gelatin capsule contains"])
    if label_claim:
        rows.append(["Label Claim", label_claim])

    storage = find_line(lines, ["store", "storage"])
    if storage:
        rows.append(["Storage Condition", storage])

    return rows


def build_reconstitution_text(sections: dict[str, list[str]]) -> str:
    all_lines = sections["a"] + sections["b"] + sections["c"] + sections["d"] + sections["e"]
    diluent_lines = [line for line in all_lines if "diluent" in line.lower() or "reconstitution" in line.lower()]
    if diluent_lines:
        return join_lines(diluent_lines)
    return ""


def build_container_closure_text(sections: dict[str, list[str]]) -> str:
    package_lines = [line for line in sections["d"] if any(term in line.lower() for term in ["pack", "carton", "insert", "container", "closure", "strip", "blister"])]
    if package_lines:
        return join_lines(package_lines)
    return ""


def fill_template_components(template_components: list[dict[str, Any]], sections: dict[str, list[str]]) -> list[dict[str, Any]]:
    filled: list[dict[str, Any]] = []

    for component in template_components:
        comp = dict(component)
        code = comp.get("section_code", "")

        if code == "dosage_form_and_characteristics":
            comp["rows"] = build_dosage_rows(sections)
        elif code == "accompanying_reconstitution_diluents":
            comp["content"] = build_reconstitution_text(sections)
        elif code == "container_closure_system":
            comp["content"] = build_container_closure_text(sections)

        filled.append(comp)

    return filled


def write_split_outputs(pdf_path: Path, components: list[dict[str, Any]]) -> None:
    sections = extract_sections(components)
    FORMAT1_OUTPUT_ROOT.mkdir(exist_ok=True)

    for folder_name, template in TEMPLATES:
        destination = FORMAT1_OUTPUT_ROOT / folder_name
        destination.mkdir(parents=True, exist_ok=True)

        output_data = {
            "section_code": template["section_code"],
            "dossier_type": template["dossier_type"],
            "_instruction": template["_instruction"],
            "components": fill_template_components(template["components"], sections),
            "source_pdf": str(pdf_path.resolve()),
        }

        output_file = destination / "format.json"
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print(f"Saved: {output_file}")


def main() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("P 1 Description and Composition.pdf")
    if not input_path.exists():
        raise FileNotFoundError(f"PDF input not found: {input_path}")

    print(f"Parsing PDF: {input_path}")
    components = parse_pdf_to_components(input_path)
    write_split_outputs(input_path, components)


if __name__ == "__main__":
    main()
