import os
import django
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

client = Client()

# Login as admin
try:
    admin_user = User.objects.get(username='admin')
    client.force_login(admin_user)
    print("Logged in as admin.")
except User.DoesNotExist:
    print("Admin user not found.")
    exit(1)

# Test Project Admin
try:
    url = reverse('admin:projects_project_changelist')
    response = client.get(url)
    print(f"Project Admin status: {response.status_code}")
except Exception as e:
    print(f"Project Admin Error: {e}")

# Test Porcelanato Admin
try:
    url = reverse('admin:projects_porcelanato_changelist')
    response = client.get(url)
    print(f"Porcelanato Admin status: {response.status_code}")
except Exception as e:
    print(f"Porcelanato Admin Error: {e}")
