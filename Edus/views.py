from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from Edus.camera import VideoCamera

# Create your views here.

# 모드 선택 후 화면

def play(request):

    return render(request, 'playView.html')

def gen(camera): # https://item4.blog/2016-05-08/Generator-and-Yield-Keyword-in-Python/

	while True:

		frame = camera.get_frame()

		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):

	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

# 마이페이지

def mypage(request):

	return render(request, 'mypageView.html')

