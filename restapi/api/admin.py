from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Comment, News, User

admin.site.register(News)
admin.site.register(Comment)
admin.site.register(User, UserAdmin)
