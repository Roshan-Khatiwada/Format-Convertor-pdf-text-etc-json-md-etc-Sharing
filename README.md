# Format Converter - PDF to JSON

A pharmaceutical document converter that extracts structured data from PDF files and converts them into organized JSON format matching predefined pharmaceutical templates.

## Overview

This project is designed to convert pharmaceutical PDF documents (like drug product descriptions and compositions) into structured JSON files. It uses optical character recognition (OCR) and intelligent text parsing to extract specific fields and organize them according to pharmaceutical dossier standards.

### Features

- **PDF Parsing**: Extracts text content from PDF files using OCR
- **Structured Output**: Organizes data into pharmaceutical template formats
- **Smart Field Extraction**: Searches for specific keywords and validates matches against templates
- **Strict Matching**: Only returns data that matches the template format; returns empty for non-matching fields
- **Multi-section Support**: Handles multiple pharmaceutical sections (P1.1, P1.2, P1.3, P1.4)

### Supported Sections

- **P1.1**: Dosage form and characteristics
- **P1.2**: Accompanying reconstitution diluent
- **P1.3**: Type of container and closure system
- **P1.4**: Composition (summary and detailed formula)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Format-Convertor-pdf-text-etc-json-md-etc-Sharing
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:

```bash
pip install liteparse
```

## Usage

### Basic Usage

Run the script with a PDF file:

```bash
python format1.py "path/to/your/pdf/file.pdf"
```

### Example

```bash
python format1.py "P 1 Description and Composition.pdf"
```

### Default Behavior

If no PDF file is specified, the script looks for `P 1 Description and Composition.pdf` in the current directory:

```bash
python format1.py
```

## Output

The script creates an output directory `format1output/` containing subdirectories for each pharmaceutical section:

```
format1output/
├── P1.1 Dosage form and characteristics/
│   └── format.json
├── P1.2 Accompanying reconstitution diluent/
│   └── format.json
├── P1.3 Type of container and closure used for the dosage form/
│   └── format.json
└── P1.4 Composition/
    └── format.json
```

Each `format.json` contains:
- `section_code`: Unique identifier for the section
- `dossier_type`: Type of document (e.g., "product")
- `_instruction`: Guidelines for data extraction
- `components`: Extracted and structured data
- `source_pdf`: Path to the source PDF file

### JSON Output Example

```json
{
  "section_code": "p1.1",
  "dossier_type": "product",
  "_instruction": "Drug Product Description — dosage form and characteristics only...",
  "components": [
    {
      "section_code": "dosage_form_and_characteristics",
      "type": "table",
      "rows": [
        ["Product Name", "TACROMUS-1"],
        ["Description", "A white colour powder filled in capsule."],
        ["Label Claim", "Each hard gelatin capsule contains: Tacrolimus USP 1 mg"]
      ]
    }
  ],
  "source_pdf": "C:\\path\\to\\pdf\\file.pdf"
}
```

## File Structure

- `format1.py`: Main script for PDF parsing and conversion
- `requirements.txt`: Python dependencies
- `README.md`: This file
- `format1output/`: Output directory (created automatically)

## How It Works

1. **Parse PDF**: Reads PDF and extracts all text using LiteParse OCR library
2. **Organize Sections**: Groups text into sections (a, b, c, d, e) based on document structure
3. **Extract Fields**: Searches for specific pharmaceutical keywords in each section
4. **Match Templates**: Validates extracted data against predefined templates
5. **Generate JSON**: Creates structured JSON files with matched data only; empty fields for non-matches

## Key Functions

- `parse_pdf_to_components()`: Extracts text from PDF
- `extract_sections()`: Organizes text by sections
- `build_dosage_rows()`: Extracts dosage form data
- `build_reconstitution_text()`: Extracts reconstitution diluent information
- `build_container_closure_text()`: Extracts container/closure details
- `fill_template_components()`: Fills template with extracted data
- `write_split_outputs()`: Writes JSON output files

## Data Extraction Behavior

- **Matched Fields**: Returns extracted data
- **Non-Matched Fields**: Returns empty string or empty array
- **Fallback**: No default/fallback values; strict format matching only

## Requirements

### Python Packages

```
liteparse
```

### System Requirements

- Minimum 2GB RAM
- 500MB free disk space (for output and temp files)

## Troubleshooting

### PDF Not Found Error

```
FileNotFoundError: PDF input not found: <path>
```

**Solution**: Verify the PDF file path and ensure the file exists.

### Module Import Error

```
ModuleNotFoundError: No module named 'liteparse'
```

**Solution**: Install dependencies with `pip install -r requirements.txt`

### Empty Output

If output JSON files have empty fields:
- The PDF format may not match expected pharmaceutical template
- Check if required keywords are present in the PDF
- Verify OCR extracted text correctly

## Contributing

To add support for new pharmaceutical sections:

1. Add new template to `TEMPLATES` list in `format1.py`
2. Create extraction function following naming pattern: `build_<section_name>()`
3. Add logic to `fill_template_components()` to use the new function

## License

[Specify your license here]

## Author

Bibash Chamlagain

## Support

For issues or questions, please check the code comments or create an issue in the repository.

---

**Last Updated**: 2026-06-01
