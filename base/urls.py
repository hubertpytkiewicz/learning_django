from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login-page'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('create-room/', views.room_form, name='create-room'),
    path('update-room/<str:pk>/', views.update_room, name='update-room'),
    path('delete-room/<str:pk>/', views.delete_room, name='delete-room'),
]