from django.conf.urls import patterns, url

from game import views

urlpatterns = patterns('',
    url(r'^index$', views.index, name='index'),
    url(r'^getData$', views.getData, name='getData'),
    url(r'^sInfo$', views.sInfo, name='sInfo'),
    url(r'^rule$',views.rule, name ="rule")
    #url(r'^test$', views.getClientIp, name='getClientIp')
)