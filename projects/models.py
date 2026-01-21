from django.db import models

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('CIVIL', 'Ingeniería Civil'),
        ('INDUSTRIAL', 'Ingeniería Industrial'),
        ('OTHER', 'Otros'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título del Proyecto")
    description = models.TextField(verbose_name="Descripción")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='CIVIL', verbose_name="Categoría")
    client = models.CharField(max_length=200, blank=True, null=True, verbose_name="Cliente")
    completion_date = models.DateField(blank=True, null=True, verbose_name="Fecha de Finalización")
    main_image = models.ImageField(upload_to='projects/main/', verbose_name="Imagen Principal")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['-completion_date', '-created_at']

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/', verbose_name="Imagen")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Leyenda")

    def __str__(self):
        return f"Imagen de {self.project.title}"

class ProjectVideo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='projects/videos/', blank=True, null=True, verbose_name="Archivo de Video")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL de Video (YouTube/Vimeo)")
    title = models.CharField(max_length=200, blank=True, verbose_name="Título del Video")

    def __str__(self):
        return f"Video de {self.project.title}"

class Porcelanato(models.Model):
    CATEGORY_CHOICES = [
        ('INTERIOR', 'Interior'),
        ('EXTERIOR', 'Exterior'),
        ('MADERA', 'Símil Madera'),
        ('CEMENTO', 'Símil Cemento'),
        ('PIEDRA', 'Símil Piedra'),
        ('MARMOL', 'Símil Mármol'),
        ('OTRO', 'Otros'),
    ]

    title = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción/Características", blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='INTERIOR', verbose_name="Categoría")
    dimensions = models.CharField(max_length=50, verbose_name="Dimensiones (ej. 60x60)", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio por m²")
    m2_per_box = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="M² por Caja")
    image = models.ImageField(upload_to='porcelanatos/', verbose_name="Imagen")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Porcelanato"
        verbose_name_plural = "Porcelanatos"
        ordering = ['-created_at']

class PorcelanatoImage(models.Model):
    porcelanato = models.ForeignKey(Porcelanato, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='porcelanatos/gallery/', verbose_name="Imagen Adicional")
    
    def __str__(self):
        return f"Imagen de {self.porcelanato.title}"

class PorcelanatoVideo(models.Model):
    porcelanato = models.ForeignKey(Porcelanato, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='porcelanatos/videos/', blank=True, null=True, verbose_name="Archivo de Video")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL de Video (YouTube/Vimeo)")
    title = models.CharField(max_length=200, blank=True, verbose_name="Título del Video")

    def __str__(self):
        return f"Video de {self.porcelanato.title}"

class Hormigon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción", blank=True)
    dimensions = models.CharField(max_length=100, verbose_name="Medidas", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio")
    image = models.ImageField(upload_to='hormigon/', verbose_name="Imagen Principal")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Prefabricado de Hormigón"
        verbose_name_plural = "Prefabricados de Hormigón"
        ordering = ['-created_at']

class HormigonImage(models.Model):
    hormigon = models.ForeignKey(Hormigon, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hormigon/gallery/', verbose_name="Imagen Adicional")

    def __str__(self):
        return f"Imagen de {self.hormigon.title}"

class HormigonVideo(models.Model):
    hormigon = models.ForeignKey(Hormigon, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='hormigon/videos/', blank=True, null=True, verbose_name="Archivo de Video")
    video_url = models.URLField(blank=True, null=True, verbose_name="URL de Video (YouTube/Vimeo)")
    title = models.CharField(max_length=200, blank=True, verbose_name="Título del Video")

    def __str__(self):
        return f"Video de {self.hormigon.title}"


# Audit Log
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuario")
    action = models.CharField(max_length=255, verbose_name="Acción")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dirección IP")

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"

    class Meta:
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ['-timestamp']

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditLog.objects.create(
        user=user,
        action="Inicio de sesión",
        ip_address=ip
    )

