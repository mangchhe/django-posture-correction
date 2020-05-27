from django import forms
from .models import EdusDB
from bootstrap_modal_forms.forms import BSModalForm

class EdusDBForm(forms.ModelForm):
    class Meta:
        model = EdusDB
        fields = ["user_id","video_id", "recode_video"]

class EdusDBForms(BSModalForm):
    class Meta:
        model = EdusDB
        fields = ['recode_video']
