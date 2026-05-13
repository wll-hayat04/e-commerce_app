from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, UpdateProfileForm

def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,
                f"Bienvenue {user.username} ! Votre compte a été créé.")
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def profile(request):
    return render(request, "registration/profile.html")

@login_required
def update_profile(request):
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect("profile")
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, "registration/update_profile.html", {"form": form})