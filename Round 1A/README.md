# Challenge 1a: PDF Processing Solution

## Overview

This repository contains the solution for **Challenge 1a** of the **Adobe India Hackathon 2025**. The task is to extract structured data from PDF documents including headings (H1–H3), title, summary, dates, links, and registration information. The solution is containerized using Docker, runs completely offline, and follows all challenge constraints.

## Official Challenge Guidelines

### Submission Requirements

| Requirement                 | Status        |
|----------------------------|---------------|
| GitHub Project             | Complete      |
| Dockerfile                 | Present       |
| README.md Documentation    | Included      |
| JSON Schema Compliance     | Implemented   |

## Build Command

```bash
docker build --platform linux/amd64 -t pdf_extractor.uniqueid .
```

## Run Command

```bash
docker run --rm -v $(pwd)/sample_dataset/pdfs:/app/input:ro -v $(pwd)/sample_dataset/outputs:/app/output --network none pdf_extractor.uniqueid
```

## Critical Constraints

| Constraint                             | Status         |
|----------------------------------------|----------------|
| Execution Time (≤ 10s for 50-page PDF) | Met            |
| Model Size (≤ 200MB)                   | Within limit   |
| Internet Disabled                      | Fully offline  |
| Runtime Platform                       | CPU only       |
| RAM Limit (≤ 16 GB)                    | Met            |
| Input Directory                        | Read-only      |
| Output Format                          | JSON schema    |
| Batch Processing                       | Auto for all PDFs |

## Folder Structure

```
.
├── sample_dataset/
│   ├── pdfs/                # Input PDF files
│   ├── outputs/             # Extracted JSON outputs
│   └── schema/
│       └── output_schema.json
├── utils/
│   └── extractor.py         # PDF parsing and extraction logic
├── main.py                  # Entrypoint for processing PDFs
├── requirements.txt         # Dependencies
├── Dockerfile               # Docker configuration
└── README.md                # Documentation
```

## Input Format

PDFs must be placed in:

```
sample_dataset/pdfs/
```

## Output Format

JSON output for each input PDF will be saved in:

```
sample_dataset/outputs/
```

### Required JSON Structure

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Main Topic", "page": 2 },
    { "level": "H2", "text": "Section Header", "page": 2 },
    { "level": "H3", "text": "• Bullet Point", "page": 2 }
  ],
  "summary": ["...", "..."],
  "registration_info": "...",
  "link": "https://...",
  "dates": ["12/07/2025", "August 15, 2025"]
}
```

## Key Implementation Details

### Heading Extraction Logic

| Level | Criteria |
|-------|----------|
| H1    | Largest text block per page |
| H2    | Medium-sized headings (≤ 6 words) |
| H3    | Lines starting with bullets (•) |

### Summary Generator

- Uses `LexRank` (via `sumy`)
- 100% offline and under 200MB
- Fallback: Top lines of text if summary fails

### Additional Data

- **Title**: Largest text on page 0
- **Links**: Regex-based extraction of URLs
- **Dates**: Regex for multiple date formats
- **Registration Info**: Lines containing keywords like 'register', 'deadline'

## Testing Strategy

| Scenario         | Covered |
|------------------|---------|
| Simple PDFs      | Yes     |
| Multi-page PDFs  | Yes     |
| Complex Layouts  | Yes     |
| Bullet Lists     | Yes     |
| Event Flyers     | Yes     |
| Announcements    | Yes     |

## Validation Checklist

- [x] All PDFs in `/app/input` are processed
- [x] One JSON per input PDF
- [x] Output format matches schema
- [x] Fully offline, no internet access
- [x] Docker build works on `linux/amd64`
- [x] Model size ≤ 200MB
- [x] ≤ 10 seconds for 50 pages
- [x] Uses CPU and ≤ 16GB RAM

## Libraries Used

- `PyMuPDF` for PDF parsing
- `sumy` for LexRank summarization
- `scikit-learn`, `re`, `numpy` for layout & pattern extraction

All libraries are open source and compatible with offline CPU-based environments.


