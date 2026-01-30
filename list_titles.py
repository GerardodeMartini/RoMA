import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from projects.models import Porcelanato

def list_titles():
    products = Porcelanato.objects.all().values_list('title', flat=True)
    print("Porcelanato Titles:")
    for t in products:
        print(f"- {t}")

if __name__ == "__main__":
    list_titles()
