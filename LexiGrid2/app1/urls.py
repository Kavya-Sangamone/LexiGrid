from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
  
     path('',views.home,name=""),
     path('superadmin_login/', views.superadmin_login, name='superadmin_login'),
     path('superadmindashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
     path('add_creator/', views.add_creator, name='add_creator'),
     path('admin_login/', views.admin_login, name='admin_login'),
     path('admindashboard/', views.admin_dashboard, name='admindashboard'),
     
     path('userlanding/', views.user_landing, name='user_landing'),
     path('creator/<str:admin_id>/', views.creator, name='creator'),
     path('user/',views.user,name="user"),
    #  path('admindashboard/upload_file/', views.upload_file, name='upload_file'),
]
