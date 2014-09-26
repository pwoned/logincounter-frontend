from django.test import TestCase
from logincounter.models import User

class TestUsers(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(user="user1", password="password") 
        self.user2 = User.objects.create(user="user2", password="password")   

    def testAdd1(self):
		self.assertEquals(self.user1.login_count, 2)