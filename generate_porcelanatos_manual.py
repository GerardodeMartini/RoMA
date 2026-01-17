import json
import os

# Load manually curated data
with open("products_manual.json", "r", encoding="utf-8") as f:
    products = json.load(f)

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

# Group by Category (Linea)
grouped_products = {}
categories_list = []

for p in products:
    cat = p.get('Linea', 'Otros').upper()
    if cat not in grouped_products:
        grouped_products[cat] = []
        categories_list.append(cat)
    grouped_products[cat].append(p)

# Build Nav
nav_html = ""
for cat in categories_list:
    nav_html += f'<a href="#{cat.replace(" ", "-").lower()}">{cat.title()}</a>'

html_body += nav_html + "</div>"

# Build Categories
for cat in categories_list:
    cat_products = grouped_products[cat]
    
    cat_html = f'<div id="{cat.replace(" ", "-").lower()}" class="category-block">'
    cat_html += f'<h2 class="category-title">{cat.title()}</h2>'
    cat_html += '<div class="row">'
    
    for p in cat_products:
        # Determine Image
        # We use 'Page' field to map to extracted image p{Page}_1.jpeg (or png)
        page_num = p.get('Page', 1)
        base_dir = "static/img/porcelanatos"
        img_src = "/static/img/no-image.png"
        
        # Look for p{page_num}_* in directory
        if os.path.exists(base_dir):
            candidates = sorted([f for f in os.listdir(base_dir) if f.startswith(f"p{page_num}_")])
            if candidates:
                img_src = f"/static/img/porcelanatos/{candidates[0]}"
        
        # Format Price
        price = p.get('Precio_M2', 0)
        formatted_price = f"${price:,.0f}".replace(",", ".") + " M2 +IVA"
        
        # Null handling
        m2_caja = p.get('M2_Caja')
        m2_caja_str = f"{m2_caja} m²" if m2_caja else "-"


        cat_html += f"""
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="product-card">
                <div class="product-image">
                    <img src="{img_src}" alt="{p['Modelo']}" loading="lazy">
                </div>
                <div class="product-info">
                    <div class="product-brand">{p['Marca']}</div>
                    <div class="product-title">{p['Modelo']}</div>
                    <div class="product-price">{formatted_price}</div>
                    
                    <div class="specs-grid">
                        <div class="spec-item">
                            <span class="spec-label">Formato</span>
                            <span class="spec-value">{p['Formato']}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">Tipología</span>
                            <span class="spec-value">{p['Tipologia']}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">Rectificado</span>
                            <span class="spec-value">{p['Rectificado']}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">Uso</span>
                            <span class="spec-value">{p['Uso']}</span>
                        </div>
                        <div class="spec-item">
                            <span class="spec-label">Caja</span>
                            <span class="spec-value">{m2_caja_str}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    cat_html += '</div></div>'
    html_body += cat_html

full_html = html_header + html_body + html_footer

with open("templates/porcelanatos.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Template generated successfully from manual JSON.")
