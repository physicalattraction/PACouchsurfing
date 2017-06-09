from django.contrib import admin

from cs_profile.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Profile detail
    fields = ('id', 'public_name', 'public_address', 'avatar_url', 'is_verified', 'is_deleted',)
    readonly_fields = ('id',)

    # Profile list
    list_filter = ('is_verified', 'is_deleted',)
    list_display = ('id', 'public_name', 'avatar_url', 'is_verified', 'is_deleted',)
    list_display_links = ('id',)
    search_fields = ('public_name', 'avatar_url',)
