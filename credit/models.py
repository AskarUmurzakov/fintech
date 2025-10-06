from django.db import models


class Credit(models.Model):
    user_hash = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=21, decimal_places=2)  # сумма кредита
    rate = models.FloatField()  # годовая процентная ставка
    months = models.PositiveSmallIntegerField()  # количество месяцев
    monthly_payment = models.DecimalField(max_digits=21, decimal_places=2)  # ежемесячный платеж
    total_interest = models.DecimalField(max_digits=21, decimal_places=2)  # переплата
    total_payment = models.DecimalField(max_digits=21, decimal_places=2)  # итого к оплате
    created_at = models.DateTimeField(auto_now_add=True)


# Create your models here.
