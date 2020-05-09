from django.urls import path, include
from Edus import views

urlpatterns = [
    path('playView', views.play, name='mode'),
    path('video_feed', views.video_feed, name='video_feed'),
]