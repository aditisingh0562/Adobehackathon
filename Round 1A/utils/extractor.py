import fitz  # PyMuPDF
import re
import spacy
from pathlib import Path
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Load multilingual spaCy model (works offline if pre-installed in Docker)
try:
    nlp = spacy.load("xx_ent_wiki_sm")
except Exception as e:
    print("[ERROR] Multilingual model not found. Please install xx_ent_wiki_sm")
    nlp = None

def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    all_blocks = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            line_text = ""
            max_size = 0
            y_pos = 1000
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        line_text += text + " "
                        max_size = max(max_size, span["size"])
                        y_pos = min(y_pos, span["bbox"][1])
            line_text = line_text.strip()
            if line_text:
                all_blocks.append({
                    "text": line_text,
                    "size": max_size,
                    "page": page_num,
                    "y": y_pos
                })
    return all_blocks

def classify_headings(blocks):
    outline = []
    page_max_titles = {}

    for block in blocks:
        page = block["page"]
        if page not in page_max_titles or block["size"] > page_max_titles[page]["size"]:
            page_max_titles[page] = block

    for block in blocks:
        text = block["text"]
        size = block["size"]
        page = block["page"]

        if block == page_max_titles[page]:
            level = "H1"
        elif re.match(r"^[•\-–●▪]", text.strip()):
            level = "H3"
        elif len(text.split()) <= 6 and size >= 10:
            level = "H2"
        else:
            continue

        outline.append({
            "level": level,
            "text": text.strip(),
            "page": page
        })

    return outline

def extract_title(blocks):
    if not blocks:
        return ""
    top_blocks = [b for b in blocks if b["page"] == 0]
    return max(top_blocks, key=lambda b: b["size"])["text"] if top_blocks else ""

def extract_links(blocks):
    pattern = r'https?://[^\s\)\],"]+'
    for block in blocks:
        match = re.search(pattern, block["text"])
        if match:
            return match.group(0)
    return ""

def extract_dates(blocks):
    pattern = r'(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}|(?:\d{1,2}(st|nd|rd|th)?\s)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[ ,]*(\d{2,4}))'
    dates = []
    for block in blocks:
        matches = re.findall(pattern, block["text"])
        for match in matches:
            full = match[0]
            if full not in dates:
                dates.append(full)
    return dates

def extract_registration_info(blocks):
    keywords = ['register', 'registration', 'deadline', 'inscription', 'fecha límite', 'registrarse']
    lines = [b["text"] for b in blocks if any(k in b["text"].lower() for k in keywords)]
    return lines[:3] if lines else []

def extract_summary(blocks):
    full_text = "\n".join([b["text"] for b in blocks])
    try:
        parser = PlaintextParser.from_string(full_text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, 5)
        return [str(sentence) for sentence in summary]
    except Exception:
        return full_text.split("\n")[:5]

def extract_all(pdf_path):
    blocks = extract_text_blocks(pdf_path)
    return {
        "title": extract_title(blocks),
        "outline": classify_headings(blocks),
        "summary": extract_summary(blocks),
        "registration_info": extract_registration_info(blocks),
        "link": extract_links(blocks),
        "dates": extract_dates(blocks)
    }
