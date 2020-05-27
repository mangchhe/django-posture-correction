from django import forms
from .models import EdusDB
from bootstrap_modal_forms.forms import BSModalForm

class EdusDBForm(BSModalForm):
    class Meta:
        model = EdusDB
        fields = ['recode_video']