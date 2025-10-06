from django.urls import path
from .views import RegistrationView, UserLoginView, HomeView, logout_view

urlpatterns =[
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('logout/', logout_view, name='logout'),
]