from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from transactions.models import Transaction

User = get_user_model()

class RegistrationView(CreateView):
    model = User
    template_name = "accounts/registration.html"
    fields = ['phone', 'username', 'first_name', 'last_name', 'email', 'password']
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True    # если юзер уже залогинен — редирект
    next_page = reverse_lazy("home") 


class HomeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        transactions = Transaction.objects.filter(Q(sender_hash=request.user.user_hash) | Q(receiver_hash=request.user.user_hash)).order_by("-created_at")
        
        hashes = {tx.sender_hash for tx in transactions} | {tx.receiver_hash for tx in transactions}
        users = User.objects.filter(user_hash__in=hashes)
        user_map = {u.user_hash: u for u in users}

        tx_with_users = []
        for tx in transactions:
            tx_with_users.append({
                "tx": tx,
                "sender_username": user_map.get(tx.sender_hash).username if tx.sender_hash in user_map else "???",
                "receiver_username": user_map.get(tx.receiver_hash).username if tx.receiver_hash in user_map else "???",
            })

        context = {"transactions": tx_with_users}
        return render(request, "accounts/home.html", context)

def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('login'))
        
