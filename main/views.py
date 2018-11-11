from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, AbstractForm, PaperForm, AbstractReviewForm, PaperReviewForm, ParticipantProfileForm, PasswordResetForm, AssignProfessorForm
from django.contrib.auth import authenticate, login, logout
from .models import Abstract, Paper, ParticipantProfile, ProfessorProfile, StaffProfile, College, SupervisorProfile
from django.contrib.auth.decorators import login_required

import sendgrid
import os
from sendgrid.helpers.mail import *

	
def paper_presentation(request):
	return HttpResponseRedirect(reverse('main:portal'))
	#return render(request, 'main/paper-presentation/paper-presentation.html', {})

def about(request):
	return render(request, 'main/paper-presentation/about.html', {})

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('main:portal'))
	
	colleges = College.objects.all()
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		participant_profile_form = ParticipantProfileForm(data=request.POST)

		if user_form.is_valid() and participant_profile_form.is_valid():
			user = user_form.save(commit=False)
			user.set_password(user.password)
			user.save()

			participant_profile = participant_profile_form.save(commit=False)
			participant_profile.user = user
			participant_profile.save()

			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('main:portal'))
			else:
				return render(request, 'main/paper-presentation/login.html', {'login_form_errors': 'Your account is disabled'})
			return HttpResponseRedirect(reverse('main:user_login'))
		else:
			print(user_form.errors, participant_profile_form.errors)
	else:
		user_form = UserForm()
		participant_profile_form = ParticipantProfileForm()
	return render(request, 
		'main/paper-presentation/register.html',
		{'user_form': user_form,
		'participant_profile_form': participant_profile_form,
		'colleges': colleges
		})

def user_login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('main:portal'))
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('main:portal'))

			else:
				return render(request, 'main/paper-presentation/login.html', {'login_form_errors': 'Your account is disabled'})
		else:
			return render(request, 'main/paper-presentation/login.html', {'login_form_errors': 'Invalid Username/Password'})
	else:
		return render(request, 'main/paper-presentation/login.html', {})

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('main:user_login'))

@login_required
def user_password_reset(request):
	if request.method == 'POST':
		user = request.user
		password_reset_form = PasswordResetForm(data=request.POST, instance=user)
		if password_reset_form.is_valid():
			user = password_reset_form.save(commit=False)
			user.set_password(user.password)
			user.save()
			return HttpResponseRedirect(reverse('main:user_login'))
	else:
		password_reset_form = PasswordResetForm()
	return render(request, 'main/paper-presentation/password-reset.html', {'password_reset_form': password_reset_form})

@login_required
def edit_profile(request):
	if request.method == 'POST':
		user = request.user
		user_profile_form = ParticipantProfileForm(data=request.POST, instance=user)
		if user_profile_form.is_valid():
			user_profile = user_profile_form.save()
			return HttpResponseRedirect(reverse('main:portal'))
	else:
		user_profile_form = ParticipantProfileForm()
	return render(request, 'main/paper-presentation/edit-profile.html', {'user_profile_form': user_profile_form})

@login_required
def portal(request):
	if request.user.is_superuser:
		#return HttpResponseRedirect('/admin')
		return HttpResponseRedirect('/paper-presentation/admin')

	if SupervisorProfile.objects.filter(user=request.user):
		user_profile = SupervisorProfile.objects.get(user=request.user)
		access_level = 3
		staff_allotted_list = []
		for supervisor_category in user_profile.categories.all():
			for staff in StaffProfile.objects.all():
				for staff_category in staff.categories.all():
					if supervisor_category == staff_category:
						if staff not in staff_allotted_list:
							staff_allotted_list.append(staff)
		print(staff_allotted_list)
		
		abstracts_allotted = []
		for abstract in Abstract.objects.filter(staff__in=staff_allotted_list):
			if abstract not in abstracts_allotted:
				abstracts_allotted.append(abstract)

		professors = ProfessorProfile.objects.all()
		assign_professor_form = AssignProfessorForm()
		return render(request, 'main/paper-presentation/portal.html', {'user_profile': user_profile,
				      												   'access_level': access_level,
				      												   'staff_allotted_list': staff_allotted_list,
				      												   'abstracts_allotted': abstracts_allotted,
																	   'professors': professors,
														               'assign_professor_form': assign_professor_form})
	
	elif StaffProfile.objects.filter(user=request.user):
		user_profile = StaffProfile.objects.get(user=request.user)
		access_level = 2
		abstracts_allotted = Abstract.objects.filter(staff=user_profile)
		professors = ProfessorProfile.objects.all()
		#professors = ProfessorProfile.objects.filter(category_id__in=[category.id for category in user_profile.categories.all()]) 
		assign_professor_form = AssignProfessorForm()
		return render(request, 'main/paper-presentation/portal.html', {'user_profile': user_profile,
													#'categories': categories,
													'access_level': access_level,
													'abstracts_allotted': abstracts_allotted,
													'professors': professors,
													'assign_professor_form': assign_professor_form})
	
	elif ProfessorProfile.objects.filter(user=request.user):	
		user_profile = ProfessorProfile.objects.get(user=request.user)
		access_level = 1
		abstracts_allotted = Abstract.objects.filter(professor=user_profile)
		papers_allotted = []
		papers = Paper.objects.all()
		for paper in papers:
			if paper.abstract in abstracts_allotted:
				papers_allotted.append(paper)
				abstracts_allotted = abstracts_allotted.exclude(uid=paper.abstract.uid)
		return render(request, 'main/paper-presentation/portal.html', {'user_profile': user_profile,
													'abstracts_allotted': abstracts_allotted,
													'papers_allotted': papers_allotted,
													'access_level': access_level})

	else:
		user_profile = ParticipantProfile.objects.get(user=request.user)
		participant_abstracts = Abstract.objects.filter(participant=user_profile)
		participant_papers = []
		for paper in Paper.objects.all():
			if paper.abstract in participant_abstracts:
				participant_papers.append(paper)
				participant_abstracts = participant_abstracts.exclude(uid=paper.abstract.uid)
		access_level = 0
		return render(request, 'main/paper-presentation/portal.html', {'abstracts': participant_abstracts,
																		'papers': participant_papers,
																		'access_level': access_level,
																		'user_profile': user_profile})

@login_required
def abstract_submission(request):
	if request.method == 'POST':
		user_profile = ParticipantProfile.objects.get(user = request.user)
		abstract_form = AbstractForm(request.POST, request.FILES)
		if abstract_form.is_valid():
			abstract = abstract_form.save(commit=False)
			if abstract.document.name.split('.')[1] != 'pdf':
				return render(request, 'main/paper-presentation/abstract-upload.html', {'abstract_upload_form_errors': 'Only PDF file format is Supported',
																						'abstract_form': abstract_form, })
			abstract.participant = user_profile
			for staff in StaffProfile.objects.filter(categories__in=[abstract.category]):
				abstract.staff.add(staff)
			abstract.document.name = str(abstract.uid) + '-' + abstract.title + '.' + abstract.document.name.split('.')[1]
			abstract.save()
			
			sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
			from_email = Email("pep@bits-apogee.org")
			to_email = Email(user_profile.user.email)
			subject = "Paper Presentation Event"
			msg = abstract.title + str(abstract.uid) + abstract.participant.author
			content = Content("text/plain", msg)
			mail = Mail(from_email, subject, to_email, content)
			response = sg.client.mail.send.post(request_body=mail.get())
			print(response.status_code)
			print(response.body)
			print(response.headers)
			
			return HttpResponseRedirect(reverse('main:portal'))
	else:
		abstract_form = AbstractForm()
	return render(request, 'main/paper-presentation/abstract-upload.html', {'abstract_form': abstract_form})

@login_required
def abstract_review(request, pk):
	abstract = get_object_or_404(Abstract, pk=pk)
	if request.method == 'POST':
		abstract_review_form = AbstractReviewForm(request.POST, instance=abstract)
		if abstract_review_form.is_valid():
			abstract = abstract_review_form.save(commit=False)
			abstract.status = 'AC'
			abstract.save()
			return HttpResponseRedirect(reverse('main:portal'))
	else:
		abstract_review_form = AbstractReviewForm()	
	return render(request, 'main/paper-presentation/abstract-review.html', {'abstract_review_form': abstract_review_form,
																			'abstract': abstract})

@login_required
def paper_submission(request):
	user_profile = ParticipantProfile.objects.get(user=request.user)
	if request.method == 'POST':
		paper_form = PaperForm(request.POST, request.FILES)
		if paper_form.is_valid():
			paper = paper_form.save(commit=False)
			paper.document.name = str(paper.abstract.uid) + '-' + paper.abstract.title + '.' + paper.document.name.split('.')[1]
			paper.save()
			return HttpResponseRedirect(reverse('main:portal'))
	else:
		paper_form = PaperForm()
	return render(request, 'main/paper-presentation/paper-upload.html', {'paper_form': paper_form})
																	  
@login_required
def paper_review(request, pk):
	abstract = get_object_or_404(Abstract, pk=pk)
	paper = get_object_or_404(Paper, abstract=abstract) 
	if request.method == 'POST': 
		paper_review_form = PaperReviewForm(request.POST, instance=paper)
		if paper_review_form.is_valid():
			paper = paper_review_form.save(commit=False)
			paper.status = 'PC'
			paper.save()
			return HttpResponseRedirect(reverse('main:portal'))
	else:
		paper_review_form = PaperReviewForm()
	return render(request, 'main/paper-presentation/paper-review.html', {'paper_review_form': paper_review_form,
																		 'abstract': abstract,
																		 'paper': paper})

def assign_professor(request, pk):
	abstract = get_object_or_404(Abstract, pk=pk)
	if request.method == 'POST':
		professor_select = request.POST.get('professor')
		professor = ProfessorProfile.objects.get(user_id=professor_select)
		abstract = Abstract.objects.get(pk=pk)
		abstract.professor = professor
		abstract.save()
		return HttpResponseRedirect(reverse('main:portal'))
	return HttpResponseRedirect(reverse('main:portal'))
