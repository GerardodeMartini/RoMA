from pypdf import PdfReader
import os

pdf_path = "docs/presentation.pdf"
reader = PdfReader(pdf_path)

print("--- TEXT EXTRACTION START ---")
full_text = ""
for page in reader.pages:
    text = page.extract_text()
    full_text += text + "\n"

with open("extracted_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text)
print("Text saved to extracted_text.txt")
print("--- TEXT EXTRACTION END ---")

# Image extraction (basic)
count = 0
os.makedirs("static/img/extracted", exist_ok=True)

for page in reader.pages:
    for image_file_object in page.images:
        with open(f"static/img/extracted/{count}_{image_file_object.name}", "wb") as fp:
            fp.write(image_file_object.data)
            count += 1

print(f"Extracted {count} images to static/img/extracted/")
