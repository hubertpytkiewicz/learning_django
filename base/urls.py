from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login-page'),
    path('register/', views.registerPage, name='register-page'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<str:pk>/', views.update_room, name='update-room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
    path('delete-comment/<str:pk>/', views.delete_comment, name='delete-comment'),
    path('user-page/<str:pk>/', views.userPage, name='user-page'),
    path('update-user/', views.updateUser, name='update-user'),
]