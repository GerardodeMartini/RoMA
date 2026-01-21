import fitz  # PyMuPDF
import os

def extract_images():
    pdf_path = "docs/catalogo.pdf"
    output_dir = "static/img/extracted_pymupdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    else:
        # Optional: clear directory? Better not delete without permission.
        print(f"Output directory exists: {output_dir}")

    doc = fitz.open(pdf_path)
    print(f"PDF opened: {len(doc)} pages.")
    
    total_extracted = 0
    
    for page_index in range(len(doc)):
        page = doc[page_index]
        image_list = page.get_images(full=True)
        
        # print(f"Page {page_index + 1}: Found {len(image_list)} images.")
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Filename format: p{Page}_{Index}.ext (e.g., p16_1.jpeg)
            # Page is 1-based index (page_index + 1)
            # Index is 1-based counter (img_index + 1)
            image_filename = f"p{page_index + 1}_{img_index + 1}.{image_ext}"
            image_filepath = os.path.join(output_dir, image_filename)
            
            with open(image_filepath, "wb") as f:
                f.write(image_bytes)
            
            total_extracted += 1

    print("-" * 30)
    print(f"Extraction Completed.")
    print(f"Total Images: {total_extracted}")
    print(f"Saved to: {output_dir}")

if __name__ == "__main__":
    extract_images()
