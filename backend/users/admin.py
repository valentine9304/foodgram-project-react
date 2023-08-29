from django.contrib import admin

from .models import User, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
    )
    search_fields = ("username", "email")
    list_filter = ("role",)
    empty_value_display = "Empty"
    list_editable = ("role",)


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author",
    )


admin.site.register(Follow, FollowAdmin)
admin.site.register(User, UserAdmin)
