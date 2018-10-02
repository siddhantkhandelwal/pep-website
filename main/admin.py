from django.contrib import admin
from .models import Paper, ProfessorProfile, ParticipantProfile, Abstract, Category, College, StaffProfile


class ParticipantProfileAdmin(admin.ModelAdmin):
	list_display = ('author', 'coauthor', 'phone1', 'phone2', 'no_of_abstracts', 'college_name',)
	
	def no_of_abstracts(self, obj):
		return Abstract.objects.filter(participant = obj).count()

	def college_name(self, obj):
		return obj.college.name


class CollegeAdmin(admin.ModelAdmin):
	list_display = ('name', 'no_of_abstracts',)

	def no_of_abstracts(self, obj):
		return Abstract.objects.filter(participant__college = obj).count()
		

class ProfessorProfileAdmin(admin.ModelAdmin):
	list_display = ('display_name', 'category', 'phone1')


class StaffProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'allotted_categories', 'no_of_abstracts')
	
	def allotted_categories(self, obj):
		return ', '.join([category.name for category in obj.categories.all()])

	def no_of_abstracts(self, obj):
		return Abstract.objects.filter(staff=obj).count()


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'no_of_abstracts')
	def no_of_abstracts(self, obj):
		return Abstract.objects.filter(category=obj).count()


class AbstractAdmin(admin.ModelAdmin):
	list_display = ('uid', 'title')
	#list_display = ('uid', 'title', 'participant_author', 'participant_coauthor', 'professor_name', 'staff_handlers', 'status', 'college_name')

	'''
	def college_name(self, obj):
		return obj.participant.college.name

	def staff_handlers(self, obj):
		return [staff.user.username for staff in obj.staff.all()]

	def participant_author(self, obj):
		return obj.participant.author

	def participant_coauthor(self, obj):
		return obj.participant.coauthor

	def professor_name(self, obj):
		return obj.professor.display_name
	'''

admin.site.register(Category, CategoryAdmin)
admin.site.register(Paper)
admin.site.register(Abstract, AbstractAdmin)
admin.site.register(ParticipantProfile, ParticipantProfileAdmin)
admin.site.register(ProfessorProfile, ProfessorProfileAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(College, CollegeAdmin)
