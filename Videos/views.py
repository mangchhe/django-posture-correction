from django.shortcuts import render
from .models import VideosDB
from .forms import VideoForm

# Create your views here.

# 만든 ModelForm을 가져 와서 렌더링하고있는 템플릿 파일을 통해 전달
def showvideo(request):

    lastvideo= VideosDB.objects.last() # 데이터베이스 테이블에서 마지막 비디오(객체)인 변수 lastvideo를 생성

    videofile= lastvideo.videofile.url # 비디오 파일 경로를 포함하는 변수 videofile을 생성

    form= VideoForm(request.POST or None, request.FILES or None) # request.POST 또는 None은 사용자가 양식을 제출 한 후 데이터를 필드에 유지
    if form.is_valid():
        form.save()
    
    context= {'videofile': videofile,
              'form': form}
      
    return render(request, 'video.html', context) # context 사전으로 전달되는 템플릿 videos.html을 렌더링