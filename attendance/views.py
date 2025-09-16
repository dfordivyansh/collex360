from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SubjectForm, MarkAttendanceForm
from .models import Subject, Timetable, AttendanceLog

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from statsmodels.tsa.arima.model import ARIMA


# ✅ Add new subject + assign it to selected days with lecture counts
@login_required(login_url="signup")
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()

            # Assign subject to selected days with lectures
            days = form.cleaned_data["days"]
            for d in days:
                lectures = form.cleaned_data.get(f"lectures_{d}", 1) or 1
                Timetable.objects.create(
                    user=request.user,
                    day=d,
                    subject=subject,
                    lectures=lectures
                )

            return redirect("attendance:dashboard")
    else:
        form = SubjectForm()
    return render(request, "attendance/add_subject.html", {"form": form})


# ✅ Mark attendance manually
@login_required(login_url="signup")
def mark_attendance(request):
    if request.method == "POST":
        form = MarkAttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            day = form.cleaned_data["day"]
            status = request.POST.get("status")  # "present" or "absent"

            # Find all subjects scheduled that day
            subjects_today = Timetable.objects.filter(user=request.user, day=day)

            for entry in subjects_today:
                lectures = entry.lectures or 1

                # Avoid duplicate logs → use update_or_create
                log, created = AttendanceLog.objects.update_or_create(
                    user=request.user,
                    subject=entry.subject,
                    date=date,
                    day=day,
                    defaults={
                        "lectures": lectures,
                        "present": (status == "present")
                    }
                )

                # Update subject counters (but only if log was newly created or status changed)
                if created or log.present != (status == "present"):
                    if created:
                        entry.subject.attendance_total += lectures
                        if status == "present":
                            entry.subject.attendance_present += lectures
                    else:
                        # If changed from absent → present
                        if status == "present" and not log.present:
                            entry.subject.attendance_present += lectures
                        # If changed from present → absent
                        elif status == "absent" and log.present:
                            entry.subject.attendance_present -= lectures

                    entry.subject.save()

            return redirect("attendance:dashboard")
    else:
        form = MarkAttendanceForm()

    return render(request, "attendance/mark_attendance.html", {"form": form})


# ✅ Dashboard with stats + AI insights
@login_required(login_url="signup")
def dashboard(request):
    subjects = Subject.objects.filter(user=request.user)

    # Handle Actions (POST requests)
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        action = request.POST.get("action")

        try:
            subject = subjects.get(id=subject_id)
        except Subject.DoesNotExist:
            return redirect("attendance:dashboard")

        if action == "present":
            subject.attendance_total += 1
            subject.attendance_present += 1
        elif action == "add":
            subject.attendance_total += 1
        elif action == "remove" and subject.attendance_total > 0:
            subject.attendance_total -= 1
            if subject.attendance_present > subject.attendance_total:
                subject.attendance_present = subject.attendance_total  
        elif action == "delete":
            subject.delete()
            return redirect("attendance:dashboard")

        subject.save()
        return redirect("attendance:dashboard")

    # --- Stats per subject with AI insights ---
    subject_data = []
    for subj in subjects:
        percentage = round((subj.attendance_present / subj.attendance_total) * 100, 2) if subj.attendance_total > 0 else 0
        forecast = subj.forecast_attendance(classes_left=30) if hasattr(subj, "forecast_attendance") else None
        required = subj.required_days_to_reach(target=75) if hasattr(subj, "required_days_to_reach") else None
        risk = forecast is not None and forecast < 75

        # --- AI Insights ---
        prob_safe = None
        forecast_trend = None

        # Logistic Regression Prediction
        if subj.attendance_total > 5:
            X = np.array([[i] for i in range(1, subj.attendance_total + 1)])
            y = np.array([1 if i <= subj.attendance_present else 0 for i in range(1, subj.attendance_total + 1)])

            if len(np.unique(y)) > 1:
                try:
                    model = LogisticRegression()
                    model.fit(X, y)
                    prob_safe = model.predict_proba([[subj.attendance_total + 5]])[0][1]
                    prob_safe = round(prob_safe * 100, 2)
                except Exception:
                    prob_safe = None
            else:
                prob_safe = 100 if subj.attendance_present == subj.attendance_total else 0

        # ARIMA Forecast (FIXED)
        logs = AttendanceLog.objects.filter(user=request.user, subject=subj).order_by("date")
        if logs.count() > 5:
            df = pd.DataFrame.from_records(logs.values("date", "present"))
            df["date"] = pd.to_datetime(df["date"])
            df = df.groupby("date").mean()   # ✅ group by date to remove duplicates
            df = df.asfreq("D").fillna(0)    # ✅ safe to reindex now

            try:
                model = ARIMA(df["present"], order=(1, 1, 1))
                fit = model.fit()
                forecast_val = fit.forecast(steps=7).mean()
                forecast_trend = round(forecast_val * 100, 2)
            except Exception:
                forecast_trend = None

        subject_data.append({
            "id": subj.id,
            "name": subj.name,
            "attendance_present": subj.attendance_present,
            "attendance_total": subj.attendance_total,
            "percentage": percentage,
            "forecast": forecast,
            "required": required,
            "risk": risk,
            "prob_safe": prob_safe,
            "forecast_trend": forecast_trend,
        })

    # --- Overall Stats ---
    total_classes = sum(s.attendance_total for s in subjects)
    total_present = sum(s.attendance_present for s in subjects)
    overall_pct = round((total_present / total_classes) * 100, 2) if total_classes > 0 else 0

    required_days = 0
    if overall_pct < 75 and total_classes > 0:
        while (total_present + required_days) / (total_classes + required_days) * 100 < 75:
            required_days += 1

    return render(request, "attendance/dashboard.html", {
        "subjects": subject_data,
        "overall_pct": overall_pct,
        "required_days": required_days,
        "total_classes": total_classes,
    })
