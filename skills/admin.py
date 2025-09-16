from django.contrib import admin
from .models import Profile, Roadmap, RoadmapItem


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "xp", "streak", "last_active", "level")
    search_fields = ("user__username",)
    list_filter = ("last_active",)


class RoadmapItemInline(admin.TabularInline):  # Inline to show items inside Roadmap
    model = RoadmapItem
    extra = 1


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ("tech_stack", "user", "created_at", "progress_percent", "badge")
    list_filter = ("tech_stack", "created_at")
    search_fields = ("user__username", "tech_stack")
    inlines = [RoadmapItemInline]  # Show items in the roadmap admin


@admin.register(RoadmapItem)
class RoadmapItemAdmin(admin.ModelAdmin):
    list_display = ("title", "roadmap", "completed")
    list_filter = ("completed", "roadmap__tech_stack")
    search_fields = ("title", "roadmap__user__username")
