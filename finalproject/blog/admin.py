from django.contrib import admin
from .models import Post, User, UserProfile


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'published')
    list_filter = ('published', 'created_at', 'user')
    search_fields = ('title', 'body')
    raw_id_fields = ('user',)
    date_hierarchy = 'published'
    ordering = ['published']


admin.site.register(Post, PostAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date']


admin.site.register(UserProfile, UserProfileAdmin)

