from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from Edus.camera import VideoCamera
from .models import EdusDB
from django.db.models import Sum
from Videos.forms import VideoForm
from Videos.models import VideosDB

# Create your views here.

# 모드 선택 후 화면

def play(request):

	# 비디오 정보 (mp4, avi 등)

    return render(request, 'playView.html')

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

def post_list(request):
	""" 비디오 업로드 """
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

#Edus_list = EdusDB.objects.filter(user_id__contains='jubin')
