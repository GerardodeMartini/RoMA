import json
import os
import re

JSON_FILE = 'products_new.json'
IMG_DIR = 'static/img/porcelanatos/'

def get_page_number(filename):
    match = re.match(r'p(\d+)_', filename)
    if match:
        return int(match.group(1))
    return None

def update_product_images():
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        products = json.load(f)

    # list all files in img dir
    all_files = os.listdir(IMG_DIR)
    
    # Filter out subdirs
    all_files = [f for f in all_files if os.path.isfile(os.path.join(IMG_DIR, f))]
    
    # Group by page
    page_images = {}
    for f in all_files:
        page = get_page_number(f)
        if page:
            if page not in page_images:
                page_images[page] = []
            
            # Filter logic: ignore small icon-like files (~24KB) or excessively small
            size = os.path.getsize(os.path.join(IMG_DIR, f))
            if size > 30000: # Filter > 30KB
                page_images[page].append(f)
    
    with open('debug_update.log', 'w') as log:
        log.write(f"Found {len(page_images)} pages with images.\n")
        log.write(f"Sample pages: {list(page_images.keys())[:5]}\n")
        log.write(f"Total products: {len(products)}\n")

        count = 0
        for i, product in enumerate(products):
            current_img = product.get('imagen', '')
            if not current_img:
                continue
                
            page = get_page_number(current_img)
            
            if i < 5:
                match = page in page_images
                log.write(f"Item {i}: '{current_img}' -> Page: {page} Match? {match}\n")

            if page and page in page_images:
                product['imagenes'] = page_images[page]
                count += 1
            else:
                product['imagenes'] = [current_img] if current_img else []
        
        log.write(f"Updated images for {count} products.\n")

    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=4, ensure_ascii=False)
    
    print("Check debug_update.log")

if __name__ == "__main__":
    update_product_images()
