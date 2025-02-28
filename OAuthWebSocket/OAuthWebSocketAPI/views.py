from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from allauth.socialaccount.models import SocialAccount
from rest_framework import status
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect("/")

@api_view()
def Oauth(request):
    return render(request, 'auth.html')
    #return HttpResponse(template_name='home.html')            

@api_view()
@login_required
def google_callback(request):
    user = request.user
    try:
        social_account = SocialAccount.objects.get(user=user,provider='google')
        profile_data= social_account.extra_data

        auth_data = {
            'profile_data':profile_data,
            'first_name': profile_data.get('given_name'),
            'last_name': profile_data.get('family_name'),
            'email': profile_data.get('email')
        }
        return Response(auth_data)
    except SocialAccount.DoesNotExist:
        return Response({"message": "Account Not Found for the User"},status=status.HTTP_404_NOT_FOUND)
    