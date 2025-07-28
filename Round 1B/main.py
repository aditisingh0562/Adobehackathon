import json
import os
from extractor import extract_from_pdf

with open("input/input.json", "r") as f:
    config = json.load(f)

documents = config.get("documents", [])

all_outputs = []

for doc in documents:
    filename = doc["filename"]
    filepath = os.path.join("input", filename)
    result = extract_from_pdf(filepath)
    result["source_file"] = filename
    all_outputs.append(result)

# Save final output
with open("output/sample.json", "w") as f:
    json.dump(all_outputs, f, indent=2)
