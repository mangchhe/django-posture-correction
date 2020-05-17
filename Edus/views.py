from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from Edus.camera import VideoCamera
from .models import EdusDB
from Users.models import UsersDB
from Videos.models import VideosDB

# Create your views here.

# 모드 선택 후 화면

def play(request):

	# 비디오 정보 (mp4, avi 등)

	edu = EdusDB.objects.filter(video_id = 1, user_id = 1)	# 해당 영상과, 사용자 주

	days = []
	video = []

	for i in edu.values():

		video.append(i['recode_video'])
		days.append(i['edu_days'])

	context = {
		'a' : zip(video, days),
	}

	if request.method == 'POST':
		new_video = EdusDB.objects.create(
			# edu_days = 현재 시간 자동 저장
			video_id=VideosDB.objects.all()[0],
			user_id=UsersDB.objects.all()[1],
			recode_video='test',
			score=99
		)

	return render(request, 'playView.html', context)

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

