from django.contrib import admin

from cs_profile.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Profile detail
    readonly_fields = ('id',)
    exclude = ('__none__',)

    # Profile list
    list_filter = ('is_verified', 'is_deleted',)
    list_display = ('id', 'public_name', 'avatar_url', 'is_verified', 'is_deleted',)
    list_display_links = ('id',)
    search_fields = ('public_name', 'avatar_url',)
