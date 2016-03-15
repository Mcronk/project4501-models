from django.http import HttpResponse, JsonResponse
from project4501_models.models import User, Course, Session, Authenticator
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
import os
import hmac
from . import settings
from datetime import datetime  



#AUTHENTICATOR: login check and create new authenticator
@csrf_exempt
def login(request):
    if request.method == 'POST':
        #email is the username for users to login
        input_email = request.POST.get('email')
        input_password = request.POST.get('password')
        users = User.objects.filter(email = input_email)
        if not users:
            return JsonResponse({'status': 'failure: no such user'}, safe=False)
        user = users[0]
        if input_password == user.password:
            authenticator = hmac.new(key = settings.SECRET_KEY.encode('utf-8'), msg = os.urandom(32), digestmod = 'sha256').hexdigest()
            new_authenticator = Authenticator.objects.create(user_id = input_email, authenticator = authenticator, date_created = datetime.now())
            new_authenticator.save()
            authenticator_data = serializers.serialize("json", [new_authenticator,]) 
            return JsonResponse({'status': 'success', 'authenticator': authenticator}, safe=False)
            return HttpResponse(authenticator_data)
        else:
            return JsonResponse({'status': 'failure: wrong password'}, safe=False)
    return JsonResponse({'status': 'confused: please give id and password'}, safe=False)

#need to change to a specific authenticator API
#AUTHENTICATOR: logout check and delete authenticator
@csrf_exempt
def logout(request):
    if request.method == 'DELETE':
        authenticator = request.POST.get('authenticator')
        Authenticator.objects.get(authenticator=authenticator).delete()
        return JsonResponse({'status': 'success: delete authenticator'}, safe=False)

#USER: listing all the existing users, or creating a new user.
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_data = serializers.serialize("json", users) 
        return HttpResponse(users_data)
    elif request.method == 'POST':   
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('description')
        grade = request.POST.get('grade')
        user = User.objects.create(name = name, password=password, email=email, phone=phone,description=description,grade=grade)
        user.save()
        return JsonResponse({'status': 'success: create user'}, safe=False)
        
#USER: used to retrieve, update or delete the individual user.
@csrf_exempt
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error: user DoesNotExist'}, safe=False)
    if request.method == 'GET':
        #Method 1: a serialized json
        user_data = serializers.serialize("json", [user,]) 
        return HttpResponse(user_data)
        #Method 2: return a dict
        # data = model_to_dict(user)
        # return JsonResponse(data, safe=False)
    elif request.method == 'POST':   
        #Attention: Make sure to POST phone and grade -- None value bug 
        user.name = request.POST.get('name')
        user.password = request.POST.get('password')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.description = request.POST.get('description')
        user.grade = request.POST.get('grade')
        user.save()
        return JsonResponse({'status': 'success: update user'}, safe=False)

#COURSE: listing all the existing courses, or creating a new course.
@csrf_exempt
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        courses_data = serializers.serialize("json", courses) 
        #Attention: Tutor data is pk value, can use Natural Keys to use other fields 
        return HttpResponse(courses_data)
    elif request.method == 'POST':   
        name = request.POST.get('name')
        tag = request.POST.get('tag')
        description = request.POST.get('description')
        popularity = request.POST.get('popularity')
        qualification = request.POST.get('qualification')
        #Attention: time format must be YYYY-MM-DD HH:MM
        time = request.POST.get('time')
        price = request.POST.get('price')
        tutor = User.objects.get(pk=request.POST.get('tutor'))
        course = Course.objects.create(tutor=tutor, name = name, tag=tag, description=description, popularity=popularity,qualification=qualification,time=time, price=price)
        course.save()
        return JsonResponse({'status': 'success: create course'}, safe=False)


#COURSE: used to retrieve, update or delete the individual course.
@csrf_exempt
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({'status': 'error: course DoesNotExist'}, safe=False)
    if request.method == 'GET':
        #Method 1: a serialized json
        course_data = serializers.serialize("json", [course,]) 
        return HttpResponse(course_data)
        #Method 2: return a dict
        # data = model_to_dict(course)
        # return JsonResponse(data, safe=False)
    elif request.method == 'POST':   
        #Attention: Make sure to POST phone and grade -- None value bug 
        course.name = request.POST.get('name')
        course.tag = request.POST.get('tag')
        course.description = request.POST.get('description')
        course.popularity = request.POST.get('popularity')
        course.qualification = request.POST.get('qualification')
        course.time = request.POST.get('time')
        course.price = request.POST.get('price')
        course.tutor = User.objects.get(pk=request.POST.get('tutor'))
        course.save()
        return JsonResponse({'status': 'success: update course'}, safe=False)
    elif request.method == 'DELETE':
        Course.objects.get(pk=pk).delete()
        return JsonResponse({'status': 'success: delete course'}, safe=False)

#SESSION: listing all the existing sessions of a course, or creating a new session.
@csrf_exempt
def session_list(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({'status': 'error: course DoesNotExist'}, safe=False)
    if request.method == 'GET':
        sessions = Session.objects.filter(course=course)
        sessions_data = serializers.serialize("json", sessions) 
        return HttpResponse(sessions_data)
    elif request.method == 'POST':   
        time = request.POST.get('time')
        session = Session.objects.create(time=time, course=course)
        student_pks = request.POST.getlist('student')
        for student_pk in student_pks:
            try:
                student = User.objects.get(pk=student_pk)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error: student DoesNotExist'}, safe=False)
            session.student.add(student)
        session.save()
        return JsonResponse({'status': 'success: create session'}, safe=False)

#SESSION: used to retrieve, update or delete the individual session.
@csrf_exempt
def session_detail(request, pk1, pk2):
    try:
        session = Session.objects.get(pk=pk2)
    except Session.DoesNotExist:
        return JsonResponse({'status': 'error: session DoesNotExist'}, safe=False)
    if request.method == 'GET':
        #Method 1: a serialized json
        session_data = serializers.serialize("json", [session,]) 
        return HttpResponse(session_data)
        #Method 2: return a dict
        # data = model_to_dict(session)
        # return JsonResponse(data, safe=False)
    elif request.method == 'POST':   
        session.time = request.POST.get('time')
        #Attention: session may disallow changing to belong to another course
        session.course = Course.objects.get(pk=pk1)
        student_pks = request.POST.getlist('student')
        session.student.remove(*session.student.all())
        for student_pk in student_pks:
            try:
                student = User.objects.get(pk=student_pk)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error: student DoesNotExist'}, safe=False)
            session.student.add(student)
        session.save()
        return JsonResponse({'status': 'success: update session'}, safe=False)
    elif request.method == 'DELETE':
        Session.objects.get(pk=pk2).delete()
        return JsonResponse({'status': 'success: delete session'}, safe=False)