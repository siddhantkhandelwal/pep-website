from django.contrib import admin
from .models import Paper, UserProfile, Abstract

admin.site.register(Paper)
admin.site.register(Abstract)
admin.site.register(UserProfile)
