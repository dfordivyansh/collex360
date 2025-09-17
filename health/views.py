from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import DailyHabit, StressLog, Reminder
from .forms import DailyHabitForm, StressLogForm, ReminderForm


@login_required(login_url="signup")
def health_dashboard(request):
    user = request.user

    # Latest habit entry (today or most recent)
    latest_habit = DailyHabit.objects.filter(user=user).order_by('-date').first()

    sleep_hours = latest_habit.sleep_hours if latest_habit else 0
    exercise_minutes = latest_habit.exercise_minutes if latest_habit else 0
    meals_count = latest_habit.meals if latest_habit else 0
    water_intake = latest_habit.hydration_liters if latest_habit else 0

    # Stress logs (latest 10)
    stress_logs = StressLog.objects.filter(user=user).order_by('-date')[:10]

    # Active reminders
    reminders = Reminder.objects.filter(user=user, is_active=True).order_by('time')

    # Chart data (last 7 days habits)
    last_7_days = DailyHabit.objects.filter(user=user).order_by('-date')[:7][::-1]

    dates = [habit.date.strftime("%b %d") for habit in last_7_days]
    sleep_data = [habit.sleep_hours or 0 for habit in last_7_days]
    water_data = [habit.hydration_liters or 0 for habit in last_7_days]
    exercise_data = [habit.exercise_minutes or 0 for habit in last_7_days]

    context = {
        "sleep_hours": sleep_hours,
        "exercise_minutes": exercise_minutes,
        "meals_count": meals_count,
        "water_intake": water_intake,
        "stress_logs": stress_logs,
        "reminders": reminders,
        "dates": dates,
        "sleep_data": sleep_data,
        "water_data": water_data,
        "exercise_data": exercise_data,
    }
    return render(request, "health/dashboard.html", context)


@login_required(login_url="signup")
def track_habits(request):
    if request.method == "POST":
        form = DailyHabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect("health:track_habits")
    else:
        form = DailyHabitForm()

    habits = DailyHabit.objects.filter(user=request.user).order_by("-date")
    return render(request, "health/track_habits.html", {"form": form, "habits": habits})


@login_required(login_url="signup")
def stress_log(request):
    if request.method == "POST":
        form = StressLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect("health:stress_log")
    else:
        form = StressLogForm()

    logs = StressLog.objects.filter(user=request.user).order_by("-date")
    return render(request, "health/stress_log.html", {"form": form, "logs": logs})


@login_required(login_url="signup")
def reminders(request):
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            return redirect("health:reminders")
    else:
        form = ReminderForm()

    reminders = Reminder.objects.filter(user=request.user).order_by("time")
    return render(request, "health/reminders.html", {"form": form, "reminders": reminders})
