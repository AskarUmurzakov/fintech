from django.db import models
from django.core.exceptions import ValidationError
import hashlib
from django.contrib.auth import get_user_model

User = get_user_model()

class Transaction(models.Model):
    sender_hash = models.CharField(max_length=20)
    receiver_hash = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=11, decimal_places=2)
    hash = models.CharField(max_length=64, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_sender(self, user_map=None):
        if user_map:
            return user_map.get(self.sender_hash)
        return User.objects.filter(user_hash=self.sender_hash).first()

    def get_receiver(self, user_map=None):
        if user_map:
            return user_map.get(self.receiver_hash)
        return User.objects.filter(user_hash=self.receiver_hash).first()
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError("Транзакции нельзя изменять")

        self.hash = hashlib.sha256(
                f"{self.sender_hash}{self.receiver_hash}{self.value}".encode("utf-8")
            ).hexdigest()
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Транзакции нельзя удалять")
    
    
# Create your models here.
