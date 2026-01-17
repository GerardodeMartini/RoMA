import json

def patch_data():
    file_path = 'products_new.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    count = 0
    # Standard M2/Box for 20x120 wood tiles
    STANDARD_M2 = 1.68
    
    for p in products:
        model = p.get('Modelo', '').lower()
        # Check for Piemont and Taruma
        if 'piemont' in model or 'taruma' in model:
            # Only update if missing or null
            if not p.get('M2_Caja'):
                p['M2_Caja'] = STANDARD_M2
                count += 1
                print(f"Updated {p['Modelo']} with M2_Caja: {STANDARD_M2}")

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=4, ensure_ascii=False)
        print(f"Successfully patched {count} products.")
    else:
        print("No products needed patching.")

if __name__ == "__main__":
    patch_data()
