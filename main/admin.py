from django.contrib import admin
from .models import Paper, ProfessorProfile, ParticipantProfile, Abstract, Category, College


admin.site.register(Category)
admin.site.register(Paper)
admin.site.register(Abstract)
admin.site.register(ParticipantProfile)
admin.site.register(ProfessorProfile)
admin.site.register(College)
