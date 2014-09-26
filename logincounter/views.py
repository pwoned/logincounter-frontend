#!/usr/bin/env python
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from logincounter.models import User
import json
from django.views.decorators.csrf import csrf_exempt

class UserForm(forms.Form):
	MAX_PASSWORD_LENGTH = 128
	MAX_USERNAME_LENGTH = 128
	
	user = forms.CharField(max_length=MAX_PASSWORD_LENGTH, required=True)
	password = forms.CharField(max_length=MAX_USERNAME_LENGTH)

@csrf_exempt
def home(request):
	form = UserForm()
	return render(request, 'index.html', {'form': form})

@csrf_exempt	
def login(request):
	if request.method == 'POST':
		data = json.loads(request.body.encode(encoding='UTF-8'))
		if data.get('user'):
			try:
				user = User.objects.get(user=data.get('user'))
			except User.DoesNotExist as e:
				return HttpResponse(json.dumps({'errCode': User.ERR_BAD_CREDENTIALS}), content_type="application/json")
			
			if user.password == data.get('password'):
				user.login_count += 1
				user.save()
				return HttpResponse(json.dumps({'errCode': User.SUCCESS, 'count': user.login_count}), content_type="application/json")
			else:
				return HttpResponse(json.dumps({'errCode': User.ERR_BAD_CREDENTIALS}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({'errCode': User.ERR_BAD_CREDENTIALS}), content_type="application/json")
	return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt      
def add(request):
	if request.method == 'POST':
		data = json.loads(request.body.encode(encoding='UTF-8'))
		if data.get('user') and len(data.get('user')) > 0 and len(data.get('user')) <= User.MAX_USERNAME_LENGTH:
			if data.get('password') is None or len(data.get('password')) > User.MAX_PASSWORD_LENGTH:
				return HttpResponse(json.dumps({'errCode': User.ERR_BAD_PASSWORD}), content_type="application/json")
			try:
				user = User.objects.get(user=data.get('user'))
				return HttpResponse(json.dumps({'errCode': User.ERR_USER_EXISTS}), content_type="application/json")
			except User.DoesNotExist as e:
				user = User(user=data.get('user'), password=data.get('password'))
				user.save()
				return HttpResponse(json.dumps({'errCode': User.SUCCESS, 'count': user.login_count}), content_type="application/json")
		else:
			return HttpResponse(json.dumps({'errCode': User.ERR_BAD_USERNAME}), content_type="application/json")
	return HttpResponse(json.dumps({}), content_type="application/json")

@csrf_exempt
def resetFixture(request):
	if request.method == 'POST':
		User.objects.all().delete()
		return HttpResponse(json.dumps({'errCode': User.SUCCESS}), content_type="application/json")
	return HttpResponse(json.dumps({}), content_type="application/json")
	
import os
import subprocess
 
@csrf_exempt
def unitTests(request):
	if request.method == 'POST':
		output = subprocess.check_output("python manage.py test logincounter; exit 0", shell=True, stderr=subprocess.STDOUT)
		lines = output.splitlines()
		for line in lines:
			if line.startswith("Ran "):
				totalTests = line.split(" ")[1]
			else if line.startswith("FAILED (failures="):
				nrFailed = line.split("=")[1]
		return HttpResponse(json.dumps({'nrFailed': nrFailed, 'output': output, 'totalTests': totalTests}), content_type="application/json")

	return HttpResponse(json.dumps({}), content_type="application/json")
