from django.urls import path, include
from Videos import views

urlpatterns = [

    path('search', views.search, name='search'),
    path('', views.main, name='main'),
    path('VideoShow', views.VideoShow.as_view(), name='VideoShow'),
]