# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


def status(request):
    return JsonResponse({'success': True, 'code': 200})

def home(request):
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect('https://codedocailt4y.rollout.site/')

def login(request):
    return render(request, 'login.html')

