from django.shortcuts import render
from .models import VideosDB
from .forms import VideoForm

# Create your views here.

def showvideo(request):

    lastvideo= VideoDB.objects.last()

    videofile= lastvideo.videofile

    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    
    context= {'videofile': videofile,
              'form': form}
      
    return render(request, 'templates/video.html', context)