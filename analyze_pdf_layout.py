import fitz
import json

doc = fitz.open("docs/catalogo.pdf")
page = doc[2] # Page 3 (0-indexed is 2)

# Extract blocks with coordinates
# Block format: (x0, y0, x1, y1, "text", block_no, block_type)
blocks = page.get_text("blocks")

debug_info = []
for b in blocks:
    debug_info.append({
        "rect": [b[0], b[1], b[2], b[3]],
        "text": b[4],
        "type": b[6]
    })

print(json.dumps(debug_info, indent=2))
