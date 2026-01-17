from django.shortcuts import render, get_object_or_404
from .models import Project

def inicio(request):
    # Show last 3 featured projects (or just last 3 created)
    featured_projects = Project.objects.all().order_by('-completion_date')[:3]
    return render(request, 'inicio.html', {'featured_projects': featured_projects})

def project_list(request):
    category = request.GET.get('category')
    if category:
        projects = Project.objects.filter(category=category)
    else:
        projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})
