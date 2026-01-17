import os
import re

IMG_DIR = 'static/img/porcelanatos'
FILTER_SIZE = 30000

def audit():
    files = [f for f in os.listdir(IMG_DIR) if os.path.isfile(os.path.join(IMG_DIR, f))]
    page_files = {}
    
    for f in files:
        match = re.match(r'p(\d+)_', f)
        if match:
            p = match.group(1)
            if p not in page_files: page_files[p] = []
            size = os.path.getsize(os.path.join(IMG_DIR, f))
            if size > FILTER_SIZE:
                page_files[p].append(f)
    
    multi_image_pages = {k: v for k, v in page_files.items() if len(v) > 1}
    
    print(f"Total pages found: {len(page_files)}")
    print(f"Pages with >1 valid image (> {FILTER_SIZE} bytes): {len(multi_image_pages)}")
    print("-" * 30)
    for p, imgs in multi_image_pages.items():
        print(f"Page {p}: {len(imgs)} images -> {imgs}")

if __name__ == "__main__":
    audit()
