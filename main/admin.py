from django.contrib import admin
from .models import Paper, ProfessorProfile, ParticipantProfile, Abstract, Category, College


class ParticipantProfileAdmin(admin.ModelAdmin):
	list_display = ('author1', 'author2', 'college', 'phone1', 'no_of_abstracts')
	def no_of_abstracts(self, obj):
		return Abstract.objects.filter(participant = obj).count()

class ProfessorProfileAdmin(admin.ModelAdmin):
	list_display = ('display_name', 'category', 'phone1')


admin.site.register(Category)
admin.site.register(Paper)
admin.site.register(Abstract)
admin.site.register(ParticipantProfile, ParticipantProfileAdmin)
admin.site.register(ProfessorProfile, ProfessorProfileAdmin)
admin.site.register(College)
