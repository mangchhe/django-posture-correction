import cv2
from django.conf import settings
import os

face_detection_videocam = cv2.CascadeClassifier(os.path.join(
	settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

class VideoCamera(object):

	def __init__(self): # 생성자

		self.video = cv2.VideoCapture(0) # 0 카메라와 연결

		self.video.set(3, 360)	# 카메라 크기 조절 너비
		self.video.set(4, 180)	# 카메라 크기 조절 높

	def __del__(self): # 소멸자

		self.video.release() # 비디오 객체 소멸

	def get_frame(self):

		success, image = self.video.read() # 재생되는 비디오를 한 프레임씩 읽는다.

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # 입력 받은 화면 gray로 변환

		faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5) # 얼굴 검출

		for (x, y, w, h) in faces_detected: # 검출된 얼굴 전부

			cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2) # 얼굴 사각형 그리기

		frame_flip = cv2.flip(image,1) # 1 좌우 반전, 0 상하 반전

		ret, jpeg = cv2.imencode('.jpg', frame_flip) # jpg 형식으로 정보의 형태를 변환시킴(인코딩)

		return jpeg.tobytes() # Returns the data in the buffer as a string.