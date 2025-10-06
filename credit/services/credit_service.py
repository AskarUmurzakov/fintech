from credit.models import Credit
from transactions.models import Transaction
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def calculate_credit(amount, rate, months):
        i = rate / 12 / 100  # месячная ставка

        context = {
                    'amount': amount,
                    'rate': rate,
                    'months': months,
                }

        monthly_payment = amount * ((i * (1 + i) ** months) / ((1 + i) ** months - 1))
        total_payment = monthly_payment * months
        total_interest = total_payment - amount

        context['result'] = {
            'monthly_payment': round(monthly_payment, 2),
            'total_interest': round(total_interest, 2),
            'total_payment': round(total_payment, 2),
            'method': 'Аннуитетный',
        }

        return context


def create_credit(user, amount, rate, months):
        
        bank_hash = settings.BANK_HASH
        user_hash = user.user_hash

        i = rate / 12 / 100  # месячная ставка
        monthly_payment = amount * ((i * (1 + i) ** months) / ((1 + i) ** months - 1))
        total_payment = monthly_payment * months
        total_interest = total_payment - amount
        
        bank = User.objects.get(user_hash=settings.BANK_HASH)

        bank.balance -= amount
        user.balance += amount
        bank.save()
        user.save()

        tx = Transaction.objects.create(
                        sender_hash=bank_hash,
                        receiver_hash=user_hash,
                        value=amount
                    )

        credit = Credit.objects.create(
                        user_hash=user_hash,
                        amount=amount,
                        rate=rate,
                        months=months,
                        monthly_payment=monthly_payment,
                        total_payment=total_payment,
                        total_interest=total_interest,
                    )

        return tx, credit
        