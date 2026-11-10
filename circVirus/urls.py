"""circVirus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from web import views, views_dtdb, views_pi

urlpatterns = [
    ## main
    path('admin/', admin.site.urls),
    # path('home/', views.home_new),
    path('home/', views.home),
    ## vcRNAdb
    path('', views.home),
    path('search/', views.search),
    path('browser/', views.browser),
    path('download/', views.download),
    path('help/', views.help),
    path('result/', views.result),
    path('advanceresult2/', views.advanceresult2),
    path('downloadbymail/', views.downloadbymail),
    path('detail/', views.detail),
    path('statistic/', views.statistic),
    re_path('^vcRNAdb/', views.home),
    ## DTDB
    path('dtdb/', views_dtdb.dtdb_web),
    path('dtdb/query/', views_dtdb.dtdb_query),
    path('dtdb/dquery/', views_dtdb.dtdb_dquery),
    path('dtdb/cclquery/', views_dtdb.dtdb_cclquery),
    path('dtdb/ctquery/', views_dtdb.dtdb_ctquery),
    path('dtdb/getccl/', views_dtdb.dtdb_getccl),  # api
    path('dtdb/search/', views_dtdb.dtdb_search),
    path('dtdb/download/', views_dtdb.dtdb_download),
    path('dtdb/help/', views_dtdb.dtdb_help),
    path('dtdb/browser/', views_dtdb.dtdb_browser),
    
    ## PI service 
    path('pi/home/', views_pi.home),
    path('pi/result/', views_pi.func1_result),

]


urlpatterns += [
    # Serve user uploads and generated PI reports. For higher traffic, put a
    # reverse proxy / object storage in front of MEDIA_ROOT instead.
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]