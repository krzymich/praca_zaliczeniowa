from django.test import Client
import json
import pytest
from django.contrib.auth.models import User
from ..models import *



def test_signin():
    client = Client()
    response = client.get('/signin/')
    assert response.status_code == 200

def test_signin_csrf():
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

def test_signup_csrf():
    client = Client()
    response = client.get('/signup/')
    assert 'csrfToken' in json.loads(response.content).keys()

def test_signup_content_type():
    client = Client()
    response = client.get('/signup/')
    assert response.headers['Content-Type'] == 'application/json'


def test_quiz_get_without_parameter():
    client = Client()
    response = client.get('/quiz/')
    assert response.status_code == 400

# @pytest.mark.django_db
# def test_quiz_get_with_parameter():
#     client = Client()
#     response = client.get('/quiz/?lang=en')
#     assert response.status_code == 400
#
# @pytest.mark.django_db
# def test_memory_get_without_parameter():
#     client = Client()
#     response = client.get('/memory/')
#     assert response.status_code == 200
#
# @pytest.mark.django_db
# def test_memory_get_with_parameter():
#     client = Client()
#     User.objects.create_user(username='John', password='123')
#     response = client.get('/memory/?result=82&user=John')
#     assert response.status_code == 200










# def test_memory():
#     client = Client()
#     response = client.get('/signin/')
#     assert response.status_code == 200




@pytest.mark.django_db
def test_signin2():
    User.objects.create_superuser(username='koń')
    me = User.objects.get(username='koń')
    assert me.is_superuser