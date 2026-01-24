
from django.core.management.base import BaseCommand
from projects.models import Porcelanato
import os
import hashlib

class Command(BaseCommand):
    help = 'Verifica problemas de integridad de datos en el catálogo de Porcelanatos'

    def handle(self, *args, **options):
        self.stdout.write("Verificando integridad de datos de Porcelanatos...")
        
        # Check for literal template tags in data
        bad_dims = Porcelanato.objects.filter(dimensions__contains='{{')
        bad_desc = Porcelanato.objects.filter(description__contains='{{')
        
        if bad_dims.exists() or bad_desc.exists():
            self.stdout.write(self.style.ERROR(f"¡CORRUPCIÓN ENCONTRADA!"))
            # ... (keep existing code for corruption) ...
        
        # New Check: Empty Data
        empty_dims = Porcelanato.objects.filter(dimensions__exact='')
        total_items = Porcelanato.objects.count()
        
        self.stdout.write(f"\nVerificando campos vacíos (Total ítems: {total_items}):")
        self.stdout.write(f"- Dimensiones vacías: {empty_dims.count()}")
        
        if empty_dims.count() == total_items and total_items > 0:
             self.stdout.write(self.style.ERROR("¡TODOS los productos tienen las dimensiones vacías!"))
             self.stdout.write("Probable causa: La importación de datos no mapeó el campo 'Formato' a 'dimensions'.")
        elif empty_dims.exists():
             self.stdout.write(self.style.WARNING(f"Alerta: {empty_dims.count()} productos no tienen dimensiones."))

        # Check a sample
        if total_items > 0:
            sample = Porcelanato.objects.first()
            self.stdout.write(f"\nMuestra (ID {sample.id}):")
            self.stdout.write(f"  Título: {sample.title}")
            self.stdout.write(f"  Dimensiones (Formato): '{sample.dimensions}'")
            self.stdout.write(f"  M2 por Caja: '{sample.m2_per_box}'")


        # Check template file existence
        template_path = os.path.join(os.getcwd(), 'templates', 'porcelanatos.html')
        if os.path.exists(template_path):
            self.stdout.write(f"Plantilla encontrada en: {template_path}")
            # Calculate hash
            with open(template_path, 'rb') as f:
                content = f.read()
                md5 = hashlib.md5(content).hexdigest()
            self.stdout.write(f"MD5 de Plantilla: {md5}")
            
            # Check for hardcoded {{ p.dimensions }} outside of django tags?
            # It's hard to parse regex for this but if the file is static HTML, it might have it.
            if b'{{ p.dimensions }}' in content and b'{% for' not in content:
                 self.stdout.write(self.style.WARNING("¡La plantilla podría ser HTML estático con marcadores de posición! (No se encontró bucle {% for %})"))
        else:
            self.stdout.write(self.style.ERROR("templates/porcelanatos.html NO ENCONTRADO"))
