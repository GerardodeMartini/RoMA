import os
import shutil
from django.db import migrations
from django.conf import settings

def restore_media_files(apps, schema_editor):
    Porcelanato = apps.get_model('projects', 'Porcelanato')
    
    # Files to restore
    restorations = [
        {"title": "Blanco Mate", "filename": "p56_1.jpeg"},
        {"title": "Blanco Pulido", "filename": "p58_2.jpeg"},
    ]
    
    # Source: Static directory in the repo
    # This path is where git put the files: c:/.../static/img/porcelanatos/
    # On the server, direct path manipulation to MEDIA_ROOT is the way to bypass volume hiding
    
    static_source = os.path.join(settings.BASE_DIR, 'static', 'img', 'porcelanatos')
    media_dest_dir = os.path.join(settings.MEDIA_ROOT, 'porcelanatos')
    
    if not os.path.exists(media_dest_dir):
        os.makedirs(media_dest_dir)
    
    for item in restorations:
        filename = item['filename']
        src_path = os.path.join(static_source, filename)
        dest_path = os.path.join(media_dest_dir, filename)
        
        if os.path.exists(src_path):
            print(f"Restoring {filename} from {src_path} to {dest_path}")
            shutil.copy2(src_path, dest_path)
            
            # Verify file size to ensure it's not empty
            if os.path.getsize(dest_path) > 0:
                print(f"Successfully restored {filename}")
            else:
                print(f"Warning: {filename} was copied but is empty.")
        else:
            print(f"Error: Source file {src_path} not found. Ensure git pull brought the static files.")


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_update_linea_blanca_images'),
    ]

    operations = [
        migrations.RunPython(restore_media_files),
    ]
