from django.shortcuts import render, get_object_or_404
from .models import Project, Porcelanato, Hormigon, HormigonImage, HormigonVideo
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from .forms import CustomAuthenticationForm
from django.conf import settings

@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='dispatch')
class RateLimitedLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['turnstile_site_key'] = getattr(settings, 'TURNSTILE_SITE_KEY', '')
        return context

def inicio(request):
    # Show last 3 featured projects (or just last 3 created)
    featured_projects = Project.objects.all().order_by('-completion_date')[:3]
    return render(request, 'inicio.html', {'featured_projects': featured_projects})

def porcelanatos(request):
    # Definition of categories to display and their mapping to DB codes
    # Use tuple (DB_CODE, Display Label, HTML ID)
    category_map = [
        ('CEMENTO', 'Cemento', 'cemento', 'linea_cemento.jpeg'),
        ('MADERA', 'Madera', 'madera', 'linea_madera.jpeg'),
        ('MARMOL', 'Mármol', 'marmol', 'linea_marmol.jpeg'),
        ('PIEDRA', 'Urban Stone', 'urban-stone', 'linea_urban_stone.jpeg'),
        ('EXTERIOR', 'Pileta', 'pileta', 'linea_pileta.jpeg'),
        ('INTERIOR', 'Blanca', 'blanca', 'linea_blanca.jpeg'),
        ('OTRO', 'Otros', 'otros', None),
    ]
    
    grouped_products = []
    
    for db_code, label, html_id, cover_image in category_map:
        items = Porcelanato.objects.filter(category=db_code)
        if items.exists():
            grouped_products.append({
                'label': label,
                'id': html_id,
                'items': items,
                'cover_image': cover_image
            })
            
    return render(request, 'porcelanatos.html', {'grouped_products': grouped_products})

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

from django.contrib.auth.decorators import login_required

@login_required
def edicion(request):
    return render(request, 'projects/edicion.html')

from .models import Project, Porcelanato, ProjectImage, ProjectVideo, PorcelanatoImage, PorcelanatoVideo, Hormigon, HormigonImage, HormigonVideo
from .forms import ProjectForm, PorcelanatoForm, HormigonForm
from django.shortcuts import redirect

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            for f in request.FILES.getlist('extra_images'):
                ProjectImage.objects.create(project=project, image=f)
            for f in request.FILES.getlist('extra_images'):
                ProjectImage.objects.create(project=project, image=f)
            
            # Process video URLs handled by generic CharField in form (not bound to model directly)
            video_urls_raw = form.cleaned_data.get('video_urls')
            if video_urls_raw:
                urls = [url.strip() for url in video_urls_raw.splitlines() if url.strip()]
                for url in urls:
                    ProjectVideo.objects.create(project=project, video_url=url, title="Video")
            return redirect('edicion')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Agregar Proyecto'})

@login_required
def manage_projects(request):
    projects = Project.objects.all().order_by('-completion_date')
    return render(request, 'projects/manage_projects.html', {'projects': projects})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            # Handle new uploads
            for f in request.FILES.getlist('extra_images'):
                ProjectImage.objects.create(project=project, image=f)
            for f in request.FILES.getlist('extra_images'):
                ProjectImage.objects.create(project=project, image=f)
            
            # Process video URLs
            video_urls_raw = form.cleaned_data.get('video_urls')
            if video_urls_raw:
                urls = [url.strip() for url in video_urls_raw.splitlines() if url.strip()]
                for url in urls:
                    ProjectVideo.objects.create(project=project, video_url=url, title="Video")
            # Handle deletions
            for image_id in request.POST.getlist('delete_images'):
                ProjectImage.objects.filter(id=image_id).delete()
            for video_id in request.POST.getlist('delete_videos'):
                ProjectVideo.objects.filter(id=video_id).delete()
                
            return redirect('manage_projects')
    else:
        form = ProjectForm(instance=project)
    
    # Pass existing media to template
    existing_images = project.images.all()
    existing_videos = project.videos.all()
    
    return render(request, 'projects/project_form.html', {
        'form': form, 
        'title': 'Editar Proyecto',
        'existing_images': existing_images,
        'existing_videos': existing_videos
    })


@login_required
def add_porcelanato(request):
    if request.method == 'POST':
        form = PorcelanatoForm(request.POST, request.FILES)
        if form.is_valid():
            porcelanato = form.save()
            for f in request.FILES.getlist('extra_images'):
                PorcelanatoImage.objects.create(porcelanato=porcelanato, image=f)
            return redirect('edicion')
    else:
        form = PorcelanatoForm()
    return render(request, 'projects/porcelanato_form.html', {'form': form, 'title': 'Agregar Porcelanato'})

@login_required
def manage_porcelanatos(request):
    porcelanatos = Porcelanato.objects.all().order_by('-created_at')
    return render(request, 'projects/manage_porcelanatos.html', {'porcelanatos': porcelanatos})

@login_required
def edit_porcelanato(request, pk):
    porcelanato = get_object_or_404(Porcelanato, pk=pk)
    if request.method == 'POST':
        form = PorcelanatoForm(request.POST, request.FILES, instance=porcelanato)
        if form.is_valid():
            form.save()
            # Handle new uploads
            for f in request.FILES.getlist('extra_images'):
                PorcelanatoImage.objects.create(porcelanato=porcelanato, image=f)
            # Handle deletions
            for image_id in request.POST.getlist('delete_images'):
                PorcelanatoImage.objects.filter(id=image_id).delete()

            return redirect('manage_porcelanatos')
    else:
        form = PorcelanatoForm(instance=porcelanato)
    
    existing_images = porcelanato.images.all()
        
    return render(request, 'projects/porcelanato_form.html', {
        'form': form, 
        'title': 'Editar Porcelanato',
        'existing_images': existing_images
    })


@login_required
def delete_porcelanato(request, pk):
    porcelanato = get_object_or_404(Porcelanato, pk=pk)
    if request.method == 'POST':
        porcelanato.delete()
        return redirect('manage_porcelanatos')
    return render(request, 'projects/confirm_delete.html', {'object': porcelanato, 'cancel_url': 'manage_porcelanatos'})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('manage_projects')
    return render(request, 'projects/confirm_delete.html', {'object': project, 'cancel_url': 'manage_projects'})

def productos_hub(request):
    return render(request, 'products_hub.html')

def productos_hormigon(request):
    products = Hormigon.objects.all().order_by('-created_at')
    return render(request, 'products_hormigon.html', {'products': products})

@login_required
def manage_hormigones(request):
    hormigones = Hormigon.objects.all().order_by('-created_at')
    return render(request, 'projects/manage_hormigon.html', {'hormigones': hormigones})

@login_required
def add_hormigon(request):
    if request.method == 'POST':
        form = HormigonForm(request.POST, request.FILES)
        if form.is_valid():
            hormigon = form.save()
            images = request.FILES.getlist('extra_images')
            for image in images:
                HormigonImage.objects.create(hormigon=hormigon, image=image)
            return redirect('manage_hormigones')
    else:
        form = HormigonForm()
    return render(request, 'projects/hormigon_form.html', {'form': form, 'title': 'Nuevo Prefabricado'})

@login_required
def edit_hormigon(request, pk):
    hormigon = get_object_or_404(Hormigon, pk=pk)
    if request.method == 'POST':
        form = HormigonForm(request.POST, request.FILES, instance=hormigon)
        if form.is_valid():
            hormigon = form.save()
            
            # Handle extra images
            images = request.FILES.getlist('extra_images')
            for image in images:
                HormigonImage.objects.create(hormigon=hormigon, image=image)
            
            # Handle deletion of existing images
            delete_images = request.POST.getlist('delete_images')
            for img_id in delete_images:
                HormigonImage.objects.filter(pk=img_id, hormigon=hormigon).delete()

            return redirect('manage_hormigones')
    else:
        form = HormigonForm(instance=hormigon)
    
    existing_images = hormigon.images.all()
    return render(request, 'projects/hormigon_form.html', {
        'form': form, 
        'title': 'Editar Prefabricado',
        'existing_images': existing_images
    })

@login_required
def delete_hormigon(request, pk):
    hormigon = get_object_or_404(Hormigon, pk=pk)
    if request.method == 'POST':
        hormigon.delete()
        return redirect('manage_hormigones')
    return render(request, 'projects/confirm_delete.html', {'object': hormigon, 'cancel_url': 'manage_hormigones'})
