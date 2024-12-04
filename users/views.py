from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from . import forms
from django.contrib import messages
from .models import Profile
from .forms import UserRegistrationForm,ProfileUpdateForm
from django.http import HttpResponseRedirect


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now awaiting approval from the admin.')
            return redirect('login')
        
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')
    
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form':form})


@login_required
def profile(request):
    user = request.user
    
    # Check if the user has a profile, if not, create one
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        # If profile does not exist, create it
        profile = Profile.objects.create(user=user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the same profile page after update
    else:
        form = ProfileUpdateForm(instance=user)
    
    return render(request, 'profile.html', {'form': form, 'profile': profile})


@method_decorator(csrf_protect, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, "Your account is not active. Please contact the admin.")
            return self.form_invalid(form)  
        login(self.request, user)  
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('home')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

    

