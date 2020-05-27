from django.urls import path, include
from Edus import views

urlpatterns = [
    path('playView/video=<int:video_id>/page=<int:page_no>', views.play, name = 'playView'),
    path('playView/result/page=<int:page_no>', views.play_after, name = 'playViewResult'),
    path('video_feed', views.video_feed, name='video_feed'),

    path('mypageView', views.post_list, name = 'mypageView'),

    path('ResultVideosList', views.ResultVideosList, name='ResultVideosList'),
    path('create', views.create, name='create'),

    path('select/video=<int:video_id>', views.video_select, name='select'),

]