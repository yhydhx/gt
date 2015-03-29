import datetime
from django_mongodb_engine.contrib import MongoDBManager
from django.db import models
from django.utils import timezone
from djangotoolbox.fields import  ListField
from django import forms

class Process(models.Model):
    Uid = models.CharField(max_length=100)
    times = models.IntegerField()
    coMethod = models.IntegerField()
    addMoney = models.IntegerField()
    money = models.IntegerField()
    addRobotMoney = models.IntegerField()
    robotMoney = models.IntegerField()
    humanChoose = models.IntegerField()
    robotChoose = models.IntegerField()
    processDate = models.DateTimeField()
    def date_format(self):
    	self.date = self.date.strftime("%Y-%m-%d")



