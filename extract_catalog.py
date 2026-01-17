import fitz  # PyMuPDF
import os
import io
from PIL import Image

pdf_path = "docs/catalogo.pdf"
output_dir = "static/img/porcelanatos"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

doc = fitz.open(pdf_path)
catalog_data = []

print(f"Processing {len(doc)} pages...")

for page_index in range(len(doc)):
    page = doc[page_index]
    text = page.get_text("text")
    
    # Extract images
    image_list = page.get_images(full=True)
    saved_images = []
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        image_filename = f"p{page_index+1}_{img_index+1}.{image_ext}"
        image_path = os.path.join(output_dir, image_filename)
        
        with open(image_path, "wb") as f:
            f.write(image_bytes)
            
        saved_images.append(f"/static/img/porcelanatos/{image_filename}")
    
    page_data = {
        "page": page_index + 1,
        "text": text.strip(),
        "images": saved_images
    }
    catalog_data.append(page_data)
    print(f"Page {page_index + 1}: Found {len(saved_images)} images. Text preview: {text.strip()[:50]}...")

print("\nExtraction complete.")
