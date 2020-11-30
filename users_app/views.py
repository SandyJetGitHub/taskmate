from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomCreationForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        register_form = CustomCreationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, ('New User Created Successfully!, Please Proceed to Login Page!!!'))
            return redirect('register')
    else:
        register_form = CustomCreationForm()
    return render(request, 'register.html', {'register_form':register_form})
    