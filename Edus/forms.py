from django import forms
from .models import EdusDB

class EdusDBForm(forms.ModelForm):
    class Meta:
        model = EdusDB
        fields = ["user_id","video_id", "recode_video"]