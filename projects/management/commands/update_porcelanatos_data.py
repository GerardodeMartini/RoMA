
import json
import os
from django.core.management.base import BaseCommand
from projects.models import Porcelanato

class Command(BaseCommand):
    help = 'Updates Porcelanato fields (Brand, Typology, Usage, etc.) from products_manual.json'

    def handle(self, *args, **options):
        json_path = "products_manual.json"
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"File {json_path} not found!"))
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        updated_count = 0
        not_found_count = 0

        for item in data:
            title = item.get('Modelo')
            # Try to match by title
            # In generate_manual, title was set to "Modelo"
            
            try:
                p = Porcelanato.objects.get(title=title)
                
                # Update fields
                p.brand = item.get('Marca', '')
                p.typology = item.get('Tipologia', '')
                p.rectified = item.get('Rectificado', '')
                p.usage = item.get('Uso', '')
                
                # Ensure dimensions is set if empty
                if not p.dimensions and item.get('Formato'):
                    p.dimensions = item.get('Formato')
                    
                # Ensure m2_per_box is set 
                if item.get('M2_Caja'):
                     p.m2_per_box = item.get('M2_Caja')
                
                p.save()
                updated_count += 1
                # self.stdout.write(f"Updated: {title}")
                
            except Porcelanato.DoesNotExist:
                # self.stdout.write(self.style.WARNING(f"Product not found in DB: {title}"))
                not_found_count += 1
            except Porcelanato.MultipleObjectsReturned:
                self.stdout.write(self.style.ERROR(f"Multiple products found for: {title}"))

        self.stdout.write(self.style.SUCCESS(f"Finished. Updated: {updated_count}. Not Found/Skipped: {not_found_count}"))
