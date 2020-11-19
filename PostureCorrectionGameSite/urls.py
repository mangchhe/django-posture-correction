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
from django.urls import path, include
import Users.views, Videos.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', Videos.views. , name = ),                        # Main 화면
    # path('videoListView/<int:>', Videos.views. , name = ),    # 영상 리스트 화면
    # path('modeView', Edus.views. , name = ),                  # 영상 선택 후 화면
    path('', include('Edus.urls')),
    path('', include('Videos.urls')),
    path('', include('Users.urls')),
    # path('mypages', Users.views. , name = ),                  # 마이페이지 화면
]

# urlpatterns 목록에 MEDIA_URL 추가
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.VIDEO_URL, document_root=settings.VIDEO_ROOT)
urlpatterns += static(settings.EDUS_URL, document_root=settings.EDUS_ROOT)
