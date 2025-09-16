from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    attendance_total = models.PositiveIntegerField(default=0)
    attendance_present = models.PositiveIntegerField(default=0)

    # ✅ New AI-related fields
    target_percentage = models.FloatField(default=75)  # threshold for warning
    last_updated = models.DateTimeField(auto_now=True)  # track updates for anomaly detection
    attendance_history = models.JSONField(default=list, blank=True)  
    # Example: [{"date": "2025-08-30", "status": "present"}]

    def percentage(self):
        """Return attendance percentage"""
        if self.attendance_total == 0:
            return 0
        return round((self.attendance_present / self.attendance_total) * 100, 2)

    def forecast_attendance(self, classes_left=30):
        """Naive forecast: assumes same attendance rate continues"""
        if self.attendance_total == 0:
            return 0
        current_rate = self.attendance_present / self.attendance_total
        predicted_present = self.attendance_present + (classes_left * current_rate)
        predicted_total = self.attendance_total + classes_left
        return round((predicted_present / predicted_total) * 100, 2)

    def required_days_to_reach(self, target=None):
        """How many more classes are needed to reach target%"""
        if target is None:
            target = self.target_percentage
        if self.attendance_total == 0:
            return 0
        present, total = self.attendance_present, self.attendance_total
        needed = 0
        while total > 0 and (present / total) * 100 < target:
            present += 1
            total += 1
            needed += 1
        return needed

    def log_attendance(self, date, status):
        """
        Update attendance + save history record (for AI analysis).
        status = "present" or "absent"
        """
        self.attendance_total += 1
        if status == "present":
            self.attendance_present += 1

        # save history entry
        history_entry = {"date": str(date), "status": status}
        self.attendance_history.append(history_entry)

        self.save()

    def __str__(self):
        return f"{self.name} ({self.user})"


class Timetable(models.Model):
    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=DAYS)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lectures = models.PositiveIntegerField(default=1)   # number of lectures for that subject on that day

    class Meta:
        unique_together = ("user", "day", "subject")  # prevents duplicates

    def __str__(self):
        return f"{self.get_day_display()} - {self.subject} ({self.lectures} lectures)"


class AttendanceLog(models.Model):
    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    day = models.CharField(max_length=3, choices=DAYS)  # restrict values to fixed days
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="attendance_logs")
    lectures = models.PositiveIntegerField(default=1)  # number of lectures for subject on that day
    present = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "subject"]  # newest logs first
        unique_together = ("user", "date", "day", "subject")  # Prevents duplicate logs for same subject/day

    def __str__(self):
        status = "Present" if self.present else "Absent"
        return f"{self.user} - {self.date} ({self.get_day_display()}) - {self.subject.name} [{self.lectures} lecture(s)] - {status}"

    @property
    def is_absent(self):
        """Quick check if user was absent"""
        return not self.present
