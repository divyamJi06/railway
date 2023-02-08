
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # auth
    path('signin/', views.signin,name="signin"), # get leadger as well as report
    # path('signup/', views.signup,name="signup"), # get leadger as well as report
    path('signout', views.signout,name="signout"), # get leadger as well as report
  
  
]