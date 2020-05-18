from django.urls import path, include
from Edus import views

urlpatterns = [
    path('playView/page=<int:page_no>', views.play, name = 'playView'),
    path('playView/result/page=<int:page_no>', views.play_after, name = 'playViewResult'),
    path('video_feed', views.video_feed, name='video_feed'),

    path('mypageView', views.post_list, name = 'mypageView'),
]