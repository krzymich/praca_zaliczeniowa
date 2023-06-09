"""games_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from quiz.views import QuizView, sign_out, ExtraFeautureView
from quiz.views import MemoryView, SignInView, SignUpView, FlagCourseView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', QuizView.as_view(), name='quiz'),
    path('memory/', MemoryView.as_view(), name='memory'),
    path('course/', FlagCourseView.as_view(), name='course'),
    path('signout/', sign_out),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('extra_feature/', ExtraFeautureView.as_view(), name='extra_feature'),
]
