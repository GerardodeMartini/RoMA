from django.contrib import admin
from .models import Project, ProjectImage, ProjectVideo, AuditLog

admin.site.register(Project)
# admin.site.register(Porcelanato)
admin.site.register(ProjectImage)
admin.site.register(ProjectVideo)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'user__email', 'ip_address')
    readonly_fields = ('user', 'action', 'timestamp', 'ip_address')
    
    def has_add_permission(self, request):
        return False
