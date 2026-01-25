
import json

try:
    with open("products_manual.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"{'MODELO':<40} | {'DIMENSIONES (FORMATO)':<20}")
    print("-" * 65)
    
    for item in data:
        modelo = item.get('Modelo', 'Sin Nombre')
        formato = item.get('Formato', 'N/A')
        print(f"{modelo:<40} | {formato:<20}")

except Exception as e:
    print(f"Error reading file: {e}")
