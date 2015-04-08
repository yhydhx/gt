#encoding: utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render,get_object_or_404,RequestContext
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from gt.models import *
import datetime
from django.utils import timezone
from gt import settings
import hashlib, time, random,re,json


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
	rules = Rule.objects.all()
	data = []
	count = 1
	for element in rules:
		tmpData = {}
		tmpData['id'] = element.id
		tmpData['name'] = "房间"+str(count)
		tmpData['algorithm'] = element.ruleName
		count += 1
		data.append(tmpData)

	'''
	get the matrix
	'''
	payoff = PayoffMatrix.objects.get(name='Default')
	MONEY_CHANGE = {}
	matrix = {}
	MONEY_CHANGE['0'] = [float(payoff.R), float(payoff.R)]
	MONEY_CHANGE['1'] = [float(payoff.T), float(payoff.S)]
	MONEY_CHANGE['2'] = [float(payoff.S), float(payoff.T)]
	MONEY_CHANGE['3'] = [float(payoff.P), float(payoff.P)]

	matrix['R'] = float(payoff.R)
	matrix['T'] = float(payoff.T)
	matrix['S'] = float(payoff.S)
	matrix['P'] = float(payoff.P)

	request.session['MONEY_CHANGE'] = MONEY_CHANGE
	print MONEY_CHANGE
	return render(request, 'index.html',{"rules":data,'matrix':matrix})

def getData(request):
	if request.method == 'POST':
		Uid = request.session['Uid']
		times = float(request.POST.get("times"))
		lastCoMethod = float(request.POST.get("lastCoMethod"))
		humanChoose = float(request.POST.get("humanChoose"))
		money = float(request.POST.get("money"))
		robotMoney = float(request.POST.get("robotMoney"))
		isFirst = float(request.POST.get("isFirst"))
		rule = get_object_or_404(Rule, id=request.session['ruleId'])
		moneyChange = request.session['MONEY_CHANGE']


		#find the last coMethod and get property
		if isFirst ==1:
			p = rule.p0
		elif lastCoMethod == 0:
			p = rule.p1
		elif lastCoMethod == 1:
			p = rule.p2
		elif lastCoMethod ==2:
			p = rule.p3
		elif lastCoMethod == 3:
			p = rule.p4

		#random a num between 0 and 1. get the robot choice 
		randomNum = random.random()
		#p is the pro. the robot want to choose C, so if randomNum > p, He dislike to C you
		#gernerate the coMethod and money you deserve to get
		if randomNum > p:
			robotChoose = 0
			if humanChoose ==0:
				coMethod = 3
			else:
				coMethod = 2
		else:
			robotChoose = 1
			if humanChoose == 0:
				coMethod = 1
			else:
				coMethod = 0
		addMoney = moneyChange[str(coMethod)][0]
		addRobotMoney = moneyChange[str(coMethod)][1]
		

		money += addMoney
		robotMoney += addRobotMoney
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
		'''
			output :
				addMoney, robotMoney,robotChoose,exit or not
		'''
		Info = {}
		exitFlag = 0
		if times > rule.minRound:
			exitRandom = random.random()
			if exitRandom < rule.w:
				exitFlag = 1
		if times >= rule.maxRound:
			exitFlag = 1
		Info['addMoney'] = addMoney
		Info['addRobotMoney'] = addRobotMoney
		Info['money'] = money
		Info['robotMoney'] = robotMoney
		Info['robotChoose'] = robotChoose
		Info['coMethod'] = coMethod
		Info['exitFlag'] = exitFlag
		process.save()
		return HttpResponse(json.dumps(Info))
	else:

		return HttpResponse("failed!")

def sInfo(request):
	"""
		Drow the picture of the process
	"""
	try:
		Uid = request.session['Uid']
		process = Process.objects.filter(Uid=Uid).order_by("times")
	except:
		return HttpResponse("Please Play the Game first!!~")
	humanData = [[0,0]]
	robotData = [[0,0]]
	maxY = 0
	minY = 0
	maxX = len(process)


	for element in process:
		tmpArr = [element.times,element.money/element.times]
		humanData.append(tmpArr)
		tmpArr = [element.times,element.robotMoney/element.times]
		robotData.append(tmpArr)
		'''find the maxY and minY'''
		element.money = float(element.money)
		element.robotMoney = float(element.robotMoney)
		if element.money/element.times > maxY:
			maxY = element.money/element.times 
		if element.money/element.times  < minY:
			minY = element.money/element.times 
		if element.robotMoney/element.times  > maxY:
			maxY = element.robotMoney/element.times 
		if element.robotMoney/element.times  < minY:
			minY = element.robotMoney/element.times 
		element.averageMoney = round(element.money/element.times,2)
		element.averageRobotMoney = round(element.robotMoney/element.times,2)

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
		    finalScore = element.money,
		    finalRobotScore = element.robotMoney,
		    uploadTime = datetime.datetime.now(),
		    rounds = maxX,
		    ruleId = request.session['ruleId'],
		)
		singlePlayer.save()


	abovePerson = Player.objects.filter(ruleId=request.session['ruleId'],finalScore__gt=singlePlayer.finalScore)
	abovePersonNum = len(abovePerson)+1
	averagePoint = singlePlayer.finalScore / maxX 
	return render(request,'sInfo.html',{"humanData":humanData,"robotData":robotData,'maxY':maxY,'maxX':maxX,'minY':minY,'abovePersonNum':abovePersonNum,"averagePoint":averagePoint,'process':process})

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
	allPlayer = Player.objects.filter(ruleId=request.session['ruleId'])
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


def static(request):
	data = []
	allPlayer = Player.objects.all()
	rankNum =1
	for element in allPlayer:
		singleData = []
		if element.isTrueName ==1:
			singleData.append(element.trueName)
		else:
			singleData.append(' ')
		singleData.append(element.finalScore/element.rounds)
		tmpData = str(singleData)
		tmpData = re.sub("u&#39;",'\'',tmpData)
		tmpData = re.sub("&#39;",'\'',tmpData)
		data.append(tmpData)
	data = ','.join(data)
	return render(request,'static.html',{"data":str(data)})

def getUser(request):
	ruleType = request.POST.get("type")
	rule = get_object_or_404(Rule,id=ruleType)
	request.session['ruleId'] =rule.id
	member = Member.objects.all()
	memberList = []
	memberLen = len(member)
	for element in 	member:
		memberList.append(element.name)	
	getName = memberList[int(random.random()*memberLen)]
	output = {}
	output['name'] = getName
	return HttpResponse(json.dumps(output))
