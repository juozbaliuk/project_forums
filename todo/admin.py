from django.contrib import admin
from .models import CustomUser, Task, Forum, Category, Topic, Tag, Post
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

class TagInline(admin.TabularInline):
    model = Topic.tags.through

class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'content', 'user', 'datetime']
    
    fieldsets = [
        (_("General"), {
            'fields': ('name', 'content', 'user', 'datetime')
        }),
    ]

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_("Additional info"), {"fields": ("photo", "flair", )}),
    )
    
class ForumAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'category']
    
    fieldsets = [
        (_("General"), {
            'fields': ('name', 'description', 'category')
        }),
    ]
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'staff_only']
    list_editable = ['staff_only']
    
    fieldsets = [
        (_("General"), {
            'fields': ('name', 'description', 'staff_only')
        }),
    ]
    
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'forum', 'get_tags', 'pinned', 'locked']
    list_editable = ['pinned', 'locked']
    inlines = [TagInline]
    
    fieldsets = [
        (_("General"), {
            'fields': ('name', 'forum')
        }),
    ]

class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    
    fieldsets = [
        (_("General"), {
            'fields': ('name', 'description')
        }),
    ]    

class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'content', 'created_at', 'last_edited']
    
    fieldsets = [
        (_("General"), {
            'fields': ('user', 'topic', 'content', 'created_at', 'last_edited')
        }),
    ]    

# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)