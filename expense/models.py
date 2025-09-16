from django.db import models
from django.contrib.auth.models import User
import datetime
from decimal import Decimal, InvalidOperation


CATEGORY_CHOICES = [
    ("Food", "Food"),
    ("Travel", "Travel"),
    ("Books", "Books"),
    ("Stationery", "Stationery"),
    ("Rent", "Rent"),
    ("Subscriptions", "Subscriptions"),
    ("Shopping", "Shopping"),
    ("Other", "Other"),
]


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(
        max_digits=30,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="Other"
    )
    date = models.DateField(default=datetime.date.today)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-date"]

    def clean_amount(self):
        """
        Convert amount into a valid Decimal.
        Accepts int, float, string numbers.
        Defaults to 0.00 if invalid.
        """
        try:
            # Always cast through str() so int/float/Decimal all work
            return Decimal(str(self.amount)).quantize(Decimal("0.00"))
        except (InvalidOperation, TypeError, ValueError):
            return Decimal("0.00")

    def save(self, *args, **kwargs):
        """Ensure amount is always a safe Decimal before saving"""
        self.amount = self.clean_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - ₹{self.clean_amount():.2f}"
