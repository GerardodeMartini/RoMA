import fitz
import json
import os

pdf_path = "docs/catalogo.pdf"
doc = fitz.open(pdf_path)
catalog_data = []

for page_index in range(len(doc)):
    page = doc[page_index]
    text = page.get_text("text").strip()
    
    # Check for existing images for this page
    # We assume images are named p{page_index+1}_*.ext
    saved_images = []
    # This is a simplification; ideally we list the directory
    # But for now let's just use the text to see what products are there
    
    catalog_data.append({
        "page": page_index + 1,
        "text": text
    })

with open("catalog_data.json", "w", encoding="utf-8") as f:
    json.dump(catalog_data, f, indent=4, ensure_ascii=False)
