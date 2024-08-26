from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegistrationForm, LoginForm, ItemForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def register(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('exp_tracker_app:dashboard'))

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, send a welcome email or redirect to a success page
            return redirect('exp_tracker_app:login')  # Redirect to login page after registration
    else:
        form = RegistrationForm()
    return render(request, 'exp_tracker_app/register.html', {'form': form})


def login_view(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('exp_tracker_app:dashboard'))
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']  # Access authenticated user from form
            login(request, user)
            return redirect('exp_tracker_app:dashboard')  # Redirect to dashboard after successful login
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'exp_tracker_app/login.html', context)


def dashboard(request):

    if request.user.is_authenticated:
        return render(request, 'exp_tracker_app/dashboard.html')
    else:
        return HttpResponseRedirect(reverse('exp_tracker_app:login'))


def create_expense(request):

    if request.user.is_authenticated:

        if request.method == 'POST':
            form = ItemForm(request.user, request.POST)
            
            if form.is_valid():
                expense = form.save(commit=False)
                expense.created_by = request.user
                form.save()

                return redirect('exp_tracker_app:dashboard')
        else:
            form = ItemForm(request.user)

        return render(request, 'exp_tracker_app/create_expense.html', {'form': form})
    

def profile(request):
    if request.user.is_authenticated:
        return render(request, 'exp_tracker_app/profile.html')
    else:
        return HttpResponseRedirect(reverse('exp_tracker_app:login'))
    
def logout_from_app(request):
    if request.user.is_authenticated:
        logout(request)
        
    return HttpResponseRedirect(reverse('exp_tracker_app:login'))