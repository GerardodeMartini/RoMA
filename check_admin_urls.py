import os
import django
from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

try:
    print(f"Project Admin URL: {reverse('admin:projects_project_changelist')}")
    print(f"Porcelanato Admin URL: {reverse('admin:projects_porcelanato_changelist')}")
except Exception as e:
    print(f"Error reversing URLs: {e}")
