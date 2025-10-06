from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from .models import Transaction
from decimal import Decimal


User = get_user_model()

class TransactionView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'transactions/transaction.html')

    def post(self, request, *args, **kwargs):
        receiver_username = request.POST.get("receiver_username")
        value_str = request.POST.get("value")

        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return render(request, "transactions/transaction.html", {"error": "Получатель не найден"})

        sender = request.user
        value = Decimal(value_str)

        if sender.balance < value:
            return render(request, "transactions/transaction.html", {"error": "Недостаточно средств"})

        # Обновляем балансы
        sender.balance -= value
        receiver.balance += value
        sender.save()
        receiver.save()

        # Создаём транзакцию
        Transaction.objects.create(
            sender_hash=sender.user_hash,
            receiver_hash=receiver.user_hash,
            value=value
        )

        return redirect("home")
        
