from django.urls import path, include
from Edus import views

urlpatterns = [
    path('playView/<int:page_no>', views.play, name = 'playView'),
    path('video_feed', views.video_feed, name='video_feed'),

    path('mypageView', views.mypage, name = 'mypageView'),
]