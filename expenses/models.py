# expenses/models.py
from django.db import models
from users.models import User
from django.utils.timezone import now


class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('investment', 'Investment'),
        ('food', 'Food'),
        ('lifestyle', 'Lifestyle'),
        ('entertainment', 'Entertainment'),
        ('petrol', 'Petrol'),
        ('bills', 'Bills'),
        ('others', 'Others'),
    ]

    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    date = models.DateField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.category} - {self.amount}"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=30)
    month = models.DateField(default=now)  # Just use the 1st day of month (e.g., 2025-05-01)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'category', 'month')  # One budget per category/month

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.category} - {self.month.strftime('%B %Y')} - {self.amount}"


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=100)
    date = models.DateField(default=now)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.source} - {self.amount}"
