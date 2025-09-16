from django.contrib import admin
from .models import DailyHabit, StressLog, Reminder


@admin.register(DailyHabit)
class DailyHabitAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "sleep_hours", "exercise_minutes", "meals", "hydration_liters")
    list_filter = ("date", "user")
    search_fields = ("user__username",)
    ordering = ("-date",)


@admin.register(StressLog)
class StressLogAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "mood", "stress_level", "notes")
    list_filter = ("mood", "stress_level", "date")
    search_fields = ("user__username", "notes")
    ordering = ("-date",)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "time", "is_active")
    list_filter = ("is_active", "time")
    search_fields = ("user__username", "title")
    ordering = ("time",)
