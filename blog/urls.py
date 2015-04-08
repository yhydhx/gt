from django.conf.urls import patterns, url

from blog import views

urlpatterns = patterns('',
    url(r'^login\.html$', views.login, name='login'),
    url(r'index',views.rule, name="rule"),
   # url(r'^contact$', views.contact,name ='contact'),
    url(r'^addUser$', views.addUser,name ='addUser'),
    url(r'^loginCertifacate$', views.loginCertifacate,name ='loginCertifacate'),
    url(r'^addUserView$', views.addUserView,name ='addUserView'),
    url(r'^changePasswd$', views.changePasswd,name ='changePasswd'),
    url(r'^logout$', views.logout,name ='logout'),

	url(r'^rule/(?P<method>\w+)/(?P<Oid>\w*)$', views.rule,name ='rule'),
	url(r'^member/(?P<method>\w+)/(?P<Oid>\w*)$', views.member,name ='member'),
    url(r'^payoff/(?P<method>\w+)/(?P<Oid>\w*)$', views.payoff,name ='payoff'),
    

    

    #file operation 
    url(r'^addImage$', views.addImage,name ='addImage'),
    url(r'^addImageInfo$', views.addImageInfo,name ='addImageInfo'),
    url(r'^showImgList$', views.showImgList,name ='showImgList'),
    url(r'^deleteImg/(?P<Oid>\w+)$', views.deleteImg,name ='deleteImg'),
    url(r'^test$', views.test,name ='test'),
    url(r'^demo$', views.demo,name ='demo'),
)
