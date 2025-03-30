from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('<int:profile_id>', views.profile_view, name='profile'),
]