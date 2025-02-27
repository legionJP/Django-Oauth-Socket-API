from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

def home(request):
    return render(request, 'home.html')

@api_view()
def Oauth(request):
    context = {
    'data': 'data from google api'
    }
    return render(request, 'auth.html', context)
    #return HttpResponse(template_name='home.html')            