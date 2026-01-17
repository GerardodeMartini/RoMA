import json
import re
import os

# Load structured data
with open("catalog_data_structured.json", "r", encoding="utf-8") as f:
    data = json.load(f)

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
    .catalog-section { padding: 40px 0; }
    .category-title { 
        margin-top: 50px; 
        margin-bottom: 30px; 
        border-bottom: 2px solid var(--primary-color); 
        padding-bottom: 10px; 
        color: var(--primary-color);
        font-family: var(--font-heading);
    }
    .product-card {
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        overflow: hidden;
        margin-bottom: 30px;
        transition: transform 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        border: 1px solid #eee;
    }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
    .product-image {
        height: 280px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f8f9fa;
        position: relative;
    }
    .product-image img {
        max-height: 100%;
        width: auto;
        max-width: 100%;
        object-fit: contain;
    }
    .product-info { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; }
    .product-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 5px; color: #333; font-family: var(--font-heading); }
    .product-price { 
        font-size: 1.4rem; 
        color: var(--accent-color-2); 
        font-weight: 700; 
        margin-bottom: 15px;
        display: block;
    }
    .specs-list { list-style: none; padding: 0; margin: 0; font-size: 0.9rem; color: #555; }
    .specs-list li { margin-bottom: 6px; display: flex; align-items: flex-start; }
    .specs-list strong { color: #333; min-width: 140px; display: inline-block; font-weight: 600; flex-shrink: 0; }
    .specs-list span { display: inline-block; }
    
    .category-nav a {
        display: inline-block;
        padding: 5px 15px;
        margin: 0 5px 10px;
        border: 1px solid var(--primary-color);
        color: var(--primary-color);
        border-radius: 20px;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    .category-nav a:hover {
        background: var(--primary-color);
        color: white;
        text-decoration: none;
    }
</style>

{% endblock %}
"""

# Main loop using products_new.json
with open("products_new.json", "r", encoding="utf-8") as f:
    products_new = json.load(f)

current_category = ""
html_body = ""
temp_cat_html = ""
products_in_cat = []

# Group by category (Line) to maintain structure
# But products_new.json is a flat list. We need to group them.
from collections import defaultdict
products_by_cat = defaultdict(list)
categories = []

for p in products_new:
    cat = p.get('Linea', 'Varios').upper()
    products_by_cat[cat].append(p)

for category, items in products_by_cat.items():
    cat_title = category.title()
    categories.append(cat_title)
    
    cat_html = f'<div id="{cat_title.replace(" ", "-").lower()}" class="category-block">'
    cat_html += f'<h2 class="category-title">{cat_title}</h2>'
    cat_html += '<div class="row" style="display: flex; flex-wrap: wrap; margin: 0 -15px;">'
    
    for p in items:
        title = p.get('Modelo', 'Producto sin nombre')
        price_val = p.get('Precio_M2', 0)
        price = f"${price_val} M2 +IVA" if price_val else "Consultar Precio"
        
        # Specs from JSON
        specs_data = p.get('Especificaciones', {})
        # Map JSON keys to display keys
        display_specs = {
            'Formato': p.get('Formato', '-'),
            'Tipología': p.get('Tipologia', '-'),
            'Faces': specs_data.get('Caras', '-'),
            'Espesor': specs_data.get('Espesor', '-'),
            'Área de Uso': p.get('Uso', '-'),
            'Rectificado': p.get('Rectificado', '-'),
            'Junta asent.': specs_data.get('Junta', '-'),
            'Resist. Manchas': specs_data.get('Resistencia_Manchas', '-'),
            'Variación Tono': specs_data.get('Variacion_Tono', '-'),
            'M2/Caja': p.get('M2_Caja', '-'),
            'Peso/Caja': f"{specs_data.get('Peso_Caja_kg', '-')} kg"
        }

        # Image Logic
        # Use the 'imagen' field from JSON as the primary image
        main_image = p.get('imagen', '')
        
        # Try to find page number from main image to find context images
        page_num = None
        match = re.search(r'p(\d+)_', main_image)
        if match:
             page_num = match.group(1)
        
        candidates = []
        if page_num:
            base_dir = "static/img/porcelanatos"
            # Filter candidates: 
            # 1. Exclude known logo size (24014 bytes)
            # 2. Exclude very small icons (<2KB)
            # 3. Exclude '4th image' artifact (files ending in _4)
            raw_candidates = [f for f in os.listdir(base_dir) if f.startswith(f"p{page_num}_")]
            for f in raw_candidates:
                # User request: "saca la 4ta imagen" (usually pXX_4.jpeg is a gray placeholder)
                if "_4." in f:
                    continue
                    
                size = os.path.getsize(os.path.join(base_dir, f))
                # 24014 is the exact size of the recurring 'Roma' logo artifact
                if size > 2000 and not (24000 < size < 24100):
                    candidates.append(f)
            candidates.sort()
        
        # Ensure main image is first if it exists in candidates, or add it
        if main_image and main_image in candidates:
             candidates.remove(main_image)
             candidates.insert(0, main_image)
        elif main_image and main_image not in candidates:
             # Just add it if it ends with valid ext and exists
             if os.path.exists(os.path.join("static/img/porcelanatos", main_image)):
                 candidates.insert(0, main_image)
             
        # Carousel ID
        safe_title = re.sub(r'[^a-zA-Z0-9]', '', title)
        carousel_id = f"carousel_{safe_title}"
        
        image_html = ""
        if not candidates:
             image_html = f'<img src="/static/img/no-image.png" alt="{title}">'
        elif len(candidates) == 1:
             image_html = f'<img src="/static/img/porcelanatos/{candidates[0]}" alt="{title}" class="img-fluid clickable-image" onclick="openImageModal(this.src)">'
        else:
             # Build Carousel
             image_html = f'<div id="{carousel_id}" class="carousel slide" data-ride="carousel" data-interval="false">'
             image_html += '<div class="carousel-inner">'
             for i, img in enumerate(candidates):
                 active_class = "active" if i == 0 else ""
                 image_html += f"""
                 <div class="carousel-item {active_class}">
                    <img src="/static/img/porcelanatos/{img}" class="d-block w-100 clickable-image" alt="{title}" onclick="openImageModal(this.src)">
                 </div>
                 """
             image_html += '</div>'
             # Controls - Enhanced Styling with Background Circle
             image_html += f"""
             <a class="carousel-control-prev" href="#{carousel_id}" role="button" data-slide="prev" style="opacity: 1;">
                <span class="carousel-control-prev-icon" aria-hidden="true" style="background-color: rgba(0,0,0,0.5); border-radius: 50%; width: 35px; height: 35px; background-size: 60%; background-position: center;"></span>
                <span class="sr-only">Previous</span>
             </a>
             <a class="carousel-control-next" href="#{carousel_id}" role="button" data-slide="next" style="opacity: 1;">
                <span class="carousel-control-next-icon" aria-hidden="true" style="background-color: rgba(0,0,0,0.5); border-radius: 50%; width: 35px; height: 35px; background-size: 60%; background-position: center;"></span>
                <span class="sr-only">Next</span>
             </a>
             </div>
             """

        # Prepare data for Modal
        images_data = ",".join(candidates) if candidates else "no-image.png"
        m2_box_val = display_specs['M2/Caja'] if display_specs['M2/Caja'] != '-' else 0
        
        # Ensure price is a clean number for JS
        price_clean = 0
        if isinstance(price_val, (int, float)):
             price_clean = price_val
        
        cat_html += f"""
        <div class="col-lg-6 col-md-12 mb-4" style="padding: 0 15px;">
            <div class="product-card">
                <div class="row no-gutters">
                    <div class="col-md-5">
                       <div class="product-image" 
                            style="height: 100%; min-height: 250px; background: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center;"
                            onclick='openProductModal(this)'
                            data-title="{title}"
                            data-price="{price_clean}"
                            data-m2box="{m2_box_val}"
                            data-images="{images_data}">
                           {image_html}
                       </div>
                    </div>
                    <div class="col-md-7">
                        <div class="product-info">
                            <div class="product-title">{title}</div>
                            <div class="product-price">{price}</div>
                            <ul class="specs-list">
                                <li><strong>Formato:</strong> <span>{display_specs['Formato']}</span></li>
                                <li><strong>Tipología:</strong> <span>{display_specs['Tipología']}</span></li>
                                <li><strong>Caras:</strong> <span>{display_specs['Faces']}</span></li>
                                <li><strong>Espesor:</strong> <span>{display_specs['Espesor']}</span></li>
                                <li><strong>Uso:</strong> <span>{display_specs['Área de Uso']}</span></li>
                                <li><strong>Rectificado:</strong> <span>{display_specs['Rectificado']}</span></li>
                                
                                <li style="margin-top: 10px; border-top: 1px dashed #eee; padding-top: 5px;"><strong>Junta:</strong> <span>{display_specs['Junta asent.']}</span></li>
                                <li><strong>Manchas:</strong> <span>{display_specs['Resist. Manchas']}</span></li>
                                <li><strong>Var. Tono:</strong> <span>{display_specs['Variación Tono']}</span></li>
                                <li><strong>M2/Caja:</strong> <span>{display_specs['M2/Caja']}</span></li>
                                <li><strong>Peso/Caja:</strong> <span>{display_specs['Peso/Caja']}</span></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    cat_html += '</div></div>'
    html_body += cat_html

# Build Nav
nav_html = ""
for cat in categories:
    nav_html += f'<a href="#{cat.replace(" ", "-").lower()}">{cat}</a>'

# Detailed Product Modal + Calculator (Injected directly by script)
modal_html = """
<!-- Product Detail Modal -->
<div class="modal fade" id="productModal" tabindex="-1" role="dialog" aria-hidden="true" style="z-index: 10500;">
  <div class="modal-dialog modal-xl modal-dialog-centered" role="document">
    <div class="modal-content" style="border: none; border-radius: 15px; overflow: hidden;">
      
      <div class="modal-body p-0">
         <div class="row no-gutters">
            <!-- Left: Carousel -->
            <div class="col-lg-8 bg-dark d-flex align-items-center justify-content-center" style="min-height: 400px; background-color: #f8f9fa !important;">
                 <div id="modalCarousel" class="carousel slide" data-ride="carousel" style="width: 100%; height: 100%;">
                    <div class="carousel-inner" id="modalCarouselInner" style="height: 100%; display: flex; align-items: center;">
                        <!-- Slides injected via JS -->
                    </div>
                    <a class="carousel-control-prev" href="#modalCarousel" role="button" data-slide="prev" style="opacity: 1;">
                        <span class="carousel-control-prev-icon" aria-hidden="true" style="background-color: rgba(0,0,0,0.5); border-radius: 50%; width: 40px; height: 40px; background-size: 60%; background-position: center;"></span>
                    </a>
                    <a class="carousel-control-next" href="#modalCarousel" role="button" data-slide="next" style="opacity: 1;">
                        <span class="carousel-control-next-icon" aria-hidden="true" style="background-color: rgba(0,0,0,0.5); border-radius: 50%; width: 40px; height: 40px; background-size: 60%; background-position: center;"></span>
                    </a>
                 </div>
            </div>
            
            <!-- Right: Info & Calculator -->
            <div class="col-lg-4 p-4">
                 <button type="button" class="close" data-dismiss="modal" aria-label="Close" style="position: absolute; right: 15px; top: 10px;">
                   <span aria-hidden="true">&times;</span>
                 </button>
                 
                 <h3 id="modalTitle" class="mb-2" style="font-weight: 700;">Nombre Producto</h3>
                 <p id="modalPriceLabel" class="text-muted mb-4" style="font-size: 1.2rem;">$ Precio</p>
                 
                 <hr>
                 
                 <h5 class="mb-3"><i class="fas fa-calculator"></i> Calculadora de Material</h5>
                 <form>
                    <div class="form-group">
                        <label for="inputM2">Metros Cuadrados a Cubrir (m²)</label>
                        <input type="number" class="form-control" id="inputM2" placeholder="Ej: 45" step="0.01" oninput="calculateMaterial()">
                    </div>
                    
                    <div class="alert alert-secondary" role="alert" style="font-size: 0.9rem;">
                        <input type="hidden" id="boxM2">
                        <input type="hidden" id="unitPrice">
                        
                        <div class="d-flex justify-content-between mb-2">
                           <span>M²/Caja:</span>
                           <strong id="displayBoxM2">-</strong>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                           <span>Cajas Necesarias:</span>
                           <strong id="resultBoxes" style="color: #d9534f; font-size: 1.1rem;">-</strong>
                        </div>
                        <div class="d-flex justify-content-between border-top pt-2">
                           <span>Total m² Real:</span>
                           <strong id="resultTotalM2">-</strong>
                        </div>
                    </div>
                    
                    <div class="text-center mt-4">
                        <small class="text-muted d-block uppercase">Precio Estimado (IVA Incl.)</small>
                        <h2 id="resultPrice" style="color: #28a745; font-weight: bold;">$ -</h2>
                    </div>
                 </form>
            </div>
         </div>
      </div>
      
    </div>
  </div>
</div>

<script>
function openProductModal(element) {
    // 1. Get Data
    const title = element.getAttribute('data-title');
    const price = parseFloat(element.getAttribute('data-price')) || 0;
    const m2box = parseFloat(element.getAttribute('data-m2box')) || 0;
    const imagesStr = element.getAttribute('data-images');
    const images = imagesStr.split(',');

    // 2. Populate Info
    document.getElementById('modalTitle').innerText = title;
    document.getElementById('modalPriceLabel').innerText = price > 0 ? '$' + price.toLocaleString() + ' m² +IVA' : 'Consultar Precio';
    
    // 3. Setup Calculator Vars
    document.getElementById('unitPrice').value = price;
    document.getElementById('boxM2').value = m2box;
    document.getElementById('displayBoxM2').innerText = m2box > 0 ? m2box + ' m²' : 'Consultar';
    document.getElementById('inputM2').value = ''; // Reset
    document.getElementById('resultBoxes').innerText = '-';
    document.getElementById('resultTotalM2').innerText = '-';
    document.getElementById('resultPrice').innerText = '$ -';
    
    // Disable input if no m2 data
    document.getElementById('inputM2').disabled = (m2box <= 0);

    // 4. Build Carousel
    const carouselInner = document.getElementById('modalCarouselInner');
    carouselInner.innerHTML = '';
    
    images.forEach((img, index) => {
        const active = index === 0 ? 'active' : '';
        // If image is just filename, prepend path. If already path (no-image), leave properly.
        const src = img.includes('no-image') ? '/static/img/no-image.png' : '/static/img/porcelanatos/' + img;
        
        const item = `
            <div class="carousel-item ${active}" style="height: 100%; text-align: center;">
                <img src="${src}" class="img-fluid" style="max-height: 500px; max-width: 100%; object-fit: contain;">
            </div>
        `;
        carouselInner.innerHTML += item;
    });

    // 5. Show
    $('#productModal').modal('show');
}

function calculateMaterial() {
    const inputM2 = parseFloat(document.getElementById('inputM2').value) || 0;
    const boxM2 = parseFloat(document.getElementById('boxM2').value) || 0;
    const price = parseFloat(document.getElementById('unitPrice').value) || 0;
    
    if (inputM2 <= 0 || boxM2 <= 0) {
        document.getElementById('resultBoxes').innerText = '-';
        document.getElementById('resultTotalM2').innerText = '-';
        document.getElementById('resultPrice').innerText = '$ -';
        return;
    }
    
    // Logic: Ceiling(Input / BoxM2) = Boxes
    const boxes = Math.ceil(inputM2 / boxM2);
    const totalM2 = boxes * boxM2;
    // Price calculation: TotalM2 * Price * 1.21 (IVA) -> User said "+IVA" in label, usually final price display includes it? 
    // Label says "Precio Estimado (IVA Incl.)" in my HTML.
    // If input price is "16200 + IVA", then calculation should be * 1.21
    
    const estimatedTotal = totalM2 * price * 1.21;
    
    document.getElementById('resultBoxes').innerText = boxes;
    document.getElementById('resultTotalM2').innerText = totalM2.toFixed(2) + ' m²';
    
    if (price > 0) {
        document.getElementById('resultPrice').innerText = '$ ' + estimatedTotal.toLocaleString('es-AR', {minimumFractionDigits: 0, maximumFractionDigits: 0});
    } else {
         document.getElementById('resultPrice').innerText = 'Consultar';
    }
}
</script>
"""

full_html = html_header + nav_html + "</div>" + html_body + modal_html + html_footer

with open("templates/porcelanatos.html", "w", encoding="utf-8") as f:
    f.write(full_html)
    
print("Template updated with products_new.json data and cleaner images.")
