from django.http import HttpResponse, JsonResponse, Http404
from project4501_models.models import User, Course, Session
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.forms.models import model_to_dict

#USER: listing all the existing users, or creating a new user.
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_data = serializers.serialize("json", users) 
        return JsonResponse(users_data, safe=False)
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
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error: user DoesNotExist'}, safe=False)
    if request.method == 'GET':
        #Method 1: a serialized json
        user_data = serializers.serialize("json", [user,]) 
        return JsonResponse(user_data, safe=False)
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
        return JsonResponse(courses_data, safe=False)
    elif request.method == 'POST':   
        name = request.POST.get('name')
        tag = request.POST.get('tag')
        description = request.POST.get('description')
        popularity = request.POST.get('popularity')
        qualification = request.POST.get('qualification')
        #Attention: time format must be YYYY-MM-DD HH:MM
        available_time = request.POST.get('available_time')
        price = request.POST.get('price')
        tutor = User.objects.get(pk=request.POST.get('tutor'))
        course = Course.objects.create(tutor=tutor, name = name, tag=tag, description=description, popularity=popularity,qualification=qualification,available_time=available_time, price=price)
        course.save()
        return JsonResponse({'status': 'success: create course'}, safe=False)

#COURSE: used to retrieve, update or delete the individual course.
# class course_detail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Course.objects.all()