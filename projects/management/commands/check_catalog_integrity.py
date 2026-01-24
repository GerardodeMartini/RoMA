
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
            self.stdout.write(f"Ítems con '{{' en dimensiones: {bad_dims.count()}")
            self.stdout.write(f"Ítems con '{{' en descripción: {bad_desc.count()}")
            
            for p in bad_dims:
                self.stdout.write(f"ID {p.id}: Dimensiones='{p.dimensions}'")
        else:
            self.stdout.write(self.style.SUCCESS("Contenido de Base de Datos: OK (No se encontraron etiquetas de plantilla literales)"))

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
