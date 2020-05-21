from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import StreamingHttpResponse
from Edus.camera import VideoCamera
from .models import EdusDB
from Users.models import UsersDB
from Videos.models import VideosDB
from django.core.paginator import Paginator
import datetime
from PostureCorrectionGameSite import settings
from mutagen.mp4 import MP4
from django.db.models import Sum
from Videos.forms import VideoForm
from Videos.models import VideosDB

# Create your views here.

# 모드 선택 후 화면

def play(request, page_no):

	# 비디오 정보 (mp4, avi 등)

	VIDEO_NAME = 'cat'

	videoName = 'videos/' + VIDEO_NAME + '.mp4'

	videoLength = MP4(settings.MEDIA_ROOT + 'videos/' + VIDEO_NAME + '.mp4').info.length + .5

	edu = EdusDB.objects.filter(video_id = 1, user_id = 1).order_by('-edu_days') # 해당 영상과, 사용자 주

	eduList = Paginator(edu, 4)

	idx = []
	days = []
	video = []

	totalPageList = [i for i in range(1, eduList.num_pages + 1)]
	currentPage = page_no

	for i, j in enumerate(eduList.get_page(page_no).object_list.values()):

		idx.append((page_no-1) * 4 + i+1)
		video.append(j['recode_video'])
		days.append(j['edu_days'])

	context = {
		'videoList' : zip(idx, video, days),
		'totalPageList' : totalPageList,
		'currentPage' : currentPage,
		'videoLength' : videoLength,
		'videoName' : videoName,
	}

	if request.method == 'POST':
		new_video = EdusDB.objects.create(
			# edu_days = 현재 시간 자동 저장
			video_id=VideosDB.objects.all()[0],
			user_id=UsersDB.objects.all()[0],
			recode_video='test',
			score=99
		)
	
	return render(request, 'playView.html', context)

def play_after(request, page_no):

	# 비디오 정보 (mp4, avi 등)

	# after

	rankList = ['A+', 'A0', 'B+', 'B0', 'C+', 'C0', 'D+', 'D0', 'F']
	zum = 90
	rank = 'F'
	nowDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	for idx, val in enumerate(rankList):

		if zum >= 95 - idx * 5:

			rank = rankList[idx]
			break

	# before

	edu = EdusDB.objects.filter(video_id = 1, user_id = 1).order_by('-edu_days') # 해당 영상과, 사용자 주

	eduList = Paginator(edu, 4)

	idx = []
	days = []
	video = []

	totalPageList = [i for i in range(1, eduList.num_pages + 1)]
	currentPage = page_no

	for i, j in enumerate(eduList.get_page(page_no).object_list.values()):

		idx.append((page_no-1) * 4 + i+1)
		video.append(j['recode_video'])
		days.append(j['edu_days'])

	context = {
		'videoList' : zip(idx, video, days),
		'totalPageList' : totalPageList,
		'currentPage' : currentPage,
		'result' : str(zum)+' , '+str(rank)+' , '+str(nowDate),
	}

	if request.method == 'POST':
		new_video = EdusDB.objects.create(
			# edu_days = 현재 시간 자동 저장
			video_id=VideosDB.objects.all()[0],
			user_id=UsersDB.objects.all()[0],
			recode_video='test',
			score=99
		)

	return render(request, 'playViewResult.html', context)

def gen(camera): # https://item4.blog/2016-05-08/Generator-and-Yield-Keyword-in-Python/
# 앨범 이미지
	while True:
		
		frame = camera.get_frame()

		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
# 웹캠 정보
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame') # 찾아보기

# 마이페이지


def mypage(request):
	
	return render(request, 'mypageView.html')

	
def post_list(request):
	""" 비디오 업로드 """
	print(request.user.id)
	lastvideo= VideosDB.objects.last() # 데이터베이스 테이블에서 마지막 비디오(객체)인 변수 lastvideo를 생성
	
	videofile= lastvideo.videofile.url # 비디오 파일 경로를 포함하는 변수 videofile을 생성
	
	form= VideoForm(request.POST or None, request.FILES or None) # request.POST 또는 None은 사용자가 양식을 제출 한 후 데이터를 필드에 유지
	
	if form.is_valid():
		form.save()
	
	""" 업로드 된 영상 및 나의 점수 """
	Edus_list = EdusDB.objects.all() # Edus 테이블의 전체 데이터 가져오기 -> 로그인이랑 회원가입 만들어지면 queryset 다시 작성 예정
	s_sum = EdusDB.objects.aggregate(Sum('score'))['score__sum'] # Edus 테이블의 전체 score 값 더하기 -> 로그인이랑 회원가입 만들어지면 queryset 다시 작성 예정

	# mypageView로 넘길 데이터
	context= {'videofile': videofile,
              'form': form,
			  'score_sum': s_sum,
              'Edus_list' : Edus_list}
	return render(request, 'mypageView.html', context)

def ResultVideosList(request):
    ResultVideos = EdusDB.objects.all()
    return render(request, 'ResultVideosList.html', {'ResultVideos': ResultVideos})

def create(request):
    form = EdusDBForm()
    context = {'form': form}
    html_form = render_to_string('create.html', context, request=request,)
    return JsonResponse({'html_form': html_form})


