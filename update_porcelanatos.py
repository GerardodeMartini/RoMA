import os
import shutil
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from projects.models import Porcelanato

def update_porcelanatos():
    # Updates mapping: Title Key -> {Filename, FullTitle, Description, etc}
    updates = {
        "Blanco Mate": {
            "filename": "p56_1.jpeg",
            "full_title": "R40082 Blanco Mate",
            "category": "INTERIOR", # Mapped from BLANCA in manual json? No, views.py maps INTERIOR to Blanca
            "brand": "Rochaforte",
            "dimensions": "40x75 cm",
            "price": 13520,
            "m2_per_box": 3.00,
            "typology": "Mate",
            "rectified": "Si",
            "usage": "LA"
        },
        "Blanco Pulido": {
            "filename": "p58_2.jpeg",
            "full_title": "R40002 Blanco Pulido",
            "category": "INTERIOR",
            "brand": "Rochaforte",
            "dimensions": "40x75 cm",
            "price": 17900,
            "m2_per_box": 3.00,
            "typology": "Pulido",
            "rectified": "Si",
            "usage": "LC"
        }
    }

    base_static = os.path.join(settings.BASE_DIR, 'static', 'img', 'porcelanatos')
    base_media = os.path.join(settings.MEDIA_ROOT, 'porcelanatos')
    
    if not os.path.exists(base_media):
        os.makedirs(base_media)

    for key, data in updates.items():
        filename = data['filename']
        
        # 1. Copy file
        src = os.path.join(base_static, filename)
        dst = os.path.join(base_media, filename)
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {filename} to media.")
        else:
            print(f"WARNING: Source file {src} not found. Assuming it might exist in media already.")
            
        # 2. Update or Create DB
        # Try to find by title substring or full title
        obj = Porcelanato.objects.filter(title__icontains=key).first()
        
        if not obj:
            print(f"Creating new product: {data['full_title']}")
            obj = Porcelanato(title=data['full_title'])
        else:
            print(f"Updating existing product: {obj.title}")
            
        # Update fields
        obj.title = data['full_title'] # Enforce full title
        obj.image = f'porcelanatos/{filename}'
        obj.category = data['category']
        obj.brand = data['brand']
        obj.dimensions = data['dimensions']
        obj.price = data['price']
        obj.m2_per_box = data['m2_per_box']
        obj.typology = data['typology']
        obj.rectified = data['rectified']
        obj.usage = data['usage']
        
        obj.save()
        print(f"Saved {obj.title} with image {obj.image}")

if __name__ == "__main__":
    update_porcelanatos()
