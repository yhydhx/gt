# coding: utf-8  
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render,get_object_or_404,RequestContext
from django.core.urlresolvers import reverse
from django.views import generic
#from dc.models import Poll,Choice,Blog
from django import forms
from gt.models import *
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib,time,re


'''def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': 1}
    return render(request, 'dc/index.html', context)
'''

def __checkin__(request):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')

def login(request):
    return render(request, 'blog/login.html' )

def logout(request):
    del request.session['username']
    return HttpResponseRedirect("login.html")

def loginCertifacate(request):
    if request.method == 'POST': 
    # If the form has been submitted...
        username = request.POST.get("username")
        tmpPassword = request.POST.get("password")
        md5Encode = hashlib.new("ripemd160")
        md5Encode.update(tmpPassword)
        password = md5Encode.hexdigest()

        admin = get_object_or_404(Admin, username=username)
        if admin.password == password:
            request.session['username'] = username
            return HttpResponseRedirect('/dc/rule/show')
        else:
            return HttpResponse("密码错误") 
        

def addUserView(request):
    return render(request,"blog/addUserView.html")

def addUser(request):
    md5Encode = hashlib.new("ripemd160")
    username = request.POST.get("username")
    tmpPassword = request.POST.get("password")
    confirmPassword = request.POST.get("password2")
    if tmpPassword != confirmPassword:
        return HttpResponse("两次输入的密码不一致")
    md5Encode.update(tmpPassword)
    password = md5Encode.hexdigest()
    
    veryfyUser = Admin.objects.filter(username = username).all()
    
    try:
        HttpResponse(veryfyUser[0])
    except IndexError,e:
        veryfyUser = None
    if veryfyUser is not None:
        return HttpResponse("This admin is already exits")

    admin = Admin(
        username = username,
        password = password,

        )
    admin.save()
    return render(request,"blog/login.html")
 
def changePasswd(request):
    if request.method == "POST":
        username = request.POST.get("username")
        tmpPassword = request.POST.get("password")
        newPassword = request.POST.get("newPassword")
        md5Encode = hashlib.new("ripemd160")
        md5Encode.update(tmpPassword)
        password = md5Encode.hexdigest()

        user = get_object_or_404(User, username=username)
        if user.password == password:
            newEncode = hashlib.new("ripemd160")
            newEncode.update(newPassword)
            user.password = newEncode.hexdigest()
            user.save()
            del request.session['username']
            return HttpResponseRedirect("login.html")
        else:
            return HttpResponse("密码错误")    
        
    else:
        return render(request,"dc/changePasswd")

def index(request):
    # render(request,'dc/index2.html',{'dept':dept.objects.all()})
    return render(request,'blog/index.html')


########################################################
# this view is about the Rule 
# contains show schl list , add schl , change schl, 
# delete schl,and add new schl
# News contain a couple of  parts , title content date                 
########################################################

def rule(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')

    if method == 'addRule' :
        ruleName = request.POST.get("ruleName")
        p0 = request.POST.get("p0")
        p1 = request.POST.get("p1")
        p2 = request.POST.get("p2")
        p3 = request.POST.get("p3")
        p4 = request.POST.get("p4")
        maxRound = request.POST.get("maxRound")
        minRound = request.POST.get("minRound")
        w = request.POST.get("w")
        rule = Rule(
            ruleName = ruleName,
            p0 = p0, 
            p1 = p1,
            p2 = p2,
            p3 = p3,
            p4 = p4,
            maxRound = maxRound,
            minRound = minRound,
            w = w
            )
        rule.save()

        return HttpResponseRedirect('/dc/rule/show')
    elif method == 'change':
        rule = Rule.objects.get(id=Oid)
        return render(request,'blog/changeRule.html',{'rule':rule})

    elif method == 'save':
        if request.method == 'POST':
            rule = {'id' : request.POST.get('id'),
                    'ruleName' : request.POST.get("ruleName"),
                    'p0' : request.POST.get("p0"),
                    'p1' : request.POST.get("p1"),
                    'p2' : request.POST.get("p2"),
                    'p3' : request.POST.get("p3"),
                    'p4' : request.POST.get("p4"),
                    'maxRound' : request.POST.get("maxRound"),
                    'minRound' : request.POST.get("minRound"),
                    'w' : request.POST.get("w"),
                }

        Rule.objects.filter(id=rule['id']).update(  ruleName = rule['ruleName'],
                                                    p0 = rule['p0'],
                                                    p1 = rule['p1'],
                                                    p2 = rule['p2'],
                                                    p3 = rule['p3'],
                                                    p4 = rule['p4'],
                                                    maxRound = rule['maxRound'],
                                                    minRound = rule['minRound'],
                                                    w = rule['w'],
                                                )
       
        return HttpResponseRedirect('/dc/rule/show')

    elif method == 'delete':
        Rule.objects.filter(id=Oid).delete()
   
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request,'blog/addRuleView.html')
    elif method == 'show' or method == '':
        allRule = Rule.objects.all()
        return render(request,'blog/showRuleList.html',{'rule':allRule})
    else:
        return HttpResponse('没有该方法')


def payoff(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')

    if method == 'addPayoff' :
        name = request.POST.get("name")
        R = request.POST.get("R")
        T = request.POST.get("T")
        S = request.POST.get("S")
        P = request.POST.get("P")
        payoff = PayoffMatrix(
            name = name,
            R = R, 
            T = T,
            S = S,
            P = P,
            )
        payoff.save()

        return HttpResponseRedirect('/dc/payoff/show')
    elif method == 'change':
        payoff = PayoffMatrix.objects.get(id=Oid)
        return render(request,'blog/changePayoff.html',{'payoff':payoff})

    elif method == 'save':
        if request.method == 'POST':
            payoff = {'id' : request.POST.get('id'),
                    'name' : request.POST.get("name"),
                    'R' : request.POST.get("R"),
                    'T' : request.POST.get("T"),
                    'S' : request.POST.get("S"),
                    'P' : request.POST.get("P"),
                }

        PayoffMatrix.objects.filter(id=payoff['id']).update(  name = payoff['name'],
                                                    R = payoff['R'],
                                                    T = payoff['T'],
                                                    S = payoff['S'],
                                                    P = payoff['P'],
                                                )
       
        return HttpResponseRedirect('/dc/payoff/show')

    elif method == 'delete':
        PayoffMatrix.objects.filter(id=Oid).delete()
   
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request,'blog/addPayoffView.html')
    elif method == 'show' or method == '':
        allPayOff = PayoffMatrix.objects.all()
        return render(request,'blog/showPayoffList.html',{'payoff':allPayOff})
    elif method =='select':
        payoff  = PayoffMatrix.objects.get(id=Oid)
        PayoffMatrix.objects.filter(name='Default').update(
                                                            R = payoff.R,
                                                            T = payoff.T,
                                                            S = payoff.S,
                                                            P = payoff.P,
                                                            )
        return HttpResponseRedirect("/dc/payoff/show")
    else:
        return HttpResponse('没有该方法')




def member(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')

    if method == 'addMember' :
        name = request.POST.get("name")
        image = request.POST.get("image")
        description = request.POST.get("description")
        blog_href = request.POST.get("blog_href")
        uploadTime = datetime.datetime.now(),
        uploadUser = request.session['username'],
        member = Member(
            name = name,
            image = image,
            description = description,
            blog_href = blog_href,
            uploadTime = datetime.datetime.now(),
            uploadUser = request.session['username'],
            )
        member.save()

        return HttpResponseRedirect('/dc/member/show')
    elif method == 'change':
        member = Member.objects.get(id=Oid)
        return render(request,'blog/changeMember.html',{'member':member})

    elif method == 'save':
        if request.method == 'POST':
            member = {
                    "id" : request.POST.get("id"),
                    "name" : request.POST.get("name"),
                    "image" : request.POST.get("image"),
                    "description" : request.POST.get("description"),
                    "blog_href" : request.POST.get("blog_href"),
                }

        Member.objects.filter(id=member['id']).update(
                                                    name = member['name'],
                                                    image = member['image'],
                                                    description = member['description'],
                                                    blog_href = member['blog_href'],
                                                )
       
        return HttpResponseRedirect('/dc/member/show')

    elif method == 'delete':
        Member.objects.filter(id=Oid).delete()
   
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request,'blog/addMemberView.html')
    elif method == 'show' or method == '':
        allMember = Member.objects.all()
        return render(request,'blog/showMemberList.html',{'member':allMember})
    else:
        return HttpResponse('没有该方法')


##################################################################################################
#  file operation 
#   about image and video
##################################################################################################

def addImage(request):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')   
    if request.method == "POST":
        return HttpResponse(1)
    return render(request,'blog/addImage.html')

def addImageInfo(request):
    if request.method == "POST":
        des_origin_path = settings.UPLOAD_PATH+'/images/'+request.POST.get('title')
        des_origin_f = open(des_origin_path, "ab") 
        tmpImg = request.FILES['img']
        for chunk in tmpImg.chunks():  
            des_origin_f.write(chunk)   
        des_origin_f.close() 
        img = Image(
            title = request.POST.get('title'),
            location = des_origin_path,
            uploadUser = request.session['username'],
            )
        img.save()
        return HttpResponseRedirect('showImgList')
    return HttpResponse('allowed only via POST')

def showImgList(request):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')    
    return render(request,'dc/showImgList.html',{'image':Image.objects.all() })

def deleteImg(request,Oid):
    Image.objects.filter(id=Oid).delete()
    return HttpResponseRedirect('../showImgList')

def test(request):
    return   render(request,"blog/ust.html")

def demo(request):
    return render(request,"blog/demo.html")
