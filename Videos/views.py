#-*- coding: utf-8 -*-
from django.shortcuts import render
from .models import VideosDB
from .forms import VideoForm
from Users.models import UsersDB
from Edus.models import EdusDB
from django.db.models import Sum, Subquery, OuterRef
import math

# Create your views here.

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
    if total_page > 1:
        page_range = range(1, total_page+1)
    else:
        page_range = None
    start_index = paginated_by * (page-1)
    end_index = paginated_by * page

    qs = qs[start_index:end_index]

    return render(request, 'search.html', {'search' : qs, 'q' : q, 'where':where, 'page_range':page_range, 'le':le,})

def main(request):

    pop = VideosDB.objects.all().order_by('-views')
    late = VideosDB.objects.all().order_by('start_date')

    pop = pop[0:4]
    late = late[0:4]

    # 이용자 순위 (총 점수 합계순으로 출력)
    Edus_list = EdusDB.objects.values('user_id__username').annotate(Sum('score')).order_by('-score__sum')
    # 인기 채널 순위 (영상 조회수가 높은 게시자 순으로 출력)
    channel = VideosDB.objects.values('editor__username').annotate(Sum('views')).order_by('-views__sum')
    print(channel)
    return render(request, 'main.html', {'pop' : pop, 'late' : late,'user':Edus_list,'channel':channel})


def VideoShow(request, video_id):
    result = VideosDB.objects.filter(id=video_id)
    print(result)
    return render(request, 'VideoShowModal.html', {'result':result})
