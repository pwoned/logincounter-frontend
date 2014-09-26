from django.test import TestCase
from logincounter.models import User
from logincounter.views import *
import json

class TestUsers(TestCase):

    MAX_LENGTH_INPUT = "abcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyzabcdefghjiklmnopqrstuvwxyz"

    def setUp(self):
        self.user1 = User.objects.create(user="user1", password="password")
        self.user2 = User.objects.create(user="user2", password="password")
        
    def testDefault(self):
        self.assertEquals(self.user1.login_count, 1)
        self.assertEquals(self.user2.login_count, 1)
        
    def testAdd(self):
        response = User.add({'user': 'user1', 'password': 'password'})
        #self.assertEquals(response.errCode
