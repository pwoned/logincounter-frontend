from django.test import TestCase, Client
from logincounter.models import User
import json

class TestUsers(TestCase):
    def setUp(self):
    	self.client = Client()
        self.user1 = User.objects.create(user="user1", password="password")
        self.user2 = User.objects.create(user="user2", password="password")   
        
    def testDefault(self):
        self.assertEquals(self.user1.login_count, 1)
        self.assertEquals(self.user2.login_count, 1)
        
    def testAdd(self):
    	response = self.client.post('/users/add/', data = json.dumps({'user': 'user3', 'password': 'password3'}), content_type="application/json")
    	result = json.loads(response.content)
    	user3 = User.objects.get(user='user3')
    	
    	self.assertEquals(200, response.status_code)
    	self.assertEquals(user3.login_count, result['count'])
    	self.assertEquals(User.SUCCESS, result['errCode'])
		
    def testLogin(self):
    	response = self.client.post('/users/login/', data = json.dumps({'user': self.user1.user, 'password': self.user1.password}), content_type="application/json")
    	result = json.loads(response.content)
    	user1 = User.objects.get(user=self.user1.user)
    	
    	self.assertEquals(200, response.status_code)
    	self.assertEquals(user1.login_count, result['count'])
    	self.assertEquals(User.SUCCESS, result['errCode'])
    	
    def testDuplicateUser(self):
    	response = self.client.post('/users/add/', data = json.dumps({'user': self.user1.user, 'password': 'wrong password'}), content_type="application/json")
    	result = json.loads(response.content)

    	user1 = User.objects.get(user=self.user1.user) 
    		
    	self.assertEquals(200, response.status_code)
    	self.assertEquals(self.user1.password, user1.password)
    	self.assertEquals(User.ERR_USER_EXISTS, result['errCode'])
   	
    def testInvalidPassword(self):
    	response = self.client.post('/users/login/', data = json.dumps({'user': self.user1.user, 'password': 'wrong password'}), content_type="application/json")
    	result = json.loads(response.content)
    	
    	self.assertEquals(200, response.status_code)
    	self.assertEquals(User.ERR_BAD_CREDENTIALS, result['errCode'])
		
    def testInvalidUser(self):
    	response = self.client.post('/users/login/', data = json.dumps({'user': 'bad user', 'password': 'wrong password'}), content_type="application/json")
    	result = json.loads(response.content)
    	
    	self.assertEquals(200, response.status_code)
    	self.assertEquals(User.ERR_BAD_CREDENTIALS, result['errCode'])
    	
    def testLongUser(self):
    	response = self.client.post('/users/login/', data = json.dumps({'user': 'bad user', 'password': 'wrong password'}), content_type="application/json")
    	result = json.loads(response.content)
    	
    	self.assertEquals(200, response.status_code)
    	self.assertEquals(User.ERR_BAD_CREDENTIALS, result['errCode'])
    	
    def testLongPassword(self):
    	response = self.client.post('/users/login/', data = json.dumps({'user': 'bad user', 'password': 'wrong password'}), content_type="application/json")
    	result = json.loads(response.content)
    	
    	self.assertEquals(200, response.status_code)
    	self.assertEquals(User.ERR_BAD_CREDENTIALS, result['errCode'])
	
