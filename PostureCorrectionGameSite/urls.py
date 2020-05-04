"""PostureCorrectionGameSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import Users.views, Videos.views, Edus.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', Videos.views. , name = ),                        # Main 화면
    # path('videoListView/<int:>', Videos.views. , name = ),    # 영상 리스트 화면
    # path('modeView', Edus.views. , name = ),                  # 영상 선택 후 화면
    # path('playView', Edus.views. , name = ),                  # 모드 선택 후 화면
    # path('mypages', Users.views. , name = ),                  # 마이페이지 화면
]
