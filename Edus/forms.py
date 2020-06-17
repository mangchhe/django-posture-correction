from django import forms
from .models import EdusDB

class EdusDBForm(forms.ModelForm):
    class Meta:
        model = EdusDB

        widgets = {
            'video_description': forms.Textarea(attrs={'rows':1}),
        }

        fields = ["video_description", "is_shared"]
