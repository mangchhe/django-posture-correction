from django import forms
from .models import VideosDB
from bootstrap_modal_forms.forms import BSModalForm
# VideosDB 데이터베이스 테이블을 기반으로 한 양식
class VideoForm(forms.ModelForm):
    class Meta:
        model= VideosDB
        fields= ["title", "videofile", "video_img", "level"]

class VideoDBForm(BSModalForm):
    class Meta:
        model = VideosDB
        fields = ['videofile']
