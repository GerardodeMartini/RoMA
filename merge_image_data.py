import json

def merge_data():
    with open('products_new.json', 'r', encoding='utf-8') as f:
        products_new = json.load(f)
    
    with open('products_manual.json', 'r', encoding='utf-8') as f:
        products_manual = json.load(f)
        
    # Index manual products by Modelo
    manual_map = {p['Modelo']: p for p in products_manual}
    
    count = 0
    for p in products_new:
        modelo = p.get('Modelo')
        if modelo in manual_map:
            page = manual_map[modelo].get('Page')
            if page:
                # Construct default image name
                # We don't verify file existence here, just the convention
                # update_images_list.py logic or generate logic handles existence
                p['imagen'] = f"p{page}_1.jpeg" 
                count += 1
                
    print(f"Merged image/page data for {count} products.")
    
    with open('products_new.json', 'w', encoding='utf-8') as f:
        json.dump(products_new, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    merge_data()
