from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from logincounter.models import User
from django.views.decorators.csrf import csrf_exempt
import json

class UserForm(forms.Form):
    MAX_PASSWORD_LENGTH = 128
    MAX_USERNAME_LENGTH = 128
    
    user = forms.CharField(max_length=MAX_PASSWORD_LENGTH, required=True)
    password = forms.CharField(max_length=MAX_USERNAME_LENGTH)

@csrf_exempt
def unitTests(request):
	if request.method == 'POST':
		return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def resetFixture(request):
	if request.method == 'POST':
		User.objects.all().delete()
		return HttpResponse(json.dumps({'errCode': User.SUCCESS}), content_type="application/json")
	return HttpResponse(json.dumps({}), content_type="application/json")
	
@csrf_exempt
def home(request):
	form = UserForm()
	return render(request, 'index.html', {'form': form})
	
@csrf_exempt
def login(request):
    if request.method == 'POST':
        if request.POST.get('user'):
            try:
                user = User.objects.get(user=request.POST.get('user'))
            except User.DoesNotExist as e:
                return HttpResponse(json.dumps({'errCode': User.ERR_BAD_CREDENTIALS}), content_type="application/json")
            
            if user.password == request.POST.get('password'):
            	user.login_count += 1
            	user.save()
                return HttpResponse(json.dumps({'errCode': User.SUCCESS, 'count': user.login_count}), content_type="application/json")
            else:
                return HttpResponse(json.dumps({'errCode': User.ERR_BAD_CREDENTIALS}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'errCode': User.ERR_BAD_CREDENTIALS}), content_type="application/json") 
    return JsonResponse(json.dumps({}))
   
@csrf_exempt         
def add(request):
	if request.method == 'POST':
		if request.POST.get('user') and len(request.POST.get('user')) <= User.MAX_USERNAME_LENGTH:
			if len(request.POST.get('password')) > User.MAX_PASSWORD_LENGTH:
				return HttpResponse(json.dumps({'errCode': User.ERR_BAD_PASSWORD}), content_type="application/json")
        	try:
        		user = User.objects.get(user=request.POST.get('user'))
        		return HttpResponse(json.dumps({'errCode': User.ERR_USER_EXISTS}), content_type="application/json")
        	except User.DoesNotExist as e:
        		user = User(user=request.POST.get('user'), password=request.POST.get('password'))
        		user.save()
        		return HttpResponse(json.dumps({'errCode': User.SUCCESS, 'count': user.login_count}), content_type="application/json")
        else:
        	return HttpResponse(json.dumps({'errCode': User.ERR_BAD_USERNAME}), content_type="application/json")
	return HttpResponse(json.dumps({}), content_type="application/json")