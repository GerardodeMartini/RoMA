import os
import django
from django.core.files import File
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from projects.models import Project, ProjectImage

def populate():
    # Create a general project for the extracted images
    project, created = Project.objects.get_or_create(
        title="Obras y Trabajos Recientes",
        defaults={
            'description': "Compilación de imágenes extraídas de la presentación institucional.",
            'category': 'CIVIL',
            'client': 'Varios'
        }
    )
    
    if created:
        print(f"Created Project: {project.title}")
    else:
        print(f"Found Project: {project.title}")

    # Path to extracted images
    extracted_dir = os.path.join(settings.BASE_DIR, 'static', 'img', 'extracted')
    
    if not os.path.exists(extracted_dir):
        print("No extracted images found.")
        return

    count = 0
    for filename in os.listdir(extracted_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(extracted_dir, filename)
            
            # Open the file
            with open(file_path, 'rb') as f:
                # Create ProjectImage
                # Check if image already exists to avoid duplicates (naive check)
                if not ProjectImage.objects.filter(project=project, caption=filename).exists():
                    img_instance = ProjectImage(project=project, caption=filename)
                    img_instance.image.save(filename, File(f), save=True)
                    print(f"Added image: {filename}")
                    count += 1
                else:
                    print(f"Skipped duplicate: {filename}")
    
    # Set the first image as main_image for the project if not set
    if not project.main_image and project.images.exists():
        first_img = project.images.first()
        # We need to copy it or just duplicate the file for the main_image field
        # For simplicity, we just leave it or you can manually set it.
        # Actually, let's set it.
        project.main_image = first_img.image
        project.save()
        print("Set main project image.")

    print(f"Successfully added {count} images to '{project.title}'")

if __name__ == '__main__':
    populate()
