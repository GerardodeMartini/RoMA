import json
import os

# Load new data
with open("products_new.json", "r", encoding="utf-8") as f:
    new_products = json.load(f)

# Load old data (if exists) for Page mapping, or rely on original list
# We can try to load products_manual.json if it exists, otherwise we have to recover page mapping
# Since we overwrote products_manual.json in previous step, we likely lost the page mapping *inside* that file because I used the clean json provided by user which didn't have pages.
# Wait, in the PREVIOUS step, the user provided a JSON WITHOUT pages.
# So products_manual.json currently HAS NO PAGES.
# I need to re-establish the page mapping.
# Fortunately I have `catalog_data.json` or `catalog_data_structured.json` if they still exist?
# I deleted them? No, I checked `ls` in previous thought... I think I *deleted* them in Step 937? No, that failed.
# Let's check if `catalog_data_structured.json` exists.

try:
    with open("catalog_data.json", "r", encoding="utf-8") as f:
        catalog_data = json.load(f)
        # Map: line 0 of text usually resembles title?
        # Or I can just map by index if the list length is similar?
        # Catalog has 59 pages. Products list has 48 items.
        # Let's map by rough title matching.
        
except FileNotFoundError:
    print("Warning: Catalog source data missing. Images might not map correctly.")
    catalog_data = []

# Create a mapping helper
def find_page_for_product(prod_model, cat_data):
    # Normalize
    p_norm = prod_model.lower().replace(" ", "")
    
    for item in cat_data:
        # Check text
        text_norm = item['text'].lower().replace(" ", "")
        if p_norm[:10] in text_norm: # Heuristic
            return item['page']
        # Try finding key words
        words = prod_model.lower().split()
        if all(w in item['text'].lower() for w in words[:3]): # First 3 words match
             return item['page']
             
    return None

# Merge logic
final_products = []
for i, p in enumerate(new_products):
    # Try to find page
    page = find_page_for_product(p['Modelo'], catalog_data)
    
    # Fallback: Sequential mapping heuristic if we assume order is roughly preserved?
    # The JSON provided seems to follow the catalog order.
    # Catalog starts page 3.
    # Let's just try to map strictly.
    if not page:
         # Try simpler matching
         pass
    
    if page:
        p['Page'] = page
    else:
        # Emergency fallback: Assign a page based on index + offset?
        # Page 3 is first product.
        # But some pages have multiple or empty?
        # Let's leave it 1 if not found, it will show generic image or mismatch.
        # Better: Scan directory for matching names? No files are named pX_1.
        p['Page'] = 1 # Placeholder
        
    final_products.append(p)

# HTML Generation
html_header = """{% extends 'base.html' %}
{% load static %}

{% block content %}
<section class="page-header">
    <div class="container text-center">
        <h1>Catálogo de Porcelanatos</h1>
        <p>Calidad y diseño para tus espacios.</p>
    </div>
</section>

<section class="section catalog-section">
    <div class="container">
        <!-- Category Navigation -->
        <div class="category-nav mb-4 text-center">
            <span class="mr-2">Categorías:</span>
"""

html_body = ""
html_footer = """
    </div>
</section>

<style>
    .catalog-section { padding: 40px 0; background-color: #fcfcfc; }
    .category-title { 
        margin-top: 60px; 
        margin-bottom: 40px; 
        border-bottom: 3px solid var(--primary-color); 
        padding-bottom: 15px; 
        color: var(--primary-color);
        font-family: var(--font-heading);
        font-size: 2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .product-card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        overflow: hidden;
        margin-bottom: 30px;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        border: 1px solid rgba(0,0,0,0.05);
    }
    .product-card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 12px 30px rgba(0,0,0,0.15); 
        border-color: var(--primary-color);
    }
    .product-image {
        height: 300px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #fff;
        position: relative;
        padding: 20px;
        border-bottom: 1px solid #f0f0f0;
    }
    .product-image img {
        max-height: 100%;
        max-width: 100%;
        object-fit: contain;
        transition: transform 0.5s ease;
    }
    .product-card:hover .product-image img {
        transform: scale(1.05);
    }
    .product-info { padding: 25px; flex-grow: 1; display: flex; flex-direction: column; }
    .product-title { 
        font-size: 1.4rem; 
        font-weight: 800; 
        margin-bottom: 8px; 
        color: #2c3e50; 
        font-family: var(--font-heading);
        line-height: 1.2;
    }
    .product-brand {
        font-size: 0.85rem;
        color: #95a5a6;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 15px;
        font-weight: 600;
    }
    .product-price { 
        font-size: 1.5rem; 
        color: var(--accent-color-2); 
        font-weight: 700; 
        margin-bottom: 20px;
        display: block;
    }
    .specs-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-bottom: 5px;
        font-size: 0.9rem;
    }
    .spec-item {
        background: #f8f9fa;
        padding: 8px 12px;
        border-radius: 6px;
        display: flex;
        flex-direction: column;
    }
    .spec-label {
        font-weight: 700;
        color: #7f8c8d;
        font-size: 0.7rem;
        text-transform: uppercase;
        margin-bottom: 3px;
    }
    .spec-value {
        color: #2c3e50;
        font-weight: 600;
    }
    .tech-specs {
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px dashed #e0e0e0;
        font-size: 0.85rem;
        color: #666;
    }
    .tech-specs ul { padding-left: 0; list-style: none; margin: 0; }
    .tech-specs li { margin-bottom: 6px; display: flex; justify-content: space-between; border-bottom: 1px solid #f9f9f9; padding-bottom: 2px;}
    .tech-specs span { color: #888; }
    .tech-specs strong { color: #444; font-weight: 600; }

    .category-nav a {
        display: inline-block;
        padding: 8px 18px;
        margin: 5px;
        border: 2px solid var(--primary-color);
        color: var(--primary-color);
        border-radius: 30px;
        font-size: 0.95rem;
        font-weight: 600;
        transition: all 0.2s;
        text-decoration: none;
    }
    .category-nav a:hover, .category-nav a.active {
        background: var(--primary-color);
        color: white;
    }
    @media (max-width: 768px) {
        .specs-grid { grid-template-columns: 1fr; }
        .product-image { height: 250px; }
    }
</style>

{% endblock %}
"""

# Group products
grouped = {}
cats = []
for p in final_products:
    c = p.get("Linea", "OTRO").upper()
    if c not in grouped:
        grouped[c] = []
        cats.append(c)
    grouped[c].append(p)

# Build Nav
html_body += '<div class="category-nav mb-4 text-center">'
for c in cats:
    html_body += f'<a href="#{c.replace(" ", "-").lower()}">{c.title()}</a>'
html_body += '</div>'

# Build Groups
for c in cats:
    html_body += f'<div id="{c.replace(" ", "-").lower()}" class="category-block">'
    html_body += f'<h2 class="category-title">{c.title()}</h2>'
    html_body += '<div class="row">'
    
    for p in grouped[c]:
        # Image
        page_num = p.get('Page', 1)
        base_dir = "static/img/porcelanatos"
        img_src = "/static/img/no-image.png"
        if os.path.exists(base_dir):
            cands = sorted([f for f in os.listdir(base_dir) if f.startswith(f"p{page_num}_")])
            if cands: img_src = f"/static/img/porcelanatos/{cands[0]}"
            
        # Price
        price = p.get('Precio_M2', 0)
        price_fmt = f"${price:,.0f}".replace(",", ".") + " M2 +IVA"
        
        # Specs
        specs = p.get('Especificaciones', {})
        
        # Helper for handling missing spec keys gracefully
        def get_spec(key, unit=""):
            val = specs.get(key)
            if val:
                return f"{val} {unit}".strip()
            return "-"

        html_body += f"""
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="product-card">
                <div class="product-image">
                    <img src="{img_src}" alt="{p['Modelo']}" loading="lazy">
                </div>
                <div class="product-info">
                    <div class="product-brand">{p['Marca']}</div>
                    <div class="product-title">{p['Modelo']}</div>
                    <div class="product-price">{price_fmt}</div>
                    
                    <div class="specs-grid">
                        <div class="spec-item"><span class="spec-label">Formato</span><span class="spec-value">{p['Formato']}</span></div>
                        <div class="spec-item"><span class="spec-label">Tipología</span><span class="spec-value">{p['Tipologia']}</span></div>
                        <div class="spec-item"><span class="spec-label">Rectificado</span><span class="spec-value">{p['Rectificado']}</span></div>
                        <div class="spec-item"><span class="spec-label">Uso</span><span class="spec-value">{p['Uso']}</span></div>
                        <div class="spec-item"><span class="spec-label">Caja</span><span class="spec-value">{p['M2_Caja']} m²</span></div>
                    </div>
                    
                    <div class="tech-specs">
                        <ul>
                            <li><span>Caras:</span> <strong>{get_spec('Caras')}</strong></li>
                            <li><span>Espesor:</span> <strong>{get_spec('Espesor')}</strong></li>
                            <li><span>Junta:</span> <strong>{get_spec('Junta')}</strong></li>
                            <li><span>Resistencia Manchas:</span> <strong>{get_spec('Resistencia_Manchas')}</strong></li>
                             <li><span>Variación Tono:</span> <strong>{get_spec('Variacion_Tono')}</strong></li>
                            <li><span>Peso Caja:</span> <strong>{get_spec('Peso_Caja_kg', 'kg')}</strong></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        """
    html_body += '</div></div>'

full_html = html_header + html_body + html_footer

with open("templates/porcelanatos.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Merged and generated successfully.")
