from liteparse import LiteParse
from pathlib import Path
import json


def parse_pdf_to_json(pdf_path):
    parser = LiteParse()
    result = parser.parse(pdf_path)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    pdf_name = Path(pdf_path).stem

    output_file = output_dir / f"{pdf_name}-output.json"

    data = {
        "section_code": pdf_name,
        "dossier_type": "product",
        "_instruction": f"Generate {pdf_name} from SECTION DATA",
        "components": []
    }

    sn = 1

    for page in result.pages:
        page_text = []

        for item in page.text_items:
            text = getattr(item, "text", "").strip()

            if text:
                page_text.append(text)

                data["components"].append(
                    {
                        "type": "text",
                        "section_title": None,
                        "page": page.page_num,
                        "sn": sn,
                        "content": text
                    }
                )
                sn += 1

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved: {output_file}")


if __name__ == "__main__":
    parse_pdf_to_json("P2.2.1 Drug Substance.pdf")