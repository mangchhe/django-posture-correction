import cv2
from django.conf import settings
import os

face_detection_videocam = cv2.CascadeClassifier(os.path.join(
	settings.BASE_DIR,'opencv_haarcascade_data/haarcascade_frontalface_default.xml'))

# COCO에서 keypoints, 선으로 연결될 skeleton
BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

color = [[250,250,250], [128,128,128], [0,0,255], [0,128,255], [0,0,128], [0,255,0], [0,128,0], [0,128,128], [255,0,0],
        [255,128,0], [255,255,0], [255,0,255], [255,0,128], [128,0,128], [128,128,128], [128,128,128], [250,250,250], [250,250,250], [128,128,128]]

POSE_PAIRS = [["Neck","RShoulder"], ["Neck","LShoulder"], ["RShoulder","RElbow"], ["RElbow","RWrist"], 
                            ["LShoulder","LElbow"], ["LElbow","LWrist"], ["Neck","RHip"], ["RHip","RKnee"],
                            ["RKnee","RAnkle"], ["Neck","LHip"], ["LHip","LKnee"], ["LKnee","LAnkle"], 
                            ["Neck","Nose"], ["Nose","REye"], ["REye","REar"], ["Nose","LEye"], ["LEye","LEar"]]

net = cv2.dnn.readNet(settings.MODEL_ROOT+'human-pose-estimation-0001.xml', settings.MODEL_ROOT+'human-pose-estimation-0001.bin') # model, proto
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

class VideoCamera(object):

	def __init__(self): # 생성자

		self.video = cv2.VideoCapture(0) # 0 카메라와 연결

		self.video.set(3, 360)	# 카메라 크기 조절 너비
		self.video.set(4, 180)	# 카메라 크기 조절 높

	def __del__(self): # 소멸자

		self.video.release() # 비디오 객체 소멸

	def get_frame(self):
		
		success, image = self.video.read() # 재생되는 비디오를 한 프레임씩 읽는다.

		if success:

			# frame.shape = 불러온 이미지에서 height, width, color 받아옴
			imageHeight, imageWidth, _ = image.shape
			
			
			#Prepare input blob and perform an inference
			inpBlob = cv2.dnn.blobFromImage(image, size = (456, 256), ddepth=cv2.CV_8U)
			net.setInput(inpBlob)
			output = net.forward()

			# output.shape[0] = 이미지 ID, [2] = 출력 맵의 높이, [3] = 너비
			H = output.shape[2]
			W = output.shape[3]
			print("이미지 ID : ", len(output[0]), ", H : ", output.shape[2], ", W : ",output.shape[3]) # 이미지 ID

			# 키포인트 검출시 이미지에 그려줌
			points = []
			for i in range(0,19):
				# 해당 신체부위 신뢰도 얻음.
				probMap = output[0, i, :, :]

				# global 최대값 찾기
				minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

				# 원래 이미지에 맞게 점 위치 변경
				x = (imageWidth * point[0]) / W
				y = (imageHeight * point[1]) / H

				# 키포인트 검출한 결과가 0.1보다 크면(검출한곳이 위 BODY_PARTS랑 맞는 부위면) points에 추가, 검출했는데 부위가 없으면 None으로    
				if prob > 0.001 :    
					points.append((int(x), int(y)))
				else :
					points.append(None)

			# 이미지 복사
			imageCopy = image
			# 각 POSE_PAIRS별로 선 그어줌 (머리 - 목, 목 - 왼쪽어깨, ...)
			for pair in POSE_PAIRS:
				partA = pair[0]             # Head
				partA = BODY_PARTS[partA]   # 0
				partB = pair[1]             # Neck
				partB = BODY_PARTS[partB]   # 1
				
				print(partA," 와 ", partB, " 연결\n")
				if points[partA] and points[partB]:
					cv2.line(imageCopy, points[partA], points[partB], (0, 255, 255), 3)
					cv2.circle(image, points[partA], 8, color[partA], thickness=-1, lineType=cv2.LINE_AA)
					cv2.circle(image, points[partB], 8, color[partB], thickness=-1, lineType=cv2.LINE_AA)
			
			frame_flip = cv2.flip(image,1) # 1 좌우 반전, 0 상하 반전
			
			ret, jpeg = cv2.imencode('.jpg', frame_flip) # jpg 형식으로 정보의 형태를 변환시킴(인코딩)
			
			return jpeg.tobytes() # Returns the data in the buffer as a string.
		else:
			print("error")
