import os
from utils.pdf_utils import extract_text_from_pdf
from fuzzywuzzy import fuzz

def search_query_in_pdfs(input_dir, query, threshold=80):
    results = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            blocks = extract_text_from_pdf(pdf_path)
            for page_num, text in blocks:
                score = fuzz.partial_ratio(query.lower(), text.lower())
                if score >= threshold:
                    results.append({
                        "file": filename,
                        "page": page_num,
                        "score": score,
                        "text": text
                    })
    return results
