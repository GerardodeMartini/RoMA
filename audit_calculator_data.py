import json

def audit_calculator():
    file_path = 'products_new.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)
    except FileNotFoundError:
        print("products_new.json not found.")
        return

    missing_m2_box = []
    missing_price = []

    for p in products:
        model = p.get('Modelo', 'Unknown')
        m2_caja = p.get('M2_Caja')
        price = p.get('Precio_M2')

        # Check M2/Box (Critical: Disables calculator if missing)
        if m2_caja is None or m2_caja == 0 or m2_caja == "-" or m2_caja == "":
            missing_m2_box.append(model)

        # Check Price (Semi-critical: Calculator works but shows 'Consultar')
        if price is None or price == 0 or price == "-":
            missing_price.append(model)

    print(f"Total Products Checked: {len(products)}")
    print("-" * 30)
    print(f"Products with MISSING M2/BOX (Calculator Disabled): {len(missing_m2_box)}")
    for m in missing_m2_box:
        print(f" - {m}")
    
    print("-" * 30)
    print(f"Products with MISSING PRICE (Shows 'Consultar'): {len(missing_price)}")
    # Uncomment to list missing prices if needed, but usually less critical
    # for m in missing_price:
    #     print(f" - {m}")

if __name__ == "__main__":
    audit_calculator()
