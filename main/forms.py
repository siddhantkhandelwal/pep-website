from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Abstract



class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('is_professor', 'phone')

class AbstractForm(forms.ModelForm):
	class Meta:
		model = Abstract
		fields = ('title', 'author1', 'author2', 'document')