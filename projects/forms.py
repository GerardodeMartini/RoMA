from django import forms
from django.contrib.auth.forms import AuthenticationForm
import requests
from django.conf import settings
from .models import Project, Porcelanato, Hormigon

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        turnstile_token = self.request.POST.get('cf-turnstile-response')
        
        if not turnstile_token:
            raise forms.ValidationError("Por favor, completa el CAPTCHA.")
            
        # Verify token with Cloudflare
        secret_key = getattr(settings, 'TURNSTILE_SECRET_KEY', None)
        if secret_key:
            response = requests.post(
                'https://challenges.cloudflare.com/turnstile/v0/siteverify',
                data={
                    'secret': secret_key,
                    'response': turnstile_token,
                    'remoteip': self.request.META.get('REMOTE_ADDR')
                }
            )
            result = response.json()
            if not result.get('success'):
                raise forms.ValidationError("Error de validación del CAPTCHA. Intenta nuevamente.")
        
        return cleaned_data

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def to_python(self, data):
        if not data:
            return None
        if not isinstance(data, list):
            if hasattr(data, 'read'): # It's a single file
                return [data]
            return None
        return data

    def clean(self, data, initial=None):
        # Prevent FileField's clean from blowing up on a list
        if not data and self.required:
             raise forms.ValidationError(self.error_messages['required'], code='required')
        return data

class ProjectForm(forms.ModelForm):
    main_image = forms.ImageField(
        label="Imagen Principal",
        error_messages={'required': "Por favor, carga una imagen principal para el proyecto."},
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'})
    )
    extra_images = MultipleFileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'accept': 'image/*'}), 
        required=False, 
        label="Imágenes Adicionales (Seleccionar varias)"
    )
    video_urls = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Pegar enlaces de YouTube aquí (uno por línea)'}), 
        required=False, 
        label="Videos de YouTube (Uno por línea)",
        help_text="Ingrese solo enlaces de YouTube válidos."
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'client', 'completion_date', 'main_image']
        widgets = {
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class PorcelanatoForm(forms.ModelForm):
    image = forms.ImageField(
        label="Imagen Principal", 
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'})
    )
    extra_images = MultipleFileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'accept': 'image/*'}), 
        required=False, 
        label="Imágenes Adicionales (Seleccionar varias)"
    )
    # extra_videos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, label="Videos Adicionales")

    class Meta:
        model = Porcelanato
        fields = ['title', 'description', 'category', 'dimensions', 'price', 'm2_per_box', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class HormigonForm(forms.ModelForm):
    image = forms.ImageField(
        label="Imagen Principal",
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'})
    )
    extra_images = MultipleFileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'accept': 'image/*'}),
        required=False,
        label="Imágenes Adicionales (Seleccionar varias)"
    )
    # extra_videos logic can be added similarly if needed

    class Meta:
        model = Hormigon
        fields = ['title', 'description', 'dimensions', 'price', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
