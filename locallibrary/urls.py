"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from catalog import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # 将catalog应用的urls模块包含进来
#     path('catalog/', include('catalog.urls')),
#     # 重定向跟目录到catalog
#     path('', RedirectView.as_view(url='catalog/', permanent=True)),
#     # 在开发期间启用静态文件的服务
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', include('catalog.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]