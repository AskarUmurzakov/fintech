from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import hashlib
import uuid

class User(AbstractUser):
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    user_hash = models.CharField(max_length=64, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            raw = f'{self.username}{uuid.uuid4()}'.encode('utf-8')
            self.user_hash = hashlib.sha256(raw).hexdigest()
        else:
            db_hash = User.objects.get(pk=self.pk).user_hash
            if self.user_hash != db_hash:
                raise ValidationError("Невозможно изменить хэш пользователя")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

# Create your models here.
