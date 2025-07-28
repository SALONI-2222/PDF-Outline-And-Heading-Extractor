# PDF-Outline-And-Heading-Extractor


# 🧾 PDF Outline Extractor

This project automatically extracts structured outlines (headings and hierarchy) from PDF files by analyzing font sizes and layout patterns.

---

## 📂 Project Structure

```
.
├── main.py               # Main script to extract headings and structure from PDFs
├── requirements.txt      # Python dependency (PyMuPDF)
├── Dockerfile            # For containerized execution
├── input/                # Place your input PDF files here
├── output/               # JSON output files will be saved here
└── process.log           # Log output from the extraction process
```

---

## ✅ Approach

Our approach involves a combination of layout-based and statistical heuristics:

- PDFs are parsed using `PyMuPDF` to extract text with bounding boxes and font sizes.
- Text lines are grouped by their font size and vertical position on the page.
- Larger font sizes are assumed to indicate higher-level headings (H1 > H2 > H3).
- Garbage text (e.g., bullets, noise, short lines) is ignored using custom filters.
- The top three to four font sizes are dynamically mapped to heading levels.
- Output is saved in structured JSON format with title and outline.

---

## 🧠 Libraries Used

- [`PyMuPDF`](https://pymupdf.readthedocs.io/en/latest/) (version 1.22.5)
  - Used to extract text blocks, fonts, and layout metadata from PDF files.

---

## 🔧 How to Build and Run

> ⚠️ Your solution should be compatible with the **Expected Execution** method:
> Docker should run and produce JSONs for PDFs in the `/input` directory.

### 🐳 Docker

```bash
docker build -t pdf-outline-extractor .
docker run --rm -v $PWD/input:/app/input -v $PWD/output:/app/output pdf-outline-extractor
```

### 🐍 Local (Python 3.8+)

```bash
pip install -r requirements.txt
python main.py
```

---

## 📥 Input

- Place all `.pdf` files inside the `input/` directory.
- Supports batch processing of multiple PDF files.

---

## 📤 Output

- Each `.pdf` file produces a `.json` file with this structure:

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Section Title", "page": 1 },
    { "level": "H2", "text": "Subsection", "page": 2 }
  ]
}
```

---

## 📬 Contact

For issues or suggestions, feel free to raise an issue or open a pull request.
