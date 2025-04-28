import json
from django.contrib.auth.views import LoginView as LoginBaseView, LogoutView as LogoutBaseView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import RegisterForm
from .models import Profile


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['avatar', 'display_name', 'bio']
    template_name = "users/profile_update.html"
    context_object_name = "profile"

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileView(DetailView):
    model = Profile
    template_name = "users/profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(LoginBaseView):
    template_name = "users/login.html"
    redirect_authenticated_user = True


class LogoutView(LogoutBaseView):
    next_page = reverse_lazy("home")


class SignupView(FormView):
    template_name = "users/signup.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save(commit=True)
        return super().form_valid(form)


def follow_profile(request, profile_id):
    if request.method == "POST":
        data = json.loads(request.body)
        user_profile = get_object_or_404(
            Profile, pk=int(data["user_profile_id"]))
        profile = get_object_or_404(Profile, pk=int(data["profile_id"]))

        if user_profile.following.filter(pk=int(profile.id)).exists():
            profile.followers.remove(user_profile)
            msg = "unfollow success"
        else:
            profile.followers.add(user_profile)
            msg = "follow success"
        return JsonResponse({
            "success": True,
            "user_id": user_profile.id,
            "profile_id": profile.id,
            "msg": msg
        })
    else:
        return JsonResponse({"success": False, "error": "Invalid request method"})


def follow_button(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    return render(request, "users/follow_button.html", {"profile": profile})
