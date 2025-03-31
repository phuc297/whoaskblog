from django.contrib.auth.views import LoginView as LoginBaseView, LogoutView as LogoutBaseView
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView

from .forms import RegisterForm
from .models import Profile


class ProfileView(DetailView):
    model = Profile
    template_name = "users/profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followers_list"] = self.get_object().followers.all()
        context["following_list"] = self.get_object().following.all()
        context["posts_list"] = self.get_object().user.posts.all()
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
        user = form.save(commit=True)
        profile = Profile.objects.create(user=user)
        profile.set_default_avatar()
        profile.save()
        return super().form_valid(form)
