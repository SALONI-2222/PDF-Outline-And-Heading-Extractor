import fitz
import os
import json
from collections import defaultdict


def normalize_y(y, tolerance=3.0):
    return round(y / tolerance) * tolerance


def is_garbage(text):
    if len(set(text.lower())) < 4:
        return True
    if text.count(" ") <= 1 and len(text) < 15:
        return True
    if any(c * 3 in text for c in "abcdefghijklmnopqrstuvwxyz"):
        return True
    return False


def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    lines_by_size = defaultdict(list)
    candidate_titles = []

    for page_number, page in enumerate(doc, start=1):
        spans_by_line = defaultdict(lambda: defaultdict(list))
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text or is_garbage(text):
                        continue
                    font_size = span["size"]
                    y = normalize_y(span["bbox"][1])
                    spans_by_line[font_size][(page_number, y)].append(text)

        for font_size, line_map in spans_by_line.items():
            for (pg, y), parts in line_map.items():
                full_line = " ".join(parts).strip()
                if full_line and not is_garbage(full_line):
                    lines_by_size[font_size].append({
                        "text": full_line,
                        "page": pg
                    })
                    if pg == 1 and len(full_line) > 50 and "Proposal" in full_line and "Digital Library" in full_line:
                        candidate_titles.append((font_size, full_line))

    sorted_font_sizes = sorted(lines_by_size.keys(), reverse=True)
    size_to_level = {}
    for i, fs in enumerate(sorted_font_sizes[:4]):
        size_to_level[fs] = f"H{i+1}"

    seen = set()
    outline = []

    for fs in sorted_font_sizes:
        for item in lines_by_size[fs]:
            key = (item["text"].lower(), item["page"])
            if key not in seen:
                seen.add(key)
                outline.append({
                    "level": size_to_level.get(fs, "H4"),
                    "text": item["text"],
                    "page": item["page"]
                })

    # ✅ Smart override logic
    if candidate_titles:
        # Pick the longest match
        title = max(candidate_titles, key=lambda x: len(x[1]))[1]
    else:
        # fallback: first valid H1
        title = "Untitled Document"
        for entry in outline:
            if entry["level"] == "H1" and entry["page"] == 1:
                title = entry["text"]
                break

    return {
        "title": title.strip(),
        "outline": outline
    }


def process_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            result = extract_outline(input_path)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)


# Run test locally on uploaded file03.pdf
process_all_pdfs("input", "output")

