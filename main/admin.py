from django.contrib import admin
from .models import Paper, ProfessorProfile, ParticipantProfile, Abstract, Category, College, StaffProfile


class ParticipantProfileAdmin(admin.ModelAdmin):
	list_display = ('author', 'coauthor', 'phone1', 'phone2', 'no_of_abstracts','college',)
	def no_of_abstracts(self, obj):
		return Abstract.objects.filter(participant = obj).count()

class CollegeAdmin(admin.ModelAdmin):
	list_display = ('name', 'no_of_abstracts',)
	def no_of_abstracts(self, obj):
		return Abstract.objects.filter(participant__college = obj).count()
		
class ProfessorProfileAdmin(admin.ModelAdmin):
	list_display = ('display_name', 'category', 'phone1')

class StaffProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'allotted_categories')
	def allotted_categories(self, obj):
		return ', '.join([category.name for category in obj.categories.all()])

admin.site.register(Category)
admin.site.register(Paper)
admin.site.register(Abstract)
admin.site.register(ParticipantProfile, ParticipantProfileAdmin)
admin.site.register(ProfessorProfile, ProfessorProfileAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(College, CollegeAdmin)
