from django.contrib import admin
from .models import Subject, Timetable, AttendanceLog


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "attendance_present", "attendance_total", "percentage")
    list_filter = ("user",)
    search_fields = ("name", "user__username")


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ("user", "day", "subject")
    list_filter = ("day", "user")
    search_fields = ("subject__name", "user__username")


@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "day", "present", "created_at")
    list_filter = ("day", "present", "user")
    search_fields = ("user__username",)
    ordering = ("-date",)
