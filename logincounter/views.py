#!/usr/bin/env python
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from logincounter.models import User
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
	return render(request, 'index.html')

@csrf_exempt	
def login(request):
	if request.method == 'POST':
		data = json.loads(request.body.encode(encoding='UTF-8'))
		return HttpResponse(json.dumps(User.login(data)), content_type="application/json")

@csrf_exempt      
def add(request):
	if request.method == 'POST':
		data = json.loads(request.body.encode(encoding='UTF-8'))
		return HttpResponse(json.dumps(User.add(data)), content_type="application/json")

@csrf_exempt
def resetFixture(request):
	if request.method == 'POST':
		return HttpResponse(json.dumps(User.resetFixture()), content_type="application/json")
	
import os
import subprocess
 
@csrf_exempt
def unitTests(request):
	if request.method == 'POST':
		nrFailed = 0
		totalTests = 0
		output = subprocess.check_output("python manage.py test logincounter; exit 0", shell=True, stderr=subprocess.STDOUT)
		lines = output.splitlines()
		for line in lines:
			if line.startswith("Ran "):
				totalTests = int(line.split(" ")[1])
			elif line.startswith("FAILED (failures="):
				nrFailed = line.split("=")[1][0:-1]
		return HttpResponse(json.dumps({'nrFailed': nrFailed, 'output': output, 'totalTests': totalTests}), content_type="application/json")

	return HttpResponse(json.dumps({}), content_type="application/json")
