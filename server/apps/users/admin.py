from django.contrib import admin
from server.apps.users.models import User, UserActivity

admin.site.register(User)
admin.site.register(UserActivity)
