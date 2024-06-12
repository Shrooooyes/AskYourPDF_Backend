from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add-user',views.addUser, name = 'add-user'),
    # path('upload',views.pdfUpload, name = 'upload'),
    path('testSEE', views.testSEE, name = 'testSEE'),
    path('login',views.login, name = 'login'),
    path('update-chat', views.updateChat, name = 'update-chat'),
]
