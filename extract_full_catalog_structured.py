import fitz
import json

doc = fitz.open("docs/catalogo.pdf")
catalog_data = []

for page_index in range(len(doc)):
    page = doc[page_index]
    words = page.get_text("words")
    # (x0, y0, x1, y1, "word", block_no, line_no, word_no)
    
    # Sort by Y0 (with tolerance) then X0
    words.sort(key=lambda w: (round(w[1]), w[0]))
    
    rows = []
    current_row = []
    last_y = -100
    
    for w in words:
        y = w[1]
        text = w[4]
        
        if abs(y - last_y) < 5: # Same row threshold
            current_row.append(w)
        else:
            if current_row:
                rows.append(current_row)
            current_row = [w]
            last_y = y
            
    if current_row:
        rows.append(current_row)
        
    # Build text lines
    text_lines = []
    for row in rows:
        row.sort(key=lambda w: w[0])
        line_text = " ".join([w[4] for w in row])
        text_lines.append(line_text)
        
    catalog_data.append({
        "page": page_index + 1,
        "lines": text_lines
    })

with open("catalog_data_structured.json", "w", encoding="utf-8") as f:
    json.dump(catalog_data, f, indent=4, ensure_ascii=False)

print("Structured extraction complete.")
