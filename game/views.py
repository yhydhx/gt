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
	Uid = md5(str(time.time())+str(random.random()))
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

	try:
		isEng = request.session['isEng']
	except:
		return render(request, 'default.html')
	if isEng == 1:
		return render(request, 'default-eng.html')	
	else:
		return render(request, 'default.html')
#md5 
def md5(s):
	m = hashlib.md5()   
	m.update(s)
	return m.hexdigest()

#language choose
def selectEnglish(request):
	request.session['isEng'] = 1
	return HttpResponseRedirect("index")

def selectChinese(request):
	request.session['isEng'] = 0
	return HttpResponseRedirect("index")

def begin(request):
	#regist a user automatically 
	try:
		Uid = request.session['Uid']
	except:
		return HttpResponseRedirect('index')

	#delete process is there exist process
	Process.objects.filter(Uid=Uid).delete()
	
	
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
	payoff.R = round(payoff.R,1)
	payoff.S = round(payoff.S,1)
	payoff.T = round(payoff.T,1)
	payoff.P = round(payoff.P,1)

	MONEY_CHANGE['0'] = [payoff.R, payoff.R]
	MONEY_CHANGE['1'] = [payoff.T, payoff.S]
	MONEY_CHANGE['2'] = [payoff.S, payoff.T]
	MONEY_CHANGE['3'] = [payoff.P, payoff.P]

	matrix['R'] = payoff.R
	matrix['T'] = payoff.T
	matrix['S'] = payoff.S
	matrix['P'] = payoff.P

	request.session['MONEY_CHANGE'] = MONEY_CHANGE
	
	try:
		isEng = request.session['isEng']
	except:
		return render(request, 'index.html',{"rules":data,'matrix':matrix})
	if isEng == 1:
		return render(request, 'index-eng.html',{"rules":data,'matrix':matrix})
	else:
		return render(request, 'index.html',{"rules":data,'matrix':matrix})

def begin_smaller(request):
	#regist a user automatically 
	try:
		Uid = request.session['Uid']
	except:
		return HttpResponseRedirect('index')

	#delete process is there exist process
	Process.objects.filter(Uid=Uid).delete()
	
	
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

	
	payoff.R = round(payoff.R,1)
	payoff.S = round(payoff.S,1)
	payoff.T = round(payoff.T,1)
	payoff.P = round(payoff.P,1)

	MONEY_CHANGE['0'] = [payoff.R, payoff.R]
	MONEY_CHANGE['1'] = [payoff.T, payoff.S]
	MONEY_CHANGE['2'] = [payoff.S, payoff.T]
	MONEY_CHANGE['3'] = [payoff.P, payoff.P]

	matrix['R'] = payoff.R
	matrix['T'] = payoff.T
	matrix['S'] = payoff.S
	matrix['P'] = payoff.P

	request.session['MONEY_CHANGE'] = MONEY_CHANGE
	

	try:
		isEng = request.session['isEng']
	except:
		return render(request, 'index-smaller.html',{"rules":data,'matrix':matrix})
	if isEng == 1:
		return render(request, 'index-smaller-eng.html',{"rules":data,'matrix':matrix})
	else:
		return render(request, 'index-smaller.html',{"rules":data,'matrix':matrix})
	

def getData(request):
	if request.method == 'POST':
		Uid = request.session['Uid']
		
		#check end
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
		clientIP = request.session['clientIP']
		humanTime = time.time()
		# add some stimilation
		randomTime = random.random()*20-10
		if randomTime < 0:
			waitTime = 0
		else:
			waitTime = randomTime
		time.sleep(int(waitTime))
		rivalClickTime = time.time()
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
			processTime = humanTime,
			rivalSelectTime = rivalClickTime,
			clientIP = clientIP,

		)
		
		process.save()
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
		Info['times'] =int(times)
		Info['watiTime'] = waitTime
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
		if request.session.has_key('user_id'):
			Uid = request.session['user_id']
			process = Process.objects.filter(Uid=Uid).order_by("times")
		else:
			return HttpResponse("Please Play the Game first!!~")

	#prepare for sName
	request.session['user_id'] = Uid
	
	humanData = [[0,0]]
	robotData = [[0,0]]
	maxY = 0
	minY = 0
	maxX = len(process)
	try:
		ruleId = request.session['ruleId']
	except:
		ruleId = 0
	try:
		roomId = request.session['roomId']
		room = Room.objects.get(roomId = roomId)
		if room.userOneId == Uid:
			room.userOneId = ""
			room.roomExistMember -= 1
		elif room.userTwoId == Uid:
			room.userTwoId = ""
			room.roomExistMember -= 1
		room.save()
	except:
		pass

	for element in process:
		tmpArr = [element.times,round(float(element.money)/element.times,2)]
		humanData.append(tmpArr)
		tmpArr = [element.times,round(float(element.robotMoney)/element.times,2)]
		robotData.append(tmpArr)
		'''find the maxY and minY'''
		element.money = float(element.money)
		element.robotMoney = float(element.robotMoney)
		if element.money/element.times > maxY:
			maxY = round(element.money/element.times,2) 
		if element.money/element.times  < minY:
			minY = round(element.money/element.times,2) 
		if element.robotMoney/element.times  > maxY:
			maxY = round(element.robotMoney/element.times,2)
		if element.robotMoney/element.times  < minY:
			minY = round(element.robotMoney/element.times,2)
		element.averageMoney = round(element.money/element.times,2)
		element.averageRobotMoney = round(element.robotMoney/element.times,2)
		if element.humanChoose ==1:
			element.humanSelect = '合作'
		else:
			element.humanSelect = '背叛'
		if element.robotChoose == 1:
			element.robotSelect = '合作'
		else:
			element.robotSelect = '背叛'
			
	# change the maxY to enable the screen show the whole figure
	maxY = maxY * 1.4

	'''
	 Show the result of the game
	'''
	#save the player info
	try:
		singlePlayer = Player.objects.get(Uid=Uid)
		singlePlayer.finalScore = element.money
		singlePlayer.finalRobotScore = element.robotMoney
		singlePlayer.rounds = maxX
		singlePlayer.ruleId = ruleId
		singlePlayer.save()
	except:
		payoff = PayoffMatrix.objects.get(name='Default')
		payoffRestore = [payoff.R,payoff.T,payoff.S,payoff.P]
		singlePlayer = Player(
			Uid = Uid,
			trueName = "",
		    isTrueName = 0,
		    finalScore = element.money,
		    finalRobotScore = element.robotMoney,
		    uploadTime = timezone.now(),
		    rounds = maxX,
		    ruleId = ruleId,
		    payoffMatrix = str(payoffRestore),
		)
		singlePlayer.save()


	abovePerson = Player.objects.filter(ruleId=ruleId,finalScore__gt=singlePlayer.finalScore)
	abovePersonNum = len(abovePerson)+1
	averagePoint = round(float(singlePlayer.finalScore) / maxX,2)
	
	try:
		isEng = request.session['isEng']
	except:
		return render(request,'sInfo.html',{"humanData":humanData,"robotData":robotData,'maxY':maxY,'maxX':maxX,'minY':minY,'abovePersonNum':abovePersonNum,"averagePoint":averagePoint,'process':process})
	if isEng == 1:
		return render(request,'sInfo-eng.html',{"humanData":humanData,"robotData":robotData,'maxY':maxY,'maxX':maxX,'minY':minY,'abovePersonNum':abovePersonNum,"averagePoint":averagePoint,'process':process})
	else:
		return render(request,'sInfo.html',{"humanData":humanData,"robotData":robotData,'maxY':maxY,'maxX':maxX,'minY':minY,'abovePersonNum':abovePersonNum,"averagePoint":averagePoint,'process':process})
	

	

def rule(request):
	questions = Question.objects.filter(isShow=1).order_by('order')
	count = 0
	for element in questions:
		count += 1
		element.name = "Question "+str(count)
	questionNumber = count


	try:
		isEng = request.session['isEng']
	except:
		return render(request,"rule.html",{'questions':questions,'questionNumber':questionNumber})
	if isEng == 1:
		return render(request,"rule-eng.html",{'questions':questions,'questionNumber':questionNumber})
	else:
		return render(request,"rule.html",{'questions':questions,'questionNumber':questionNumber})
	
	

def sName(request):
	try:
		Uid = request.session['user_id']
		singlePlayer = Player.objects.get(Uid=Uid)
	except:
		return HttpResponse("No user")
	singlePlayer.message = request.POST.get("message")
	singlePlayer.save()
	return HttpResponseRedirect("top")

def top(request):
	data = []
	try:
		ruleId = request.session['ruleId']
	except:
		ruleId =0
	allPlayer = Player.objects.filter(ruleId=ruleId)
	rankNum = 1
	for element in allPlayer:
		singleData = {}
		singleData['rank'] = rankNum
		if element.rounds == None:
			singleProcss = Process.objects.filter(Uid = element.Uid)
			singleData['rounds'] = len(singleProcss)
		else:
			singleData['rounds'] = element.rounds
		singleData['averageMoney'] = round(float(element.finalScore) / singleData['rounds'],2)
		singleData['averageRobotMoney'] = round(float(element.finalRobotScore) / singleData['rounds'],2)
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


def rooms(request):
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

	rooms = Room.objects.all()


	'''
		clean the user who is offline
	'''

	for room in rooms:
		expireTime = 10 * 60
		currentTime  = float(time.time())
		userOneStamp = room.userOneTimestamp
		userTwoStamp = room.userTwoTimestamp
		print (currentTime - float(userOneStamp) > expireTime)
		print (currentTime - float(userTwoStamp) > expireTime)
		if room.userOneId != "" and (currentTime - float(userOneStamp) > expireTime):
			room.userOneId = ""
			room.roomExistMember = room.roomExistMember - 1
		if room.userTwoId != "" and (currentTime - float(userTwoStamp) > expireTime):
			room.userTwoId = ""
			room.roomExistMember = room.roomExistMember - 1

		room.save()

	return render(request,"room.html",{'rooms':rooms})

def online(request,room_id):
	Uid = time.time()
	request.session['Uid'] = Uid
	request.session['roomId'] = room_id

	room = Room.objects.get(roomId=room_id)
	existNum = room.roomExistMember
	currentTime  = float(time.time())



	'''
		If the user is the first One , roomExistNum must be zero
		elif the user is not the first One, roomExitNum must one
	'''
	if existNum == 0:
		room.userOneId = Uid
		room.userOneTimestamp = currentTime
		room.roomExistMember = 1
		room.save()

	elif existNum == 1:
		if room.userOneId == "":
			room.userOneId = Uid
			room.userOneTimestamp = currentTime
			room.roomExistMember = 2
			room.save()
						
		elif room.userTwoId == "":
			room.userTwoId = Uid
			room.userTwoTimestamp = currentTime
			room.roomExistMember = 2
			room.save()
	else:
		return HttpResponse("The room is already full!!!!")


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
	
	'''
	get the matrix
	'''
	payoff = PayoffMatrix.objects.get(name='Default')
	matrix = {}


	matrix['R'] = float(payoff.R)
	matrix['T'] = float(payoff.T)
	matrix['S'] = float(payoff.S)
	matrix['P'] = float(payoff.P)


	return render(request, 'indexOnline.html',{'matrix':matrix})

def getOnlineUser(request):
	Uid = request.session['Uid']
	print Uid
	roomId = request.session['roomId']
	room = Room.objects.get(roomId=roomId)

	'''
		update the current  user's timestamp
	'''

	if str(room.userOneId) == str(Uid):
		isUserOne = 1
		room.userOneTimestamp = time.time()
	elif str(room.userTwoId) == str(Uid):
		isUserOne = 0
		room.userTwoTimestamp = time.time()

	data = {}
	existNum = room.roomExistMember
	if existNum == 2:
		data['isFull'] = 1
		if isUserOne == 1:
			request.session['rivalId'] = room.userTwoId
		else:
			request.session['rivalId'] = room.userOneId
		return HttpResponse(json.dumps(data))
	else:
		data['isFull'] = 0
		return HttpResponse(json.dumps(data))

def getOnlionData(request):
	if request.method == 'POST':
		Uid = request.session['Uid']
		rivalId = request.session['rivalId']
		times = float(request.POST.get("times"))
		lastCoMethod = float(request.POST.get("lastCoMethod"))
		humanChoose = float(request.POST.get("humanChoose"))
		money = float(request.POST.get("money"))
		robotMoney = float(request.POST.get("robotMoney"))
		isFirst = float(request.POST.get("isFirst"))
		moneyChange = request.session['MONEY_CHANGE']
		clientIP = request.session['clientIP']
	
		
		getRivalInfo = 0
		
		rivalProcess = Process.objects.filter(Uid=rivalId,times=times)
		if len(rivalProcess) != 0:
			rivalProcess = rivalProcess[0]
			getRivalInfo = 1
			rivalChoice = rivalProcess.humanChoose

			if	rivalChoice == 0:
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

			userProcessSet = Process.objects.filter(Uid=Uid,times=times)

			if len(userProcessSet) == 0:
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
					processTime = time.time(),
					rivalSelectTime = rivalProcess.processTime,
					clientIP = clientIP,
				)
				process.save()
				Room.objects.filter(userOneId=Uid).update(userOneTimestamp=process.processTime)
				Room.objects.filter(userTwoId=Uid).update(userOneTimestamp=process.processTime)

			else:
				userProcess = userProcessSet[0]
				userProcess.coMethod = coMethod
				userProcess.addMoney = addMoney
				userProcess.money = money
				userProcess.addRobotMoney = addRobotMoney
				userProcess.robotMoney = robotMoney
				userProcess.humanChoose = humanChoose
				userProcess.robotChoose = robotChoose
				userProcess.rivalSelectTime = rivalProcess.rivalSelectTime
				userProcess.save()



		else:
			
			if len(Process.objects.filter(Uid=Uid,times=times)) == 0:
				process = Process(
					Uid = Uid,
					times = times,
					coMethod = -1,
					addMoney = 0,
					money = money,
					addRobotMoney = 0,
					robotMoney = robotMoney,
					humanChoose = humanChoose,
					robotChoose = -1,
					processTime = time.time(),
					rivalSelectTime = 0,
					clientIP = clientIP,

				)
				process.save()
				Room.objects.filter(userOneId=Uid).update(userOneTimestamp=process.processTime)
				Room.objects.filter(userTwoId=Uid).update(userOneTimestamp=process.processTime)

		'''
			output :
				addMoney, robotMoney,robotChoose,exit or not
		'''
		Info = {}
		


		roomId = request.session['roomId']
		room = Room.objects.get(roomId=roomId)
		
		'''
			clean the user who is offline
		'''
		expireTime = 10 * 60
		currentTime  = float(time.time())
		userOneStamp = room.userOneTimestamp
		userTwoStamp = room.userTwoTimestamp
		
		if room.userOneId != "" and (currentTime - float(userOneStamp) > expireTime):
			room.userOneId = ""
			room.roomExistMember = room.roomExistMember - 1
		if room.userTwoId != "" and (currentTime - float(userTwoStamp) > expireTime):
			room.userTwoId = ""
			room.roomExistMember = room.roomExistMember - 1
		room.save()
		
		"""
			check the User or His rival  is offLine or not!
		"""
		
		if str(room.userOneId) != str(Uid) and str(room.userTwoId) != str(Uid):
			Info['offLineState'] = 1
		elif str(room.userTwoId) != str(rivalId) and str(room.userOneId) != str(rivalId):
			Info['offLineState'] = 2
		else:
			Info['offLineState'] = 0



		"""
			check the max round is arrived or not
		"""
		exitFlag = 0
		if times > room.maxRound:
				exitFlag = 1
		

		Info['getRivalInfo'] = getRivalInfo
		Info['rivalId'] = rivalId
		Info['Uid'] = Uid
		Info['times'] =int(times)
		if getRivalInfo == 1:
			Info['addMoney'] = addMoney
			Info['addRobotMoney'] = addRobotMoney
			Info['money'] = money
			Info['robotMoney'] = robotMoney
			Info['robotChoose'] = robotChoose
			Info['coMethod'] = coMethod
			Info['exitFlag'] = exitFlag

		
		return HttpResponse(json.dumps(Info))
	else:
		
		return HttpResponse("failed!")

def quitGame(request):
	Uid = str(request.session['Uid'])
	roomId = request.session['roomId']
	room = Room.objects.get(roomId=roomId)
	#print Uid,room.userOneId,room.userTwoId
	#print str(room.userOneId) == Uid,str(room.userTwoId) == Uid
	if room.userOneId == Uid:
		#print " adsfasdfas"
		room.userOneId = ""
		room.roomExistMember -= 1
	elif room.userTwoId == Uid:
		#print " this is user two"
		room.roomExistMember -= 1
		room.userTwoId = ""
	room.save()
	return HttpResponse("Good Bye@")


def quit(request):
	quitFlag = request.GET.get("quit")
	
	if quitFlag == '1':
		del request.session['Uid']
		return HttpResponse("{'answer':'quit the game'}")

def getInitInfo(request):
	if request.method == 'POST':
		try:
			Uid = request.session['Uid']
		except:
			return HttpResponseRedirect("index")

		trueName = request.POST.get('name')
		sex = request.POST.get('sex')
		email = request.POST.get('email')
		age = request.POST.get('age')

		try:
			singlePlayer = Player.objects.get(Uid=Uid)
			singlePlayer.trueName = trueName
			singlePlayer.sex = sex
			singlePlayer.email = email
			singlePlayer.age = age
			singlePlayer.save()
		except:
			payoff = PayoffMatrix.objects.get(name='Default')
			payoffRestore = [payoff.R,payoff.T,payoff.S,payoff.P]
			singlePlayer = Player(
				Uid = Uid,
				trueName = trueName,
				email = email,
				age = age,
				sex = sex,
			    isTrueName = 1,
			    finalScore = 0.0,
			    finalRobotScore = 0.0,
			    uploadTime = datetime.datetime.now(),
			    rounds = 0,
			    ruleId = 0,
			    payoffMatrix = str(payoffRestore),
			)
			singlePlayer.save()
			del request.session['allCorrectFlag']

		return HttpResponseRedirect("begin")

def checkRule(request):
	Uid = request.session['Uid']
	isRead = 1
	
	try:
		singlePlayer = Player.objects.get(Uid=Uid)
	except:
		isRead = 0
	
	Info = {}
	Info['isRead'] = isRead
	return HttpResponse(json.dumps(Info))

def question(request):
	questions = Question.objects.filter(isShow=1).order_by('order')
	count = 0
	for element in questions:
		count += 1
		element.name = "Question "+str(count)
	questionNumber = count
	return render(request,'question.html',{'questions':questions,'questionNumber':questionNumber})


def getAnswer(request):
	questions = Question.objects.filter(isShow=1).order_by('order')
	answer = request.GET.get('qAnswer').split(",")
	count = 0 
	check = {}
	allCorrectFlag = 1
	for element in questions:
		check[str(count)]  = {}
		if element.correctAnswer == int(answer[count]):
			check[str(count)]['correct'] = 1
		else:
			check[str(count)]['correct'] = 0
			allCorrectFlag = 0
		check[str(count)]['correctAnswer'] = element.correctAnswer
		count += 1
	request.session['allCorrectFlag'] = allCorrectFlag

	return HttpResponse(json.dumps(check))

def getAnswerAllCorrect(request):
	Info = {}
	try:
		Info['allCorrectFlag'] = request.session['allCorrectFlag']
	except:
		Info['allCorrectFlag'] = 0
	return HttpResponse(json.dumps(Info))

def test(request):
	return HttpResponse("Helloworld!")
