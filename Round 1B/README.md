# 📘 Adobe Hackathon Round 1B - Travel Persona-Based PDF Summarizer

## 🧠 Objective

This solution processes multiple input PDFs and a `input.json` persona-based prompt to extract relevant information and generate a meaningful summary. It is tailored for different personas and tasks such as planning trips, summarizing announcements, or identifying key points from study material.



## 🗂️ Project Structure

adobe_1b/
├── Dockerfile
├── main.py
├── extractor.py
├── requirements.txt
├── README.md
├── approach_explanation.md
├── input/
│ ├── input.json
│ ├── South of France - Cities.pdf
│ ├── South of France - Tips and Tricks.pdf
│ └── ...
├── output/
│ └── output.json

## ⚙️ How to Run (Docker)

### 🧱 Step 1: Build the Docker Image

> In PowerShell (Windows):

```powershell
docker build -t pdf-extractor .
Step 2: Run the Container
powershell
Copy
Edit
docker run --rm `
  -v ${PWD}/input:/app/input `
  -v ${PWD}/output:/app/output `
  pdf-extractor