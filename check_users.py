import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
print(f"Users count: {User.objects.count()}")
if User.objects.count() > 0:
    print(f"Usernames: {[u.username for u in User.objects.all()]}")
else:
    print("No users found.")
