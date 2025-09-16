from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    @property
    def level(self):
        if self.xp >= 500:
            return "Master"
        elif self.xp >= 300:
            return "Expert"
        elif self.xp >= 150:
            return "Skilled"
        elif self.xp >= 50:
            return "Learner"
        return "Beginner"


class Roadmap(models.Model):
    TECH_CHOICES = [
        ("MERN Stack", "MERN Stack Development"),
        ("MEAN Stack", "MEAN Stack Development"),
        ("AI & Machine Learning", "AI & Machine Learning"),
        ("Python Development", "Python Development"),
        ("Data Analytics", "Data Analytics"),
        ("Cloud Computing", "Cloud Computing"),
        ("Cybersecurity", "Cybersecurity"),
        ("DevOps", "DevOps"),
        ("Blockchain", "Blockchain"),
        ("Mobile App Development", "Mobile App Development"),
        ("UI/UX Design", "UI/UX Design"),
        ("AR/VR Development", "AR/VR Development"),
        ("Data Science", "Data Science"),
        ("Game Development", "Game Development"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tech_stack = models.CharField(max_length=50, choices=TECH_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tech_stack} - {self.user.username}"

    @property
    def progress_percent(self):
        total = self.items.count()
        completed = self.items.filter(completed=True).count()
        return int((completed / total) * 100) if total > 0 else 0

    @property
    def badge(self):
        if self.progress_percent == 100:
            return "🏆 Mastery Badge"
        elif self.progress_percent >= 75:
            return "🔥 Expert Badge"
        elif self.progress_percent >= 50:
            return "⭐ Intermediate Badge"
        elif self.progress_percent >= 25:
            return "📘 Beginner Badge"
        return ""


class RoadmapItem(models.Model):
    roadmap = models.ForeignKey(Roadmap, related_name="items", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
