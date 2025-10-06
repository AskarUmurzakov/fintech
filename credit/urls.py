from django.urls import path
from .views import CreditView, CreditsListView

urlpatterns = [
    path('credit/', CreditView.as_view(), name='credit'),
    path('credits-list/', CreditsListView.as_view(), name='credits-list'),
]