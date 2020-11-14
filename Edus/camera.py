# -*- encoding: utf8 -*-
import cv2
from django.conf import settings
import os
import time
import numpy as np
import os
import sys
from pathlib import Path


BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
              "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
              "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
              "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

color = [[250, 250, 250], [128, 128, 128], [0, 0, 255], [0, 128, 255], [0, 0, 128], [0, 255, 0], [0, 128, 0], [0, 128, 128], [255, 0, 0],
         [255, 128, 0], [255, 255, 0], [255, 0, 255], [255, 0, 128], [128, 0, 128], [128, 128, 128], [128, 128, 128], [250, 250, 250], [250, 250, 250], [128, 128, 128]]

POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"], ["RElbow", "RWrist"],
              ["LShoulder", "LElbow"], ["LElbow", "LWrist"], [
                  "Neck", "RHip"], ["RHip", "RKnee"],
              ["RKnee", "RAnkle"], ["Neck", "LHip"], [
                  "LHip", "LKnee"], ["LKnee", "LAnkle"],
              ["Neck", "Nose"], ["Nose", "REye"], ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]


class VideoCamera(object):

    def __init__(self, nowDatetime):  # 생성자

        self.nowDatetime = nowDatetime
        # self.video = cv2.VideoCapture(0)  # 0 카메라와 연결

        # cv2.resizeWindow("video", 640, 480)

        self.net = cv2.dnn.readNet(settings.MODEL_ROOT+'human-pose-estimation-0001.xml',
                                   settings.MODEL_ROOT+'human-pose-estimation-0001.bin')  # model, proto

        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        # height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

        width = 640
        height = 480

        # fps = self.video.get(cv2.CAP_PROP_FPS)  # 프레임 수

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(
            settings.EDUS_ROOT+nowDatetime+'.mp4', fourcc, 3, (int(width), int(height)))

    def __del__(self):  # 소멸자

        # self.video.release()  # 비디오 객체 소멸
        self.out.release()

    def get_frame(self, image):

        # start = time.time()

        # success, image = self.video.read()  # 재생되는 비디오를 한 프레임씩 읽는다.

        imageHeight, imageWidth, _ = image.shape

        inpBlob = cv2.dnn.blobFromImage(
            image, size=(456, 256), ddepth=cv2.CV_8U)
        self.net.setInput(inpBlob)
        output = self.net.forward()

        H = output.shape[2]
        W = output.shape[3]

        points = []
        for i in range(0, 19):
            #  해당 신체부위 신뢰도 얻음.
            probMap = output[0, i, :, :]

            #  global 최대값 찾기
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

            #  원래 이미지에 맞게 점 위치 변경
            x = (imageWidth * point[0]) / W
            y = (imageHeight * point[1]) / H


            #  키포인트 검출한 결과가 0.1보다 크면(검출한곳이 위 BODY_PARTS랑 맞는 부위면) points에 추가, 검출했는데 부위가 없으면 None으로    
            if prob > 0.001:
                points.append((int(x), int(y)))
            else:
                points.append(None)
                
        imageCopy = image

        for pair in POSE_PAIRS:
            partA = pair[0]  #  Head
            partA = BODY_PARTS[partA]  #  0
            partB = pair[1]  #  Neck
            partB = BODY_PARTS[partB]  #  1

            if points[partA] and points[partB]:
                cv2.line(imageCopy, points[partA],
                         points[partB], (0, 255, 255), 4)
                cv2.circle(
                    image, points[partA], 8, color[partA], thickness=-1, lineType=cv2.LINE_AA)
                cv2.circle(
                    image, points[partB], 8, color[partB], thickness=-1, lineType=cv2.LINE_AA)

        self.out.write(imageCopy)

        # Image.fromarray(image, 'RGB').show()
        ret, jpeg = cv2.imencode('.jpg', image)  # jpg 형식으로 정보의 형태를 변환시킴(인코딩)

        # if 0.333333 - (time.time() - start) > 0:
        #     time.sleep(0.333333 - (time.time() - start))
        #print(0.333333 - (time.time() - start))

        # Returns the data in the buffer as a string.
        return jpeg.tobytes(), points

