from django.contrib import admin
from .models import Paper, UserProfile, Abstract, Category, College


admin.site.register(Category)
admin.site.register(Paper)
admin.site.register(Abstract)
admin.site.register(UserProfile)
admin.site.register(College)
