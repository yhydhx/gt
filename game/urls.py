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
    url(r'^rooms$', views.rooms, name='rooms'),
    url(r'^online/(?P<room_id>\w+)$', views.online,name ='online'),
    url(r'^getOnlineUser$', views.getOnlineUser, name='getOnlineUser'),
    url(r'^getOnlionData$', views.getOnlionData, name='getOnlionData'),
    url(r'^quitGame$', views.quitGame, name='quitGame'),
    url(r'^getInitInfo$', views.getInitInfo, name='getInitInfo'),
    url(r'^checkRule$', views.checkRule, name='checkRule'),
    url(r'^question$', views.question, name='question'),
    url(r'^getAnswer$', views.getAnswer, name='getAnswer'),


    #url(r'^test$', views.getClientIp, name='getClientIp')
)
