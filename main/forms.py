from django import forms
from django.contrib.auth.models import User
from .models import ProfessorProfile, ParticipantProfile, Abstract, Paper


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ParticipantProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParticipantProfileForm, self).__init__(*args, **kwargs)
        self.fields['college'].required = True

    class Meta:
        model = ParticipantProfile
        fields = ('author', 'coauthor', 'phone1', 'phone2', 'college')


class AssignProfessorForm(forms.ModelForm):
    class Meta:
        model = Abstract
        fields = ('professor',)


class AbstractForm(forms.ModelForm):
    class Meta:
        model = Abstract
        fields = ('title', 'document', 'category')


class PaperForm(forms.ModelForm):

    class Meta:
        model = Paper
        fields = ('abstract','document',)

class PaperAbstractNewForm(forms.ModelForm):

    class Meta:
        model = Paper
        fields = ('document',)

class AbstractReUploadForm(forms.ModelForm):
    class Meta:
        model = Abstract
        fields = ('document',)

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
