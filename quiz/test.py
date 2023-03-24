from django.test import TestCase
from django.test import Client
import unittest
from .views import MemoryView
import json
import pytest
from django.contrib.auth.models import User
#
# # Create your tests here.
#
#
#
# class SimpleTest(unittest.TestCase):
#     def setUp(self):
#         # Every test needs a client.
#         self.client = Client()
#
#     def test_MemoryView(self):
#         # Issue a GET request.
#         response = self.client.get('memory/')
#         print(response)
#
#         # Check that the response is 200 OK.
#         # self.assertEqual(response.status_code, 200)
#
#         # Check that the rendered context contains 5 customers.
#         # self.assertEqual(len(response.context['desc']), 5)



def test_signin():
    client = Client()
    response = client.get('/signin/')

    assert response.status_code == 200

def test_signin():
    client = Client()
    response = client.get('/signin/')
    assert 'csrfToken' in json.loads(response.content).keys()


def test_signin_content_type():
    client = Client()
    response = client.get('/signin/')
    assert response.headers['Content-Type'] == 'application/json'



def test_signup():
    client = Client()
    response = client.get('/signup/')
    assert response.status_code == 200

# def test_memory():
#     client = Client()
#     response = client.get('/signin/')
#     assert response.status_code == 200




@pytest.mark.django_db
def test_my_user():
    me = User.objects.get(username='Rambo')
    assert me.is_superuser