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
	Uid = time.time()
	request.session['Uid'] = Uid
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
		)
		process.save()
		return HttpResponse("success!")
	else:
		return HttpResponse("failed!")