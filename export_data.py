import os
import django
from django.core.management import call_command
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

output_file = 'datadump.json'

print(f"Exporting data to {output_file} with UTF-8 encoding...")

with open(output_file, 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'projects', indent=2, stdout=f)

print("Export complete.")
