from django.urls import path, include
from Videos import views

urlpatterns = [
    path('videoView', views.showvideo, name = 'videoView'),
]