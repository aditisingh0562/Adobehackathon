import fitz  # PyMuPDF

def extract_text_from_pdf(path):
    text_blocks = []
    doc = fitz.open(path)
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")
        for b in blocks:
            text = b[4].strip()
            if text:
                text_blocks.append((page_num, text))
    return text_blocks
