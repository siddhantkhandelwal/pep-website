from django.contrib import admin
from .models import Paper, UserProfile, Abstract, Category


admin.site.register(Category)
admin.site.register(Paper)
admin.site.register(Abstract)
admin.site.register(UserProfile)
