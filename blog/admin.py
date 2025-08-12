from django.contrib import admin
from .models import Post, AboutPage, ContactFormSubmission, ContactMessage
from django.db import models


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
@admin.register(ContactFormSubmission)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    readonly_fields = ('submitted_at',)
    search_fields = ('name', 'email')
    list_filter = ('submitted_at',)

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not AboutPage.objects.exists()
    
    def has_change_permission(self, request, obj=None):
        return True
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at', 'is_read')
    list_filter =('is_read','submitted_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('submitted_at',)
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    actions = [mark_as_read]