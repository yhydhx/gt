import datetime
from django_mongodb_engine.contrib import MongoDBManager
from django.db import models
from django.utils import timezone
from djangotoolbox.fields import  ListField
from django import forms
import time

class Process(models.Model):
    Uid = models.CharField(max_length=100)
    times = models.IntegerField()
    coMethod = models.IntegerField()
    addMoney = models.FloatField()
    money = models.FloatField()
    addRobotMoney = models.FloatField()
    robotMoney = models.FloatField()
    humanChoose = models.IntegerField()
    robotChoose = models.IntegerField()
    processTime = models.FloatField()
    rivalSelectTime = models.FloatField(null=True)
    clientIP = models.CharField(max_length=30)
    


class Player(models.Model):
    Uid = models.CharField(max_length=100)
    trueName = models.CharField(max_length = 100)
    isTrueName = models.IntegerField()
    sex = models.CharField()
    email = models.CharField()
    age = models.IntegerField(null=True)
    message = models.TextField()
    uploadTime = models.DateTimeField()
    finalScore = models.IntegerField(null=True )
    finalRobotScore = models.IntegerField(null=True )
    rounds = models.IntegerField(null=True)
    ruleId = models.CharField(null=True,max_length=100)
    payoffMatrix = models.CharField(null=True,max_length=100)
    def date_format(self):
        self.uploadTime = self.uploadTime.strftime("%Y-%m-%d")

class Rule(models.Model):
    ruleName = models.CharField(max_length = 100)
    p0 = models.FloatField()
    p1 = models.FloatField()
    p2 = models.FloatField()
    p3 = models.FloatField()
    p4 = models.FloatField()
    maxRound = models.IntegerField()
    minRound = models.IntegerField()
    w = models.FloatField()

class PayoffMatrix(models.Model):
    name = models.CharField(max_length = 100)
    R = models.FloatField()
    T = models.FloatField()
    S = models.FloatField()
    P = models.FloatField()

class User(models.Model):
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    user_flag = models.SmallIntegerField()

class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Member(models.Model):
    name = models.CharField(max_length = 100)
    image = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)
    blog_href = models.CharField(max_length = 200)
    uploadUser = models.CharField(max_length = 100)
    uploadTime = models.DateTimeField()
    uploadUser = models.CharField(max_length = 100)
    def date_format(self):
        self.uploadTime = self.uploadTime.strftime("%Y-%m-%d")

class Room(models.Model):
    roomId = models.CharField(max_length=100)
    roomName = models.CharField(max_length=100)
    userOneId = models.CharField(max_length=100)
    userTwoId = models.CharField(max_length=100)
    userOneTimestamp = models.FloatField()
    userTwoTimestamp = models.FloatField()
    roomSize = models.IntegerField()
    roomExistMember = models.IntegerField()
    uploadTime = models.DateTimeField()
    uploadUser = models.CharField(max_length = 100)
    maxRound = models.IntegerField()
    def date_format(self):
        self.uploadTime = self.uploadTime.strftime("%Y-%m-%d")



class Question(models.Model):
    description = models.TextField()
    selectA = models.CharField(max_length=100)
    selectB = models.CharField(max_length=100)
    selectC = models.CharField(max_length=100)
    selectD = models.CharField(max_length=100)
    correctAnswer = models.IntegerField()
    isShow = models.IntegerField()
    order = models.IntegerField()
    uploadTime = models.DateTimeField()
    uploadUser = models.CharField(max_length = 100)
    def date_format(self):
        self.uploadTime = self.uploadTime.strftime("%Y-%m-%d")


