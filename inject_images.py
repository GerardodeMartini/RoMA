import re
import os
from bs4 import BeautifulSoup

HTML_FILE = 'templates/porcelanatos.html'
IMG_DIR = '/static/img/porcelanatos/ambience/'

# Map keywords to image filenames (floor, wall)
# Order matters: more specific first
IMAGE_MAPPING = [
    # CEMENTO
    {
        'keywords': ['cemento gris - mate', 'gris mate', 'concept', 'concreto cl'],
        'floor': 'cemento_gris_mate_floor.png',
        'wall': 'cemento_gris_mate_wall.png'
    },
    {
        'keywords': ['cemento beige', 'arenito', 'apollo - mate'],
        'floor': 'cement_beige_matte_floor.png',
        'wall': 'cement_beige_matte_wall.png'
    },
    {
        'keywords': ['cemento gris - pulido', 'concreto', 'granulado', 'granillado'],
        'floor': 'cement_grey_polished_floor.png',
        'wall': 'cement_grey_polished_wall.png'
    },
    
    # MADERA
    {
        'keywords': ['carvalho natural', 'carvalho nat'],
        'floor': 'carvalho_natural_mate_floor.png',
        'wall': 'carvalho_natural_mate_wall.png'
    },
    {
        'keywords': ['caja', 'piemont', 'taruma', 'fresno', 'madera'],
        'floor': 'wood_neutral_matte_floor.png',
        'wall': 'wood_neutral_matte_wall.png'
    },

    # MARMOL / PIEDRA
    {
        'keywords': ['marmo negro', 'arenito black'],
        'floor': 'marble_black_polished_floor.png',
        'wall': 'marble_black_polished_wall.png'
    },
    {
        'keywords': ['marmo gris', 'silver', 'statuario', 'mirage', 'marmo imperial', 'evok', 'caravaggio', 'apunan'],
        'floor': 'marble_grey_polished_floor.png',
        'wall': 'marble_grey_polished_wall.png'
    },
    {
        'keywords': ['blanco'],
        'floor': 'white_tile_white_polished_floor.png',
        'wall': 'white_tile_white_polished_floor.png' # Fallback for wall
    },
    {
        # CATCH ALL MARBLE/NEUTRAL
        'keywords': ['mármol', 'cremo', 'damasco', 'allure', 'crema', 'brown', 'apollo', 'gran vision', 'lexus', 'arabesco', 'iris', 'montreal', 'golden', 'douro', 'oro', 'bronze', 'dommus', 'algarve', 'pr7', 'r7'],
        'floor': 'cremo_delicato_pulido_floor.png',
        'wall': 'cremo_delicato_pulido_wall.png'
    }
]

def get_images_for_product(title):
    title_lower = title.lower()
    for mapping in IMAGE_MAPPING:
        for kw in mapping['keywords']:
            if kw in title_lower:
                return mapping['floor'], mapping['wall']
    return None, None

def inject_images():
    if not os.path.exists(HTML_FILE):
        print(f"Error: {HTML_FILE} not found.")
        return

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    product_cards = soup.find_all('div', class_='product-card')
    count = 0

    for card in product_cards:
        title_div = card.find('div', class_='product-title')
        if not title_div:
            continue
            
        title = title_div.get_text(strip=True)
        floor_img, wall_img = get_images_for_product(title)
        
        if floor_img and wall_img:
            # Check if already has ambience section, remove it to update
            existing_ambience = card.find('div', class_='ambience-images')
            if existing_ambience:
                existing_ambience.decompose()

            # Create new structure
            ambience_div = soup.new_tag('div', attrs={'class': 'ambience-images mt-3 border-top pt-2'})
            
            h6 = soup.new_tag('h6', attrs={'class': 'text-muted mb-2'})
            h6.string = "Ver en ambiente:"
            ambience_div.append(h6)
            
            row_div = soup.new_tag('div', attrs={'class': 'row'})
            
            # Floor Column
            col_floor = soup.new_tag('div', attrs={'class': 'col-6'})
            img_floor = soup.new_tag('img', src=f"{IMG_DIR}{floor_img}", alt="Ambiente Piso", attrs={'class': 'img-fluid rounded border'})
            small_floor = soup.new_tag('small', attrs={'class': 'd-block text-center mt-1 text-muted'})
            small_floor.string = "Piso"
            col_floor.append(img_floor)
            col_floor.append(small_floor)
            
            # Wall Column
            col_wall = soup.new_tag('div', attrs={'class': 'col-6'})
            img_wall = soup.new_tag('img', src=f"{IMG_DIR}{wall_img}", alt="Ambiente Pared", attrs={'class': 'img-fluid rounded border'})
            small_wall = soup.new_tag('small', attrs={'class': 'd-block text-center mt-1 text-muted'})
            small_wall.string = "Pared"
            col_wall.append(img_wall)
            col_wall.append(small_wall)
            
            row_div.append(col_floor)
            row_div.append(col_wall)
            ambience_div.append(row_div)
            
            # Append to product-info
            info_div = card.find('div', class_='product-info')
            if info_div:
                info_div.append(ambience_div)
                count += 1
        else:
            print(f"Skipping (no match): {title}")

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Successfully injected images into {count} products.")

if __name__ == "__main__":
    inject_images()
