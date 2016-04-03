from django.http import HttpResponse, JsonResponse
from project4501_models.models import User, Course, Session, Authenticator
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth import hashers
import json
import os
import hmac
from . import settings, models
from datetime import datetime  
from django import db

#Notes: sign up (user create) needs to check email unique
#Notes: users and courses are returned as lists
#Notes: user and course are returned as dictionary


#AUTHENTICATOR: check authentication
@csrf_exempt
def check_authenticator(request):
    if request.method != 'POST':
        return _error_response(request, "please make POST request with authenticator")
    if 'authenticator' not in request.POST:
        return _error_response(request, "missing required field: authenticator")
    authenticator = request.POST.get('authenticator')
    try:
        auth = Authenticator.objects.get(authenticator = authenticator)
    except models.Authenticator.DoesNotExist:
        return _error_response(request, "no such authenticator")
    try:
        user = User.objects.get(email = auth.user_id)
    except models.User.DoesNotExist:
        return _error_response(request, "user with Authenticator.email DoesNotExist")
    return _success_response(request, {'tutor':user.pk})


#AUTHENTICATOR: login check and create new authenticator
@csrf_exempt
def login(request):
    if request.method != 'POST':
        return _error_response(request, "please make POST request with id and password")
    if 'email' not in request.POST or 'password' not in request.POST:
        return _error_response(request, "missing required field: id or password")
    #email is the username for users to login
    input_email = request.POST.get('email')
    input_password = request.POST.get('password')
    try:
        user = User.objects.get(email = input_email)
    except models.User.DoesNotExist:
        return _error_response(request, "no such user")
    if hashers.check_password(input_password, user.password):
        authenticator = hmac.new(key = settings.SECRET_KEY.encode('utf-8'), msg = os.urandom(32), digestmod = 'sha256').hexdigest()
        new_authenticator = Authenticator.objects.create(user_id = input_email, authenticator = authenticator, date_created = datetime.now())
        new_authenticator.save()
        return _success_response(request, {'authenticator':new_authenticator.authenticator})
    else:
        return _error_response(request, "wrong password")

#AUTHENTICATOR: logout check and delete authenticator
@csrf_exempt
def logout(request):
    if request.method == 'POST':
        authenticator = request.POST.get('authenticator')
        try:
            a = Authenticator.objects.get(authenticator=authenticator)
        except Authenticator.DoesNotExist:
            return _error_response(request, "authenticator DoesNotExist")
        try:
            a.delete()
        except:
            return _error_response(request, "delete fail")
        return _success_response(request)
        return JsonResponse({'status': 'success: delete authenticator'}, safe=False)
    return _error_response(request, "use POST")

#USER: listing all the existing users, or creating a new user.
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_data = serializers.serialize("json", users) 
        return HttpResponse(users_data)
    elif request.method == 'POST':   
        if 'name' not in request.POST or 'password' not in request.POST or 'email' not in request.POST or 'phone' not in request.POST or 'description' not in request.POST or 'grade' not in request.POST:
            return _error_response(request, "missing required field: name or password or email or phone or description or grade")
        try:
            user = User.objects.get(email=request.POST.get('email'))
        except User.DoesNotExist:
            user = User(name = request.POST.get('name'), password = hashers.make_password(request.POST.get('password')), email = request.POST.get('email'), phone = request.POST.get('phone'), description = request.POST.get('description'), grade = int(request.POST.get('grade')))
            try:
                user.save()
            except db.Error:
                return _error_response(request, "db save error")
            return _success_response(request, {'user_name': user.name})
        return _error_response(request, "This email has been registered")
        
#USER: used to retrieve, update or delete the individual user.
@csrf_exempt
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return _error_response(request, "user DoesNotExist")
    if request.method == 'GET':
        #Method 0: return a dictionary
        return _success_response(request, {'name': user.name, 'password': user.password, 'email': user.email, 'phone': user.phone,'description': user.description, 'grade': user.grade})
        #Method 1: a serialized json
        # user_data = serializers.serialize("json", [user,]) 
        # return HttpResponse(user_data)
        #Method 2: return a dict
        # data = model_to_dict(user)
        # return JsonResponse(data, safe=False)
    elif request.method == 'POST':   
        #Attention: Make sure to POST phone and grade -- None value bug 
        if 'name' not in request.POST or 'password' not in request.POST or 'email' not in request.POST or 'phone' not in request.POST or 'description' not in request.POST or 'grade' not in request.POST:
            return _error_response(request, "missing required field: name or password or email or phone or description or grade")
        user.name = request.POST.get('name')
        user.password = request.POST.get('password')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.description = request.POST.get('description')
        user.grade = request.POST.get('grade')
        user.save()
        return _success_response(request, "update user")

#COURSE: listing all the existing courses, or creating a new course.
@csrf_exempt
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        courses_data = serializers.serialize("json", courses) 
        #Attention: Tutor data is pk value, can use Natural Keys to use other fields 
        return HttpResponse(courses_data)
    elif request.method == 'POST':   
        if 'name' not in request.POST or 'tag' not in request.POST or 'description' not in request.POST or 'popularity' not in request.POST or 'qualification' not in request.POST or 'time' not in request.POST or 'price' not in request.POST or 'tutor' not in request.POST:
            return _error_response(request, "missing required field: name or tag or description or popularity or qualification or time or price or tutor")
        try:
            tutor = User.objects.get(pk=request.POST.get('tutor'))
        except User.DoesNotExist:
            return _error_response(request, "tutor DoesNotExist")
        course = Course(tutor=tutor, name=request.POST.get('name'), tag = request.POST.get('tag'), description = request.POST.get('description'), popularity = int(request.POST.get('popularity')), qualification = request.POST.get('qualification'), time = request.POST.get('time'), price = int(request.POST.get('price')))
        try:
            course.save()
        except db.Error:
            return _error_response(request, "db save error")
        return _success_response(request, {'pk': course.pk})


#COURSE: used to retrieve, update or delete the individual course.
@csrf_exempt
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return _error_response(request, "course DoesNotExist")
    if request.method == 'GET':
        #Method 0: return a dictionary
        return _success_response(request, {'name': course.name, 'tag': course.tag, 'description': course.description, 'popularity': course.popularity,'qualification': course.qualification, 'time': course.time, 'price': course.price, 'tutor': course.tutor.pk})
        #Method 1: a serialized json
        # course_data = serializers.serialize("json", [course,]) 
        # return HttpResponse(course_data)
        #Method 2: return a dict
        # data = model_to_dict(course)
        # return JsonResponse(data, safe=False)
    elif request.method == 'POST':    
        if 'name' not in request.POST or 'tag' not in request.POST or 'description' not in request.POST or 'popularity' not in request.POST or 'qualification' not in request.POST or 'time' not in request.POST or 'price' not in request.POST or 'tutor' not in request.POST:
            return _error_response(request, "missing required field: name or tag or description or popularity or qualification or time or price or tutor")
        course.name = request.POST.get('name')
        course.tag = request.POST.get('tag')
        course.description = request.POST.get('description')
        course.popularity = request.POST.get('popularity')
        course.qualification = request.POST.get('qualification')
        course.time = request.POST.get('time')
        course.price = request.POST.get('price')
        try:
            tutor = User.objects.get(pk=request.POST.get('tutor'))
        except User.DoesNotExist:
            return _error_response(request, "tutor DoesNotExist")
        course.tutor = tutor
        course.save()
        return _success_response(request, "update course")
    elif request.method == 'DELETE':
        course.delete()
        return _success_response(request, "delete course")

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


def _error_response(request, error_msg):
    return JsonResponse({'work': False, 'msg': error_msg}, safe=False)

def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'work': True, 'resp': resp}, safe=False)
    else:
        return JsonResponse({'work': True})