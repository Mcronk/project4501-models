from django.db import models
from django.db.models import Count, Min, Sum, Avg, Max
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime  

class Authenticator(models.Model):
	user_id = models.CharField(max_length = 20)
	authenticator = models.CharField(max_length = 255, primary_key = True)
	date_created = models.DateTimeField('Create_time')

class User(models.Model):
	# id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 20)
	password = models.CharField(max_length = 511)
	email = models.CharField(max_length = 20)
	phone = models.CharField(max_length = 20, blank = True, null = True)
	description = models.TextField(blank = True)
	grade = models.IntegerField(default = 0)

class Course(models.Model):
	# id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length=20)
	tag = models.CharField(max_length=20, blank = True)
	description = models.TextField(null = True)
	popularity = models.IntegerField(default = 0)
	qualification = models.CharField(max_length=30, blank = True)
	time = models.CharField(max_length=50, blank = True)
	# available_time = models.DateTimeField(default=datetime.now, blank=True)
	#should be a list of available time
	price = models.IntegerField(default = -1)
	tutor = models.ForeignKey('User', related_name = 'tutoring_courses', null=True)

class Session(models.Model):
	# id = models.IntegerField(primary_key = True)
	time = models.DateTimeField('Class_time')
	
	student = models.ManyToManyField('User', related_name = 'student_session')
	course = models.ForeignKey('Course', related_name = 'course_session')