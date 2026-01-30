import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from projects.models import Porcelanato

def cleanup():
    # Targets to clean
    targets = [
        {"title": "R40082 Blanco Mate", "correct_image": "porcelanatos/p56_1.jpeg"},
        {"title": "R40002 Blanco Pulido", "correct_image": "porcelanatos/p58_2.jpeg"}
    ]

    for t in targets:
        title = t["title"]
        correct_img = t["correct_image"]
        
        # Find all matches
        items = Porcelanato.objects.filter(title__icontains=title).order_by('-updated_at')
        count = items.count()
        print(f"Found {count} items for '{title}'")
        
        if count > 1:
            kept = False
            for p in items:
                # Normalizing paths for comparison
                p_img = p.image.name.replace('\\', '/')
                
                if not kept and (p_img.endswith(correct_img) or p_img == correct_img):
                    print(f"Keeping ID {p.pk} (Image: {p.image.name})")
                    kept = True
                else:
                    print(f"Deleting duplicate ID {p.pk} (Image: {p.image.name})")
                    p.delete()
            
            # If we didn't find one with the correct image, we might have deleted the last one? 
            # No, 'kept' logic ensures we delete everything if none match? 
            # Improved logic:
            if not kept:
                print("WARNING: No matched image found among duplicates. Check logic.")
                
        elif count == 1:
            print(f"ID {items[0].pk} is unique. Verifying image...")
            # Ensure it has the right image
            p = items[0]
            if p.image.name.replace('\\', '/') != correct_img:
                print(f"Updating image for ID {p.pk} to {correct_img}")
                p.image = correct_img
                p.save()
        else:
            print(f"No items found for {title}")

if __name__ == "__main__":
    cleanup()
