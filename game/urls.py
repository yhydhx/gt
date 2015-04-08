from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^getData$', views.getData, name='getData'),
    url(r'^sInfo$', views.sInfo, name='sInfo'),
    url(r'^rule$',views.rule, name ="rule"),
    url(r'^sName$',views.sName, name ="sName"),
    url(r'^top$',views.top, name ="top"),
    url(r'^static$',views.static, name ="static"),
    url(r'^getUser$', views.getUser, name='getUser'),
    #url(r'^test$', views.getClientIp, name='getClientIp')
)
