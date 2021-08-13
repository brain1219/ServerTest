"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from blog import views
from django.conf.urls import url, include

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewset)
router.register(r'cat_and_dogs', views.CatAndDogViewset)
# router.register(r'catdogapi', views.CatAndDogUploadApiViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("blog/", include("blog.urls")),  # blog/ 를 입력하면 blog 앱이 처리함
    path("", RedirectView.as_view(url="/blog/", permanent=True)), #기본 주소 입력시 blog로 넘겨줌
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)