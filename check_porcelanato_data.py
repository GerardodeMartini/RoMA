
import os
import sys
import django

# Add the project directory to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from projects.models import Porcelanato

items_with_tags_dim = Porcelanato.objects.filter(dimensions__contains='{{')
items_with_tags_desc = Porcelanato.objects.filter(description__contains='{{')

print(f"Items with '{{' in dimensions: {items_with_tags_dim.count()}")
print(f"Items with '{{' in description: {items_with_tags_desc.count()}")

if items_with_tags_dim.exists():
    print("Example dimension:", items_with_tags_dim.first().dimensions)

if items_with_tags_desc.exists():
    print("Example description:", items_with_tags_desc.first().description)
