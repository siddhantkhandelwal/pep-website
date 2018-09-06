from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Abstract, Paper


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('phone', 'category')

class AbstractForm(forms.ModelForm):
	class Meta:
		model = Abstract
		fields = ('title', 'author1', 'author2', 'document', 'category', 'professor')

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
