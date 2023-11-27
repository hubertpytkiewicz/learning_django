from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
        )
    print(q)
    for room in rooms:
        print(room.topic)

    topics = Topic.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')
    context = {'rooms': rooms, 'topics': topics, 'room_count': rooms.count(), 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def loginPage(request):

    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
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

    return render(request, 'base/login_register.html', context)

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Couldn't register an account.")

    context = { 'form': form}

    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def room(request, pk):
    
    room = Room.objects.get(id = pk)
    if request.method == 'POST':
        message = Message.objects.create(
            body=request.POST.get('body'),
            user=request.user, 
            room=room, )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
        
    #messages = Message.objects.filter(room__id=pk)
    room_messages = room.message_set.all().order_by('-updated')

    participants = room.participants.all()
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login-page')
def create_room(request):
    form = RoomForm()
    
    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login-page')
def update_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You don't have a permission to do this.")
    
    form = RoomForm(instance=room)
    context = {'form': form}    

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            
            return redirect('home')
        
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login-page')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You don't have a permission to do this.")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = {'name': room.name}

    return render(request, 'base/delete.html', context)

@login_required(login_url='login-page')
def delete_comment(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        if message.room.message_set.filter(user=request.user).count() == 1:
            message.room.participants.remove(request.user)
        message.delete()
        return redirect('home')
    
    context = {'name': message }
    
    return render(request, 'base/delete.html', context)