from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import auth
from .forms import LoginForm, RegisterForm
from .models import Profile


def profile_view(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    context = {
        "profile": profile,
        "followers_list": profile.followers.all(),
        "following_list": profile.following.all()
    }
    return render(request, "profiles/profile.html", context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    context = {"form": form}
    return render(request, "users/login.html", context)


def logout_view(request):
    auth.logout(request)
    return redirect("home")


def signup_view(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(True)
            profile = Profile.objects.create(user=user)
            profile.set_default_avatar()
            profile.save()
            return redirect("home")
    else:
        register_form = RegisterForm()
    context = {"form": register_form}
    return render(request, "users/signup.html", context)
