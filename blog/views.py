from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserCreationForm, BlogForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import Blog

# Create your views here.

def login_user(request):
    form = AuthenticationForm(data=request.POST or None)
    print(form.is_valid())
    if form.is_valid():
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
        print(user)
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))
    return render(request, 'login.html', {'form':form})

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('login'))
    return render(request, 'register.html', {'form':form})

def home(request):
    user = request.user
    form = BlogForm(request.POST or None)
    blogs = Blog.objects.all()
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        return redirect(reverse('home'))
    return render(request, 'home.html', {'user':user, 'form':form, 'blogs':blogs})