from django.db import models
from django.contrib.auth.models import User


class DailyHabit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    sleep_hours = models.FloatField(null=True, blank=True)
    exercise_minutes = models.IntegerField(null=True, blank=True)
    meals = models.IntegerField(null=True, blank=True)
    hydration_liters = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class StressLog(models.Model):
    MOOD_CHOICES = [
        ("happy", "😊 Happy"),
        ("neutral", "😐 Neutral"),
        ("stressed", "😟 Stressed"),
        ("anxious", "😰 Anxious"),
        ("sad", "😢 Sad"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    stress_level = models.IntegerField(help_text="Rate 1 (low) - 10 (high)")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood} ({self.stress_level})"


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.title} at {self.time}"
