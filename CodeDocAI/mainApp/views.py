# Create your views here.
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import userCollection  # Ensure this references the MongoDB collection, not a Django ORM model


def status(request):
    return JsonResponse({'success': True, 'code': 200})

def home(request):
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect('https://codedocailt4y.rollout.site/')

def login(request):
    return render(request, 'login.html')

@csrf_exempt
def addUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            user = {
                'name': name,
                'email': email,
                'password': password
            }
            userCollection.insert_one(user)
            return JsonResponse({'success': True, 'code': 200})
        except Exception as e:
            return JsonResponse({'success': False, 'code': 400, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'code': 400})

@csrf_exempt
def getAllUsers(request):
    users = userCollection.find()
    users_list = list(users)  # Convert the Cursor to a list
    for user in users_list:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
    return JsonResponse({'success': True, 'code': 200, 'users': users_list})
