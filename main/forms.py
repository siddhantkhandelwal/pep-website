from django import forms
from django.contrib.auth.models import User
from .models import ProfessorProfile, ParticipantProfile, Abstract, Paper


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class PasswordResetForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('password',)

class ParticipantProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ParticipantProfileForm, self).__init__(*args, **kwargs)
		self.fields['college'].required=True
	class Meta:
		model = ParticipantProfile
		fields = ('author1', 'author2', 'phone1', 'phone2', 'college')

class AbstractForm(forms.ModelForm):
	class Meta:
		model = Abstract
		fields = ('title', 'document', 'category', 'participant')

class PaperForm(forms.ModelForm):
	class Meta:
		model = Paper
		fields = ('document', 'abstract')

class AbstractReviewForm(forms.ModelForm):
	class Meta:
		model = Abstract
		fields = ('review',)
		widgets = {
            'review': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }
	
class PaperReviewForm(forms.ModelForm):
	class Meta:
		model = Paper
		fields = ('review',)
		widgets = {
            'review': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }
