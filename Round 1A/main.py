import json
from pathlib import Path
from utils.extractor import extract_all

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "sample.json"

pdf_files = list(INPUT_DIR.glob("*.pdf"))
if not pdf_files:
    raise FileNotFoundError("No PDF file found in input directory.")

pdf_path = pdf_files[0]
print(f"Processing {pdf_path.name}...")

result = extract_all(pdf_path)

OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("✅ Extraction complete. Output written to output/sample.json")
