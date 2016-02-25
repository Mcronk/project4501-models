from django.contrib import admin

from .models import Course, User, Session

admin.site.register(Course)
admin.site.register(User)
admin.site.register(Session)
