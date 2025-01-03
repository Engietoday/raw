from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile
from .forms import CustomUserCreationForm

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')


def registerUser(reqeust):
    page = 'register'
    form = CustomUserCreationForm()
    
    if reqeust.method == 'POST':
        form = CustomUserCreationForm(reqeust.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower() # Lowercase the username
            user.save()
            messages.success(reqeust, 'User was created successfully')
            
            login(reqeust, user)
            return redirect('profiles')
        else:
            messages.error(reqeust, 'An error has occurred during registration')
        
    context = {
        'page': page,
        'form': form
    }
    return render(reqeust, 'users/login_register.html', context)

# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    
    context = {
        'profile': profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills
    }
    
    
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    
    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects
    }
    return render(request, 'users/account.html', context)