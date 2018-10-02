from django.db import models
from django.contrib.auth.models import User
import random
from datetime import datetime


class Category(models.Model):
	name = models.CharField('Category Name', max_length=200)

	class Meta:
		verbose_name_plural = 'Categories'


class College(models.Model):
	name = models.CharField('College/University Name', max_length=500)

	class Meta:
		ordering = ['name']


class StaffProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	categories = models.ManyToManyField(Category)


class ProfessorProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	display_name = models.CharField('Display Name', max_length=200, null=True)
	phone1 = models.BigIntegerField('Phone', null=True)
	phone2 = models.BigIntegerField('Alternate Phone', null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) 
	
	class Meta:
		ordering = ['category']


class ParticipantProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	author = models.CharField('Author', max_length=200)
	coauthor = models.CharField('Co-Author', max_length=200, null=True, blank=True)
	phone1 = models.BigIntegerField('Phone', null=True)
	phone2 = models.BigIntegerField('Alternate Phone', null=True, blank=True)
	college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
			

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


def uid(temp_uid):
	abstracts = Abstract.objects.all()
	for abstract in abstracts:
		if abstract.uid == temp_uid:
			return False
