import json
import re
from collections import defaultdict

def analyze_products(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

    print(f"Total products: {len(products)}")

    clusters = defaultdict(list)
    
    for p in products:
        # Extract key features
        linea = p.get('Linea', '').lower()
        modelo = p.get('Modelo', '').lower()
        tipologia = p.get('Tipologia', '').lower()
        
        # Determine Material/Look
        material = 'generic'
        if 'cemento' in linea or 'cemento' in modelo or 'concreto' in linea or 'concreto' in modelo:
            material = 'cement'
        elif 'madera' in linea or 'madera' in modelo or 'wood' in modelo:
            material = 'wood'
        elif 'mármol' in linea or 'marmol' in linea or 'marmo' in modelo or 'calacatta' in modelo or 'carrara' in modelo:
            material = 'marble'
        elif 'granito' in modelo or 'granillado' in modelo:
            material = 'granite'
        elif 'piedra' in modelo or 'stone' in linea or 'stone' in modelo:
            material = 'stone'
        elif 'blanca' in linea:
             material = 'white_tile'
        
        # Determine Tone/Color
        color = 'neutral'
        if 'gris' in modelo or 'grey' in modelo or 'silver' in modelo or 'ceniza' in modelo:
            color = 'grey'
        elif 'beige' in modelo or 'crema' in modelo or 'bone' in modelo or 'arena' in modelo or 'marfil' in modelo:
            color = 'beige'
        elif 'blanco' in modelo or 'white' in modelo or 'nieve' in modelo:
            color = 'white'
        elif 'negro' in modelo or 'black' in modelo or 'oscuro' in modelo:
            color = 'black'
        elif 'marron' in modelo or 'brown' in modelo or 'cafe' in modelo or 'noce' in modelo:
            color = 'brown'
        elif 'natural' in modelo:
            color = 'natural'
            
        # Determine Finish
        finish = 'matte' # Default
        if 'pulido' in modelo or 'pulido' in tipologia or 'brillante' in tipologia:
            finish = 'polished'
        elif 'satinado' in modelo or 'satinado' in tipologia:
            finish = 'satin'
        elif 'granillado' in modelo or 'granillado' in tipologia:
            finish = 'textured'
            
        visual_key = f"{material}_{color}_{finish}"
        clusters[visual_key].append(p['Modelo'])

    with open('cluster_analysis.txt', 'w', encoding='utf-8') as f_out:
        f_out.write("\n--- Proposed Visual Clusters ---\n")
        for key, items in clusters.items():
            f_out.write(f"[{key}]: {len(items)} products\n")
            f_out.write(f"   Examples: {', '.join(items[:3])}\n")
    print("Analysis complete. Check cluster_analysis.txt")

if __name__ == "__main__":
    analyze_products('products_new.json')
