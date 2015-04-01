from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render,get_object_or_404,RequestContext
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from gt.models import *
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib, time, random


def index(request):
	#regist a user automatically 

	Uid = time.time()
	request.session['Uid'] = Uid
	#get the user IP
	try:
	    real_ip = request.META['HTTP_X_FORWARDED_FOR']
	    regip = real_ip.split(",")[0]
	except:
	    try:
	        regip = request.META['REMOTE_ADDR']
	    except:
	        regip = ""
	request.session['clientIP'] = regip
	return render(request, 'index.html')

def getData(request):
	if request.method == 'POST':
		Uid = request.session['Uid']
		times = request.POST.get("times")
		coMethod = request.POST.get("coMethod")
		addMoney = request.POST.get("addMoney")
		money = request.POST.get("money")
		addRobotMoney = request.POST.get("addRobotMoney")
		robotMoney = request.POST.get("robotMoney")
		humanChoose = request.POST.get("humanChoose")
		robotChoose = request.POST.get("robotChoose")
		processDate = datetime.datetime.now()
		clientIP = request.session['clientIP']
		process = Process(
			Uid = Uid,
			times = times,
			coMethod = coMethod,
			addMoney = addMoney,
			money = money,
			addRobotMoney = addRobotMoney,
			robotMoney = robotMoney,
			humanChoose = humanChoose,
			robotChoose = robotChoose,
			processDate = processDate,
			clientIP = clientIP,
		)
		process.save()
		return HttpResponse("success!")
	else:
		return HttpResponse("failed!")

def sInfo(request):
	"""
		Drow the picture of the process
	"""
	try:
		Uid = request.session['Uid']
		process = Process.objects.filter(Uid=Uid)
	except:
		return HttpResponse("Please Play the Game first!!~")
	humanData = [[0,0]]
	robotData = [[0,0]]
	maxY = 0
	minY = 0
	maxX = 0

	for element in process:
		tmpArr = [element.times,element.money]
		humanData.append(tmpArr)
		tmpArr = [element.times,element.robotMoney]
		robotData.append(tmpArr)
		'''find the maxY and minY'''
		if element.money > maxY:
			maxY = element.money
		if element.money < minY:
			minY = element.money
		if element.robotMoney > maxY:
			maxY = element.robotMoney
		if element.robotMoney < minY:
			minY = element.robotMoney

	maxX = element.times
	'''
	 Show the result of the game
	'''
	#save the player info
	try:
		singlePlayer = Player.objects.get(Uid=Uid)
	except:
		singlePlayer = Player(
			Uid = Uid,
			trueName = "",
		    isTrueName = 0,
		    finalScore = humanData[-1][1],
		    finalRobotScore = robotData[-1][1],
		    uploadTime = datetime.datetime.now(),
		    rounds = maxX,
		)
		singlePlayer.save()


	abovePerson = Player.objects.filter(finalScore__gt=singlePlayer.finalScore)
	abovePersonNum = len(abovePerson)+1
	averagePoint = singlePlayer.finalScore / maxX 
	return render(request,'sInfo.html',{"humanData":humanData,"robotData":robotData,'maxY':maxY,'maxX':maxX,'minY':minY,'abovePersonNum':abovePersonNum,"averagePoint":averagePoint})

def rule(request):
	return render(request,"rule.html")

def sName(request):
	try:
		Uid = request.session['Uid']
		singlePlayer = Player.objects.get(Uid=Uid)
	except:
		return HttpResponse("No user")
	singlePlayer.isTrueName = 1
	singlePlayer.trueName = request.POST.get("username")
	singlePlayer.save()
	return HttpResponseRedirect("top")

def top(request):
	data = []
	allPlayer = Player.objects.all()
	rankNum = 1
	for element in allPlayer:
		singleData = {}
		singleData['rank'] = rankNum
		if element.rounds == None:
			singleProcss = Process.objects.filter(Uid = element.Uid)
			singleData['rounds'] = len(singleProcss)
		else:
			singleData['rounds'] = element.rounds
		singleData['averageMoney'] = element.finalScore / singleData['rounds']
		singleData['averageRobotMoney'] = element.finalRobotScore / singleData['rounds']
		if element.isTrueName == 1:
			singleData['trueName'] = element.trueName
		else:
			singleData['trueName'] = "NoName"
		data.append(singleData)
		
		rankNum += 1

	return render(request,"top.html",{"data":data})
