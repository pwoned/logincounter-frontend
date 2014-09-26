from django.db import models
from django.views.decorators.csrf import csrf_exempt

class User(models.Model):
    ERR_BAD_CREDENTIALS = -1
    ERR_BAD_PASSWORD = -4
    ERR_BAD_USERNAME = -3
    ERR_USER_EXISTS = -2
    MAX_PASSWORD_LENGTH = 128
    MAX_USERNAME_LENGTH = 128
    SUCCESS = 1
    
    user = models.CharField(max_length=MAX_USERNAME_LENGTH, unique=True)
    password = models.CharField(max_length=MAX_PASSWORD_LENGTH, blank=True)
    login_count = models.IntegerField(default=1)
            
    def __unicode__(self):
        return self.user
        
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(MyView, self).dispatch(*args, **kwargs)