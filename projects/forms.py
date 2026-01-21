from django import forms
from .models import Project, Porcelanato, Hormigon

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
    extra_videos = MultipleFileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'accept': 'video/*'}), 
        required=False, 
        label="Videos Adicionales (Seleccionar varias)"
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
