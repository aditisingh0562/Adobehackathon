import fitz  # PyMuPDF
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
# extractor.py

def extract_from_pdf(pdf_path):
    print(f"Processing PDF: {pdf_path}")
    # Dummy logic for now
    return {
        "title": "Sample Title",
        "summary": "This is a summary.",
        "outline": [],
        "dates": [],
        "link": [],
        "registration_info": []
    }

def extract_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    pages_text = [page.get_text() for page in doc]
    return pages_text

def extract_title(pages_text):
    for text in pages_text:
        lines = text.strip().split('\n')
        if lines:
            title_candidate = lines[0].strip()
            if len(title_candidate.split()) > 2:
                return title_candidate
    return "Untitled Document"

def classify_headings(pages_text):
    outline = []
    for page_num, text in enumerate(pages_text):
        lines = text.strip().split('\n')
        h1_found = False
        for line in lines:
            clean_line = line.strip()
            if not clean_line:
                continue
            if not h1_found and len(clean_line.split()) > 3:
                outline.append({"level": "H1", "text": clean_line, "page": page_num + 1})
                h1_found = True
            elif clean_line.isupper() and len(clean_line.split()) <= 5:
                outline.append({"level": "H2", "text": clean_line, "page": page_num + 1})
            elif len(clean_line.split()) <= 7:
                outline.append({"level": "H3", "text": clean_line, "page": page_num + 1})
    return outline

def generate_summary(text, sentence_count=3):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentence_count)
        return " ".join(str(sentence) for sentence in summary)
    except Exception as e:
        print(f"Summary generation failed: {e}")
        return text[:500]  # fallback: first 500 chars

def extract_links(pages_text):
    links = []
    for text in pages_text:
        found = re.findall(r'(https?://\S+)', text)
        links.extend(found)
    return list(set(links))

def extract_dates(pages_text):
    date_pattern = r'\b(?:\d{1,2}[-/th|st|nd|rd\s]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*[-/\s]*\d{2,4}\b|\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b'
    dates = []
    for text in pages_text:
        found = re.findall(date_pattern, text, re.IGNORECASE)
        dates.extend(found)
    return list(set(dates))

def extract_registration_info(pages_text):
    keywords = ["register", "registration", "sign up", "apply"]
    found_lines = []
    for text in pages_text:
        lines = text.split('\n')
        for line in lines:
            for kw in keywords:
                if kw in line.lower():
                    found_lines.append(line.strip())
    return list(set(found_lines))

def extract_all(pdf_path):
    pages_text = extract_text_by_page(pdf_path)
    full_text = "\n".join(pages_text)

    return {
        "title": extract_title(pages_text),
        "outline": classify_headings(pages_text),
        "summary": generate_summary(full_text),
        "dates": extract_dates(pages_text),
        "link": extract_links(pages_text),
        "registration_info": extract_registration_info(pages_text),
    }

