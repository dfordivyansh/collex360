from django import forms
from .models import DailyHabit, StressLog, Reminder


class DailyHabitForm(forms.ModelForm):
    class Meta:
        model = DailyHabit
        fields = ["sleep_hours", "exercise_minutes", "meals", "hydration_liters"]
        widgets = {
            "sleep_hours": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg bg-white/10 border border-indigo-400/30 "
                         "text-gray-200 placeholder-gray-400 focus:outline-none "
                         "focus:ring-2 focus:ring-indigo-400 focus:border-transparent",
                "placeholder": "Hours of sleep"
            }),
            "exercise_minutes": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg bg-white/10 border border-indigo-400/30 "
                         "text-gray-200 placeholder-gray-400 focus:outline-none "
                         "focus:ring-2 focus:ring-indigo-400 focus:border-transparent",
                "placeholder": "Minutes exercised"
            }),
            "meals": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg bg-white/10 border border-indigo-400/30 "
                         "text-gray-200 placeholder-gray-400 focus:outline-none "
                         "focus:ring-2 focus:ring-indigo-400 focus:border-transparent",
                "placeholder": "Meals today"
            }),
            "hydration_liters": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg bg-white/10 border border-indigo-400/30 "
                         "text-gray-200 placeholder-gray-400 focus:outline-none "
                         "focus:ring-2 focus:ring-indigo-400 focus:border-transparent",
                "placeholder": "Liters of water"
            }),
        }


class StressLogForm(forms.ModelForm):
    class Meta:
        model = StressLog
        fields = ["mood", "stress_level", "notes"]
        widgets = {
            "mood": forms.Select(attrs={
                "class": "w-full px-4 py-2 rounded-lg bg-white/10 border border-indigo-400/30 "
                         "text-yellow-300 bg-gray-900 focus:outline-none focus:ring-2 "
                         "focus:ring-indigo-400"
            }),
            "stress_level": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg bg-white/10 border border-indigo-400/30 "
                         "text-gray-200 placeholder-gray-400 focus:outline-none "
                         "focus:ring-2 focus:ring-indigo-400 focus:border-transparent",
                "placeholder": "Stress level (1-10)"
            }),
            "notes": forms.Textarea(attrs={
                "class": "w-full px-4 py-2 rounded-lg bg-white/10 border border-indigo-400/30 "
                         "text-gray-200 placeholder-gray-400 focus:outline-none "
                         "focus:ring-2 focus:ring-indigo-400 focus:border-transparent",
                "rows": 4,
                "placeholder": "Write any notes..."
            }),
        }


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["title", "time", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg bg-white/10 border border-indigo-400/30 "
                         "text-gray-200 placeholder-gray-400 focus:outline-none "
                         "focus:ring-2 focus:ring-indigo-400 focus:border-transparent",
                "placeholder": "Reminder title"
            }),
            "time": forms.TimeInput(attrs={
                "type": "time",
                "class": "w-full px-4 py-2 rounded-lg bg-white/10 border border-indigo-400/30 "
                         "text-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 text-indigo-500 border-gray-300 rounded focus:ring-indigo-400"
            }),
        }
