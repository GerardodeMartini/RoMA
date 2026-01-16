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
