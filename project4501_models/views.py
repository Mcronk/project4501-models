from django.http import HttpResponse, JsonResponse, Http404
# from project4501.serializers import UserSerializer, CourseSerializer, ReviewSerializer, SessionSerializer, MessageSerializer, ApplicationSerializer
from project4501_models.models import User, Course, Session
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

#USER: listing all the existing users, or creating a new user.
@csrf_exempt
def user_list(request):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.all()
        users_data = serializers.serialize("json", users) 
        # json_users_data = json.loads(users_data)
        # json_users_data['status'] = 'success'
        # users_data.append({'status':'success'})   
        return JsonResponse(users_data, safe=False)
    elif request.method == 'POST':   
        # data = json.loads(request.POST.get('data',)
        # for deserialized_object in serializers.deserialize("json", request.POST.dict()):
        #     deserialized_object.save() 

        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        description = request.POST.get('description')
        grade = request.POST.get('grade')
        user = User.objects.create(name = name, password=password, email=email, phone=phone,description=description,grade=grade)

        user.save()
        return JsonResponse({'status': 'working'}, safe=False)
        
