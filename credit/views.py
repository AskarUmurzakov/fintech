from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from .models import Credit
from .services.credit_service import calculate_credit, create_credit
from django.conf import settings



class CreditView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        context = {
            'rate': settings.CURRENT_CREDIT_RATE
        }
        return render(request, 'credit/credit.html', context=context)
    
    def post(self, request: HttpRequest):
        amount = int(request.POST.get('amount'))
        rate = settings.CURRENT_CREDIT_RATE
        months = int(request.POST.get('months'))

        action = request.POST.get('action')

        if action == "calculate":
            context=calculate_credit(amount, rate, months)
            return render(request, 'credit/credit.html', context=context)
     
        if action == 'save':
            create_credit(request.user, amount, rate, months)
        
        return redirect('credit')
    
class CreditsListView(LoginRequiredMixin, ListView):
    model = Credit
    template_name = 'credit/credits-list.html'
    context_object_name = "credits"

    def get_queryset(self):
        return Credit.objects.filter(user_hash=self.request.user.user_hash).order_by("-created_at")

# Create your views here.
