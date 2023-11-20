from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'room_count': rooms.count()}
    return render(request, 'base/home.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)

        try:
            user = User.objects.get(username=username)
        except:
            messages.add_message(request, messages.ERROR, "User does not exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, "Wrong password.")

    context = {}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def room(request, pk):
    room = Room.objects.get(id = pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def room_form(request):
    form = RoomForm()
    
    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)
    
    form = RoomForm(instance=room)
    context = {'form': form}    

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            
            return redirect('home')
        
    return render(request, 'base/room_form.html', context)

def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = {'name': room.name}

    return render(request, 'base/delete.html', context)
