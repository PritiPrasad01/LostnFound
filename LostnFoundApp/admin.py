from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Post,
    Profile,
    Comment,
)

@admin.register(Post)
class LostModelAdmin(admin.ModelAdmin):
    list_display = [
            'title','location','description','category','product_image',
    ]

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = [
            'user','phone_num','gender','profile_pic','birth_date',
    ]

# @admin.register(Comment)
# class CommentModelAdmin(admin.ModelAdmin):
#     list_display = [
#             'post','user_name','subject','comment','create_at','update_at','ip','status',
#     ]
#     list_filter = ['create_at', 'user_name']
#     search_fields = ['comment']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user', 'post__title')
