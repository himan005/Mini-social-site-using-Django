from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

def user_login(request):
    if request.method == "POST":
        form =LoginForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user is not None:
                if user.is_active():
                    login(request, user)
                    return HttpResponse("Authentication Successfull")
                else:
                    return HttpResponse("Disabled Account")
            else:
                return HttpResponse('Invalid Login')
    else:
        form =LoginForm()
        context = {
            'form': form
        }
    return render(request, 'account/login.html', context)

@login_required
def dashboard(request):
    context = {
        'section':'dashboard'
    }
    return render(request, 'account/dashboard.html', context)
    
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user = new_user)
            context  = {
                'new_user': new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form })

@login_required
def edit(request):
    if request.method =="POST":
        user_form = UserEditForm(instance= request.user, data = request.POST)
        profile_form = ProfileEditForm(instance= request.user.profile, data = request.POST, files = request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'profile updated Successfully')
        else:
            messages.error(request, 'Error in updating your profile')
    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance = request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/edit.html', context)