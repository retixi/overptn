"""ptn_ana_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from ana.views import *
from overptn.settings import STATIC_URL
from django.contrib import admin



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', root),
    url(r'^ring_dashboard/',ring_dashboard),
    url(r'^link_dashboard/', link_dashboard),
    url(r'^ringList/',ringList),
    url(r'^linkList/', linkList),
    url(r'^dataCollect/', dataCollect),
    url(r'^dateInput/', dateInput),
    url(r'^dataCombine/', dataCombine),
    url(r'^outLink/', outLink),
    url(r'^userhelp/', userhelp),
    url(r'^dataMap/', dataMap),
    url(r'^dataMapHeat/', dataMapHeat),

    # url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':STATIC_URL}),
]
