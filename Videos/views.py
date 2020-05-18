from django.shortcuts import render
from .models import VideosDB
from .forms import VideoForm
from Users.models import UsersDB
from Edus.models import EdusDB

import math

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

def search(request):
    
    where = request.GET.get('where',None)

    if where == 'pop':
        qs = VideosDB.objects.all().order_by('-views')
    elif where == 'last':
        qs = VideosDB.objects.all().order_by('start_date')
    else:
        qs = VideosDB.objects.all()

    page = int(request.GET.get('page',1))
    paginated_by = 1


    q = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    le = request.GET.getlist('le','')
    llist = ['상', '중', '하']
    nole = []
    if le:
        for x in llist:
            if str(x) not in le:
                nole.append(x)

        for x in nole:
            qs = qs.exclude(level=x)
    
    if q: # q가 있으면
        qs = qs.filter(title__icontains=q) # 제목에 q가 포함되어 있는 레코드만 필터링
    
    total_count = len(qs)
    total_page = math.ceil(total_count/paginated_by)
    page_range = range(1, total_page+1)
    start_index = paginated_by * (page-1)
    end_index = paginated_by * page

    qs = qs[start_index:end_index]

    return render(request, 'search.html', {'search' : qs, 'q' : q, 'where':where, 'page_range':page_range, 'le':le})

def main(request):

    pop = VideosDB.objects.all().order_by('-views')
    late = VideosDB.objects.all().order_by('start_date')
    #user = UsersDB.objects.prefetch_related('id')
    user = EdusDB.objects.order_by('score')
    pop = pop[0:4]
    late = late[0:4]

    return render(request, 'main.html', {'pop' : pop, 'late' : late,'user':user,})


  
