from django.db import migrations

def update_porcelanatos(apps, schema_editor):
    Porcelanato = apps.get_model('projects', 'Porcelanato')
    
    updates = [
        {
            "match_title": "Blanco Mate",
            "full_title": "R40082 Blanco Mate",
            "image": "porcelanatos/p56_1.jpeg",
            "category": "INTERIOR",
            "brand": "Rochaforte",
            "dimensions": "40x75 cm",
            "price": 13520,
            "m2_per_box": 3.00,
            "typology": "Mate",
            "rectified": "Si",
            "usage": "LA"
        },
        {
            "match_title": "Blanco Pulido",
            "full_title": "R40002 Blanco Pulido",
            "image": "porcelanatos/p58_2.jpeg",
            "category": "INTERIOR",
            "brand": "Rochaforte",
            "dimensions": "40x75 cm",
            "price": 17900,
            "m2_per_box": 3.00,
            "typology": "Pulido",
            "rectified": "Si",
            "usage": "LC"
        }
    ]

    for data in updates:
        # Try finding by full title first, then substring
        obj = Porcelanato.objects.filter(title=data['full_title']).first()
        if not obj:
            obj = Porcelanato.objects.filter(title__icontains=data['match_title']).first()
        
        if not obj:
            # Create if doesn't exist
            obj = Porcelanato(title=data['full_title'])
        
        obj.title = data['full_title']
        obj.image = data['image']
        obj.category = data['category']
        obj.brand = data['brand']
        obj.dimensions = data['dimensions']
        obj.price = data['price']
        obj.m2_per_box = data['m2_per_box']
        obj.typology = data['typology']
        obj.rectified = data['rectified']
        obj.usage = data['usage']
        obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_auditlog_user'),
    ]

    operations = [
        migrations.RunPython(update_porcelanatos),
    ]
