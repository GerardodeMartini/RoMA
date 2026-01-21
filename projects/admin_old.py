from django.contrib import admin
from .models import Project, ProjectImage, ProjectVideo, Porcelanato

# @admin.register(Porcelanato)
# class PorcelanatoAdmin(admin.ModelAdmin):
#     pass

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class ProjectVideoInline(admin.TabularInline):
    model = ProjectVideo
    extra = 1

# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     pass
    # list_display = ('title', 'category', 'client', 'completion_date')
    # list_filter = ('category', 'completion_date')
    # search_fields = ('title', 'description', 'client')
    # inlines = [ProjectImageInline, ProjectVideoInline]

admin.site.register(Project)
# admin.site.register(ProjectImage)
# admin.site.register(ProjectVideo)

