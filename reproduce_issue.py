
import os
import sys
import django
from django.test import Client

# Add the project directory to sys.path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS += ['testserver']

def reproduce():
    c = Client()
    response = c.get('/productos/revestimientos/')
    
    print(f"Status Code: {response.status_code}")
    
    content = response.content.decode('utf-8')
    
    if "{{ p.dimensions }}" in content:
        print("FAIL: Found literal '{{ p.dimensions }}' in response.")
        # Print context to see where it is
        index = content.find("{{ p.dimensions }}")
        snippet = content[max(0, index-100):min(len(content), index+100)]
        print(f"Snippet:\n{snippet}")
    else:
        print("SUCCESS: Did not find literal '{{ p.dimensions }}' in response.")
        
    if "{{ p.description }}" in content:
        print("FAIL: Found literal '{{ p.description }}' in response.")
    
    # Also print the first product card's rendered HTML to be sure
    if "product-card" in content:
        print("\n--- Sample Product Card HTML ---")
        start = content.find('<div class="product-card">')
        end = content.find('</div>', start + 100) # approximate end
        print(content[start:end+200]) # Print a chunk

if __name__ == "__main__":
    reproduce()
