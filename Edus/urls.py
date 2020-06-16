from django.urls import path, include
from Edus import views

urlpatterns = [

    path('playView/video=<int:video_id>/page=<int:page_no>', views.play, name = 'playView'),
    path('playView/video=<int:video_no>/result/page=<int:page_no>', views.play_after, name = 'playViewResult'),
    path('video_feed/video=<int:video_id>', views.video_feed, name='video_feed'),

    path('mypageView', views.post_list, name = 'mypageView'),

    path('VideoSelect', views.VideoSelect, name='VideoSelect'),
    path('ResultVideosList', views.ResultVideosList, name='ResultVideosList'),
    path('select/video=<int:video_id>', views.video_select, name='select'),

    path('result/edu_id=<int:edu_id>',views.resultView, name='resultView'),
    path('resultView/edu_id=<int:edu_id>',views.resultView, name='result'),

    path('calculatePosture', views.calculatePosture, name='calculatePosture'),

]
