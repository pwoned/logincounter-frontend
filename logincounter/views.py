from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from logincounter.models import User
from django.views.decorators.csrf import csrf_exempt

class UserForm(forms.Form):
    MAX_PASSWORD_LENGTH = 128
    MAX_USERNAME_LENGTH = 128
    
    user = forms.CharField(max_length=MAX_PASSWORD_LENGTH, required=True)
    password = forms.CharField(max_length=MAX_USERNAME_LENGTH)

@csrf_exempt
def unitTests(request):
	return JsonResponse({})

@csrf_exempt
def resetFixture(request):
	if request.method == 'POST':
		User.objects.all().delete()
		return JsonResponse({'errCode': User.SUCCESS})
	return JsonResponse({})
	
@csrf_exempt
def home(request):
	form = UserForm()
	return render(request, 'index.html', {'form': form})
	
@csrf_exempt
def login(request):
    if request.method == 'POST':
        if len(request.POST['user']) > 0:
            try:
                user = User.objects.get(user=request.POST['user'])
            except User.DoesNotExist as e:
                return JsonResponse({'errCode': User.ERR_BAD_CREDENTIALS})
            
            if user.password == request.POST['password']:
            	user.login_count += 1
            	user.save()
                return JsonResponse({'errCode': User.SUCCESS, 'count': user.login_count})
            else:
                return JsonResponse({'errCode': User.ERR_BAD_CREDENTIALS})
        else:
            return JsonResponse({'errCode': User.ERR_BAD_CREDENTIALS}) 
    return JsonResponse({})
   
@csrf_exempt         
def add(request):
    if request.method == 'POST':
        if len(request.POST['user']) > 0 and len(request.POST['user']) <= User.MAX_USERNAME_LENGTH:
        	if len(request.POST['password']) > User.MAX_PASSWORD_LENGTH:
        		return JsonResponse({'errCode': User.ERR_BAD_PASSWORD})
        	try:
        		user = User.objects.get(user=request.POST['user'])
        		return JsonResponse({'errCode': User.ERR_USER_EXISTS})
        	except User.DoesNotExist as e:
        		user = User(user=request.POST['user'], password=request.POST['password'])
        		user.save()
        		return JsonResponse({'errCode': User.SUCCESS, 'count': user.login_count})
        else:
        	return JsonResponse({'errCode': User.ERR_BAD_USERNAME})
    #return JsonResponse({}, header)