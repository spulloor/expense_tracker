from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm, LoginForm
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, send a welcome email or redirect to a success page
            return redirect('expense_tracker_app:login')  # Redirect to login page after registration
    else:
        form = RegistrationForm()
    return render(request, 'exp_tracker_app/register.html', {'form': form})


def login_view(request):

    if request.user.is_authenticated:
        return HttpResponse("The user is authenticated")
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']  # Access authenticated user from form
            login(request, user)
            return redirect('expense_tracker_app:dashboard')  # Redirect to dashboard after successful login
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'exp_tracker_app/login.html', context)