from django.db import models
from django.contrib.auth.models import User
import random
from datetime import datetime


class Category(models.Model):
	name = models.CharField('Category Name', max_length=200)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name


class College(models.Model):
	name = models.CharField('College/University Name', max_length=500)

	def __str__(self):
		return self.name


class StaffProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	categories = models.ManyToManyField(Category)

	def __str__(self):
		return self.user.username
	

class ProfessorProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	display_name = models.CharField('Display Name', max_length=200, null=True)
	phone1 = models.BigIntegerField('Phone', null=True)
	phone2 = models.BigIntegerField('Alternate Phone', null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) 

	def __str__(self):
		return self.display_name + ' - ' + self.category.name
	
	class Meta:
		ordering = ['category']


class ParticipantProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	author1 = models.CharField('Author 1', max_length=200)
	author2 = models.CharField('Author 2', max_length=200, null=True, blank=True)
	phone1 = models.BigIntegerField('Phone', null=True)
	phone2 = models.BigIntegerField('Alternate Phone', null=True, blank=True)
	college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
	
	def __str__(self):
		if self.author2:
			return self.user.username + ' - ' + self.author1 + ', ' + self.author2
		else:
			return self.user.username + ' - ' + self.author1
		

class Abstract(models.Model):
	def generate_uid():
		random.seed(datetime.now())
		temp_uid = random.randint(0, 1000)
		while(uid(temp_uid) == False):
			temp_uid = random.randint(0, 1000)
		return temp_uid
	
	title = models.CharField('Abstract Title', max_length=200)
	submission_date = models.DateTimeField('Date Submitted', auto_now_add=True)
	uid = models.IntegerField('UID', primary_key=True, default=generate_uid)
	participant = models.ForeignKey(ParticipantProfile, on_delete=models.SET_NULL, null=True)
	file_name = ''
	document = models.FileField(upload_to='documents/abstracts/' + file_name)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	professor = models.ForeignKey(ProfessorProfile, on_delete=models.SET_NULL, null=True)
	staff = models.ManyToManyField(StaffProfile)
	review = models.TextField(null=True, blank=True)
	verdict_choices = (
		('ASel', 'Abstract Selected'),
		('ARej', 'Abstract Rejected'),
		('AMod', 'Acceptable after changes'))
	verdict = models.CharField(
		max_length=4,
		choices=verdict_choices,
		null=True,
		blank=True)
	status_choices = (
		('AS', 'Abstract Submitted'),
		('AC', 'Abstract Checked'),
		)
	status = models.CharField(
		max_length=2,
		choices=status_choices,
		default='AS') 

	class Meta:
		ordering = ['uid']

	def return_file_path(self):
		self.file_name = 'documents/abstracts/' + self.uid + '-' + self.title
	def __str__(self):
		return self.title + '-' + self.participant.author1


class Paper(models.Model):
	abstract = models.OneToOneField(Abstract, on_delete=models.CASCADE)
	submission_date = models.DateTimeField('Date Submitted', auto_now_add=True)
	document = models.FileField(upload_to='documents/papers/')
	review = models.TextField(null=True)
	status_choices = (
		('PS', 'Paper Submitted'),
		('PC', 'Paper Checked'),
		)
	status = models.CharField(
		max_length=2,
		choices=status_choices,
		default='PS')
	verdict_choices = (
		('PSel', 'Abstract Selected'),
		('PRej', 'Abstract Rejected'))
	verdict = models.CharField(
		max_length=4,
		choices=verdict_choices,
		null=True) 

	def __str__(self):
		return self.abstract.title + '-' + self.abstract.participant.author1


def uid(temp_uid):
	abstracts = Abstract.objects.all()
	for abstract in abstracts:
		if abstract.uid == temp_uid:
			return False
