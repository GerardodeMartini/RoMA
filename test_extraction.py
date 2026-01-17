import fitz

doc = fitz.open("docs/catalogo.pdf")
page = doc[2] # Page 3

words = page.get_text("words")
# words format: (x0, y0, x1, y1, "word", block_no, line_no, word_no)

# Sort by Y0 (with tolerance) then X0
# Group words into rows
rows = []
current_row = []
last_y = -100

# Sort predominantly by Y, then X
words.sort(key=lambda w: (round(w[1]), w[0]))

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

# Construct text strings from rows
for row in rows:
    # Sort by X inside the row just to be sure
    row.sort(key=lambda w: w[0])
    line_text = " ".join([w[4] for w in row])
    print(line_text)
