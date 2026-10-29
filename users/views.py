from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import SellerProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect("catalog:product_list")

    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("catalog:product_list")

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("catalog:product_list")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "You are now logged in.")
        return redirect("catalog:product_list")

    return render(request, "users/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("catalog:product_list")


@login_required
def become_seller(request):
    SellerProfile.objects.get_or_create(user=request.user)
    messages.success(request, "Your seller profile is ready.")
    return redirect("catalog:product_list")