from django.contrib import admin
from .models import Paper, ProfessorProfile, ParticipantProfile, Abstract, Category, College, StaffProfile, SupervisorProfile


class ParticipantProfileAdmin(admin.ModelAdmin):
    list_display = ('author', 'coauthor', 'phone1', 'phone2',
                    'no_of_abstracts', 'college_name',)

    def no_of_abstracts(self, obj):
        return Abstract.objects.filter(participant=obj).count()

    def college_name(self, obj):
        return obj.college.name


class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'no_of_abstracts',)

    def no_of_abstracts(self, obj):
        return Abstract.objects.filter(participant__college=obj).count()


class ProfessorProfileAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'category', 'phone1')


class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'allotted_categories', 'staff_allotted')

    def staff_allotted(self, obj):
        staff_allotted_list = []
        for supervisor_category in obj.categories.all():
            for staff in StaffProfile.objects.all():
                for staff_category in staff.categories.all():
                    if supervisor_category == staff_category:
                        if staff not in staff_allotted_list:
                            staff_allotted_list.append(staff)
        return staff_allotted_list

    def allotted_categories(self, obj):
        return ', '.join([category.name for category in obj.categories.all()])


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
    list_display = ('uid', 'title', 'category', 'participant_author', 'participant_coauthor',
                    'professor_name', 'staff_handlers', 'status', 'verdict', 'college_name')

    def college_name(self, obj):
        return obj.participant.college.name

    def staff_handlers(self, obj):
        return [staff.user.username for staff in obj.staff.all()]

    def participant_author(self, obj):
        return obj.participant.author

    def participant_coauthor(self, obj):
        return obj.participant.coauthor

    def professor_name(self, obj):
        if obj.professor is not None:
            return obj.professor.display_name
        else:
            return 'NA'


class PaperAdmin(admin.ModelAdmin):
    list_display = ('abstract', 'title', 'document', 'category', 'participant_author',
                    'participant_coauthor', 'professor_name', 'staff_handlers', 'status', 'verdict', 'college_name')

    def title(self, obj):
        return obj.abstract.title

    def category(self, obj):
        return obj.abstract.category.name

    def college_name(self, obj):
        return obj.abstract.participant.college.name

    def staff_handlers(self, obj):
        return [staff.user.username for staff in obj.abstract.staff.all()]

    def participant_author(self, obj):
        return obj.abstract.participant.author

    def participant_coauthor(self, obj):
        return obj.abstract.participant.coauthor

    def professor_name(self, obj):
        if obj.abstract.professor is not None:
            return obj.abstract.professor.display_name
        else:
            return 'NA'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Abstract, AbstractAdmin)
admin.site.register(ParticipantProfile, ParticipantProfileAdmin)
admin.site.register(ProfessorProfile, ProfessorProfileAdmin)
admin.site.register(SupervisorProfile, SupervisorProfileAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(College, CollegeAdmin)
