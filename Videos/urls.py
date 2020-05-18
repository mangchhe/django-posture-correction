from django.urls import path, include
from Videos import views

urlpatterns = [

    path('videoView', views.showvideo, name = 'videoView'),
    path('search', views.search, name='search'),
    path('', views.main, name='main'),

    path('mypageView', views.showvideo, name = 'mypageView'),

]