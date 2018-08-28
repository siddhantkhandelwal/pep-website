from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	is_professor = models.BooleanField('Is Professor?', default=False)
	phone = models.BigIntegerField('Phone')

	def __str__(self):
		return self.user.username


class Paper(models.Model):
	title = models.CharField('Paper Title', max_length=200)
	submission_date = models.DateTimeField('Date Submitted')
	uid = models.IntegerField('UID', primary_key=True)
	author1 = models.CharField('Author 1', max_length=100, blank=True)
	author2 = models.CharField('Author 2', max_length=100, blank=True)
	#professor = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
	status_choices = (
		('AS', 'Abstract Submitted'),
		('AC', 'Abstract Checked'),
		('PS', 'Paper Submitted'),
		('PC', 'Paper Checked'),
		)
	status = models.CharField(
		max_length=2,
		choices=status_choices,
		default='AS') 

	class Meta:
		ordering = ['uid']

	def __str__(self):
		return self.title + '-' + self.author1
