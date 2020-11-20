from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import StreamingHttpResponse
from django.http import HttpResponse, JsonResponse
from Edus.camera import VideoCamera
from Edus.camera2 import VideoCamera2
from .models import EdusDB
from Users.models import UsersDB
from Videos.models import VideosDB
from django.core.paginator import Paginator
import datetime
import webbrowser
from PostureCorrectionGameSite import settings
from mutagen.mp4 import MP4
from django.db.models import Sum, Max, Subquery, OuterRef
from Videos.forms import VideoForm
from .forms import EdusDBForm
# Create your views here.
from django.urls import reverse_lazy
import json
from pathlib import Path
import pickle
import cv2
import numpy as np
import datetime
# 11/13 추가
from django.views.decorators.csrf import csrf_exempt
import re
import base64
from PIL import Image

accuracy = 0
rank = ''
rank_trans = 0
rankList = []
total_accuracy_list = []
total_rank_list = []
total_zum_list = []
total_accuracy = 0
total_rank = ''
total_zum = 0
com_movie = False
# 추가 11/14
video_no = 0
flag = True
""" 초당 평균 데이터 구하는 부분 """
p_list = []
save = [[0 for col in range(2)] for row in range(19)]
count = 0
n_count = [0 for row in range(19)]
s_count = 0
skel_list = 0
s_len = 0
videoCamera = 0
sendFlag = True
sendFlag2 = True


BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
              "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
              "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
              "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"], ["RElbow", "RWrist"],
              ["LShoulder", "LElbow"], ["LElbow", "LWrist"], [
                  "Neck", "RHip"], ["RHip", "RKnee"],
              ["RKnee", "RAnkle"], ["Neck", "LHip"], [
                  "LHip", "LKnee"], ["LKnee", "LAnkle"],
              ["Neck", "Nose"], ["Nose", "REye"], ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]

nowDatetime = ""


def dist(v):
    return np.sqrt(v[0]**2 + v[1]**2)


def innerProduct(v1, v2):
    # 벡터 v1, v2의 크기 구하기

    distA = dist(v1)
    distB = dist(v2)

    # 내적 1 (x1x2 + y1y2)
    if v1[0] + v1[1] == 0 or v2[0] + v2[1] == 0:
        return None

    ip = v1[0] * v2[0] + v1[1] * v2[1]

    # 내적 2 (|v1|*|v2|*cos x)
    ip2 = distA * distB

    # cos x값 구하기s
    cost = ip / ip2

    # x값(라디안) 구하기 (cos 역함수)
    x = np.arccos(cost)

    # x값을 x도로 변환하기
    degX = np.rad2deg(x)

    return degX


def score_skeleton(train, result):

    global rankList

    for pair in POSE_PAIRS:
        partA = pair[0]  #  Head
        partA = BODY_PARTS[partA]  # 1
        partB = pair[1]  # Neck
        partB = BODY_PARTS[partB]  # 1

        if train[partA] and result[partB]:
            t_vector = (train[partA][0]-train[partB][0],
                        train[partA][1]-train[partB][1])
            r_vector = (result[partA][0]-result[partB][0],
                        result[partA][1]-result[partB][1])

            # t_vector백터, r_vector -> train, result 각각 백터 값 구해서 넣기
            degree = innerProduct(t_vector, r_vector)

            for i in range(1, 10):

                if degree:

                    if degree < 20 * i:

                        rankList.append(4.5 - .5 * (i - 1))
                        break

                else:

                    break
# 모드 선택 후 화면


def play(request, page_no, video_id):

    global total_accuracy_list
    global total_rank_list
    global total_zum_list
    global video_no

    del total_accuracy_list[:]
    del total_rank_list[:]
    del total_zum_list[:]
    video_no = video_id

    # 비디오 정보 (mp4, avi 등)

    VIDEO_NAME = VideosDB.objects.get(id=video_id)
    videoName = str(VIDEO_NAME.videofile)

    videoLength = MP4(settings.MEDIA_ROOT + videoName).info.length + .5

    edu = EdusDB.objects.filter(video_id=video_id, user_id=request.user.id).order_by(
        '-edu_days')  # 해당 영상과, 사용자 주
    eduList = Paginator(edu, 4)

    idx = []
    eid = []
    days = []
    video = []
    desc = []

    totalPageList = [i for i in range(1, eduList.num_pages + 1)]
    currentPage = page_no

    for i, j in enumerate(eduList.get_page(page_no).object_list.values()):

        idx.append((page_no-1) * 4 + i+1)
        eid.append(j['id'])
        video.append(j['recode_video'])
        desc.append(j['video_description'])
        days.append(j['edu_days'])

    context = {
        'videoList': zip(eid, idx, video, desc, days),
        'totalPageList': totalPageList,
        'currentPage': currentPage,
        'videoName': videoName,
        'videoNo': video_id,
    }

    return render(request, 'playView.html', context)


def play_after(request, page_no, video_no):

    global total_zum, nowDatetime, videoCamera, sendFlag
    # 비디오 정보 (mp4, avi 등)
    sendFlag = False

    # after
    # 조회수 증가
    views = VideosDB.objects.get(id=video_no)
    views.views += 1
    views.save()

    nowDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # before

    edu = EdusDB.objects.filter(video_id=video_no, user_id=request.user.id).order_by(
        '-edu_days')  # 해당 영상과, 사용자 주

    eduList = Paginator(edu, 4)

    text_len = []

    for i in range(len(total_accuracy_list)):

        text_len.append(str(i + 1) + '초')

    total_accuracy = round(sum(total_accuracy_list) /
                           len(total_accuracy_list), 2)

    total_zum = round(sum(total_zum_list) / len(total_zum_list), 2)

    zumList = ['A+', 'A0', 'B+', 'B0', 'C+', 'C0', 'D+', 'D0', 'F']

    for i in range(1, 10):

        if total_zum > 4.5 - .5 * i:

            total_rank = zumList[i - 1]
            rank_trans = ((4.5 - .5 * (i - 1)) / 4.5) * 100
            total_zum = round(100 * (total_zum / 4.5))
            break

    idx = []
    eid = []
    days = []
    video = []
    desc = []

    totalPageList = [i for i in range(1, eduList.num_pages + 1)]
    currentPage = page_no

    for i, j in enumerate(eduList.get_page(page_no).object_list.values()):

        idx.append((page_no-1) * 4 + i+1)
        eid.append(j['id'])
        video.append(j['recode_video'])
        desc.append(j['video_description'])
        days.append(j['edu_days'])
        
    
    video_get = VideosDB.objects.get(id=video_no)
    total_zum = str(total_zum)
    total_rank= str(total_rank)
    total_accuracy = str(total_accuracy)

    if request.method == 'POST':
        form = EdusDBForm(request.POST)
        if form.is_valid():
            del videoCamera
            edus_form = form.save(commit=False)
            edus_form.video_id=video_get
            edus_form.user_id=request.user
            edus_form.recode_video = '/edus/'+nowDatetime+'.mp4'
            edus_form.score = total_zum
            edus_form.save()
    elif request.method == 'GET':
        form = EdusDBForm()
    else:
        pass

    context = {
        'videoList': zip(eid, idx, video, desc, days),
        'totalPageList': totalPageList,
        'currentPage': currentPage,
        'form': form,
        'videoNo': video_no,
        'total_zum': total_zum,
        'total_rank': total_rank,
        'total_accuracy': total_accuracy,
        'rank_trans': rank_trans,
        'total_zum_list': total_zum_list,
        'total_accuracy_list': total_accuracy_list,
        'total_rank_list': total_rank_list,
        'text_len': text_len,
    }

    return render(request, 'playViewResult.html', context)


def getSkelImg(img):  # https://item4.blog/2016-05-08/Generator-and-Yield-Keyword-in-Python/
    # 앨범 이미지
    global accuracy
    global rank
    global rankList
    global com_movie
    global p_list
    global save
    global count
    global n_count
    global s_count
    global skel_list

    # while True:
    #if s_count == s_len:

    points = img
    
    com_movie = True
    for i in range(0, 19):
        if(points[i] == None):
            n_count[i] += 1
        else:
            save[i][0] += points[i][0]
            save[i][1] += points[i][1]

    score_skeleton(skel_list[s_count], save)

    zum = round(sum(rankList) / len(rankList), 2)

    accuracy = round(zum / 4.5 * 100, 2)

    total_zum_list.append(zum)
    total_accuracy_list.append(accuracy)

    zumList = ['A+', 'A0', 'B+', 'B0', 'C+', 'C0', 'D+', 'D0', 'F']

    for i in range(1, 10):

        if zum > 4.5 - .5 * i:
            total_rank_list.append(4.5 - .5 * (i - 1))
            rank = zumList[i - 1]
            break

    del rankList[:]

            # p_list.append(save) # 초당 평균 데이터 -> 이 데이터와 학습 영상 데이터랑 비교하면 됨

    save = [[0 for col in range(2)] for row in range(19)]
    s_count += 1

    # yield (b'--frame\r\n'
    #         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# 마이페이지
def mypage(request):

    return render(request, 'mypageView.html')


def post_list(request):
    """ 비디오 업로드 """

    lastvideo = VideosDB.objects.last()  # 데이터베이스 테이블에서 마지막 비디오(객체)인 변수 lastvideo를 생성
    videofile = lastvideo.videofile.url  # 비디오 파일 경로를 포함하는 변수 videofile을 생성

    # ne, request.FILES request.POST 또는 None은 사용자가 양식을 제출 한 후 데이터를 필드에 유지
    form = VideoForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':

        # print(form.errors)
        if form.is_valid():
            video_form = form.save(commit=False)
            dir = str(request.FILES['videofile'])
            video_form.editor = request.user
            video_form.save()

            # print(form.instance.id)
            item = VideosDB.objects.get(pk=form.instance.id)
            skeleton = VideoCamera2(dir)

            p_list = []
            save_data = [[0 for col in range(2)] for row in range(19)]
            count = 0
            n_count = [0 for row in range(19)]

            while True:
                frame, points = skeleton.get_frame()

                if frame == 2:
                    break
                elif frame == 1:
                    continue
                else:
                    for i in range(0, 19):
                        if(points[i] == None):
                            n_count[i] += 1
                        else:
                            save_data[i][0] += points[i][0]
                            save_data[i][1] += points[i][1]

                    for i in range(0, 19):
                        if(save_data[i][0] != 0):
                            save_data[i][0] /= 3 - n_count[i]
                        if(save_data[i][1] != 0):
                            save_data[i][1] /= 3 - n_count[i]

                    p_list.append(save_data)  # 초당 평균 데이터
                    save_data = [
                        [0 for col in range(2)] for row in range(19)]
                    n_count = [0 for row in range(19)]


            # JSON 인코딩
            jsonString = json.dumps(p_list)

            item.skeleton = jsonString
            item.save()
        else:
            print("else_test")

    """ 업로드 된 영상 및 나의 점수 """

    # Edus 테이블의 전체 데이터 가져오기 -> 로그인이랑 회원가입 만들어지면 queryset 다시 작성 예정
    Edus_list = EdusDB.objects.values('video_id__title', 'score', 'edu_days').filter(user_id=request.user.id).order_by('-edu_days')
    # s_sum = EdusDB.objects.aggregate(Sum('score'))['score__sum'] # Edus 테이블의 전체 score 값 더하기 -> 로그인이랑 회원가입 만들어지면 queryset 다시 작성 예정
    # Edus 테이블의 전체 score 값 더하기 -> 로그인이랑 회원가입 만들어지면 queryset 다시 작성 예정
    Video_list = VideosDB.objects.all().filter(editor=request.user.id).order_by('-start_date')
    s_sum = Edus_list.aggregate(Sum('score'))['score__sum']
    # mypageView로 넘길 데이터
    context = {'videofile': videofile,
               'form': form,
               'score_sum': s_sum,
               'Video_list': Video_list,
               'Edus_list': Edus_list}
    return render(request, 'mypageView.html', context)


def ResultVideosList(request):  # 학습한 결과 영상 리스트 화면 view
    ResultVideos = EdusDB.objects.all()
    EdusDB_list = EdusDB.objects.all().filter(
        user_id=request.user.id).order_by('-edu_days')  # 학습일 최근순으로
    paginator = Paginator(EdusDB_list, 5)  # Paginator를 이용해서 한 페이지에 보여줄 객체 갯수
    page = request.GET.get('  page')  # 현재 페이지를 받아옴
    Edus = paginator.get_page(page)

    context = {'EdusDB_list': EdusDB_list,
               'Edus': Edus}

    return render(request, 'ResultVideosList.html', context)


def video_select(request, video_id):  # 영상 선택 후 화면 view
    Edus_list = EdusDB.objects.filter(
    id=Subquery(
        EdusDB.objects.filter(user_id=OuterRef('user_id'))
            .order_by('-score')
            .values('id')[:1])
    ).values('user_id__username', 'edu_days', 'score')
    another_list = EdusDB.objects.values('user_id__username', 'edu_days','id').exclude(user_id=request.user.id)
    context = {'Edus_list' : Edus_list,
                'another_list' : another_list,
               'video_id': video_id}
    return render(request, 'modepage.html', context)


def resultView(request, edu_id):
    result = EdusDB.objects.filter(id=edu_id)

    return render(request, 'resultView.html', {'result': result})

# 11/13 추가
@csrf_exempt
def sendImg(request):

    global flag
    global s_len
    global nowDatetime
    global skel_list
    global videoCamera
    global sendFlag
    global sendFlag2

    if flag:
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y%m%d%H%M%S')
        videoCamera = VideoCamera(nowDatetime)

        qVideo = VideosDB.objects.get(id=video_no)

        skel_list = json.loads(qVideo.skeleton)

        s_len = len(skel_list)

        nowDatetime = videoCamera.nowDatetime
        
        flag = False

    url = request.POST['url']
    imgstr=re.search(r'data:image/png;base64,(.*)',url).group(1)
    decoded=base64.b64decode(imgstr)
    decoded = np.fromstring(decoded, dtype=np.int8)
    decoded = cv2.imdecode(decoded, cv2.IMREAD_COLOR)

    # img = Image.fromarray(decoded)

    if sendFlag and sendFlag2:
        sendFlag2 = False
        frame, image = videoCamera.get_frame(decoded)
        getSkelImg(image)
        sendFlag2 = True
    else:
        pass

    return JsonResponse({'':''})

def calculatePosture(request):

    global accuracy
    global rank
    global com_movie

    content = {
        'accuracy': accuracy,
        'rank': rank,
        'com_movie': com_movie,
    }

    return JsonResponse(content)


def playResultView(request, edu_id):

    result = EdusDB.objects.filter(id=edu_id)
    return render(request, 'playviewshowmodal.html', {'result': result})


def UploadPreView(request):
    result = '/edus/'+nowDatetime+'.mp4'
    return render(request, 'uploadpreview.html', {'result': result})