from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, UserProfileForm, AbstractForm, PaperForm, AbstractReviewForm, PaperReviewForm, ParticipantProfileForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from .models import Abstract, Paper, UserProfile
from django.contrib.auth.decorators import login_required


def think_again(request):
	return render(request, 'main/think-again.html', {})

def paper_presentation(request):
	return render(request, 'main/paper-presentation/paper-presentation.html', {})

def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('dashboard'))
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		participant_profile_form = ParticipantProfileForm(data=request.POST)

		if user_form.is_valid() and participant_profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			participant_profile = participant_profile_form.save(commit=False)
			participant_profile.user = user

			participant_profile.save()
			return HttpResponseRedirect(reverse('user_login'))
		else:
			print(user_form.errors, participant_profile_form.errors)
	else:
		user_form = UserForm()
		participant_profile_form = ParticipantProfileForm()

	return render(request, 
		'main/paper-presentation/register.html',
		{'user_form': user_form,
		'participant_profile_form': participant_profile_form,
		})

def user_login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('dashboard'))
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('dashboard'))

			else:
				return HttpResponse("Your account is disabled.")
		else:
			return HttpResponse("Invalid Login Details Supplied.")
	else:
		return render(request, 'main/paper-presentation/login.html', {})

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('user_login'))

@login_required
def user_password_reset(request):
	if request.method == 'POST':
		user = request.user
		password_reset_form = PasswordResetForm(data=request.POST, instance=user)
		if password_reset_form.is_valid():
			user = password_reset_form.save(commit=False)
			user.set_password(user.password)
			user.save()
			return HttpResponseRedirect(reverse('user_login'))
	else:
		password_reset_form = PasswordResetForm()
	return render(request, 'main/paper-presentation/password-reset.html', {'password_reset_form': password_reset_form})

def abstract_submission(request):
	if request.method == 'POST':
		user_profile = UserProfile.objects.get(user = request.user)
		abstract_form = AbstractForm(request.POST, request.FILES)
		if abstract_form.is_valid():
			abstract = abstract_form.save(commit=False)
			abstract.author1 = user_profile
			abstract.save()
			return HttpResponseRedirect(reverse('dashboard'))
	else:
		abstract_form = AbstractForm()
	return render(request, 'main/paper-presentation/abstract-upload.html', {'abstract_form': abstract_form})

def paper_submission(request):
	if request.method == 'POST':
		paper_form = PaperForm(request.POST, request.FILES)
		if paper_form.is_valid():
			paper_form.save()
			return HttpResponseRedirect(reverse('dashboard'))
	else:
		paper_form = PaperForm()
	return render(request, 'main/paper-presentation/paper-upload.html', {'paper_form': paper_form})

@login_required
def dashboard(request):
	if request.user.is_superuser:
		return HttpResponseRedirect('/admin')
	user_profile = UserProfile.objects.get(user = request.user)
	if user_profile.is_participant:
		participant_abstracts = Abstract.objects.filter(author1=user_profile)
		#participant_papers = Paper.objects.filter(author=user_profile)
		return render(request, 'main/paper-presentation/dashboard.html', {'abstracts': participant_abstracts,})
																		  #'papers': participant_papers})
	abstracts_allotted = Abstract.objects.filter(professor=user_profile)
	papers_allotted = []
	papers = Paper.objects.all()
	for paper in papers:
		if paper.abstract in abstracts_allotted:
			papers_allotted.append(paper)
			abstracts_allotted = abstracts_allotted.exclude(uid = paper.abstract.uid)
	return render(request, 'main/paper-presentation/dashboard.html', {'user_profile': user_profile,
													'abstracts_allotted': abstracts_allotted,
													'papers_allotted': papers_allotted})
@login_required
def abstract_review(request, pk):
	abstract = get_object_or_404(Abstract, pk=pk)
	if request.method == 'POST':
		abstract_review_form = AbstractReviewForm(request.POST, instance=abstract)
		if abstract_review_form.is_valid():
			abstract = abstract_review_form.save(commit=False)
			abstract.status = 'AC'
			abstract.save()
			return HttpResponseRedirect(reverse('dashboard'))
	else:
		abstract_review_form = AbstractReviewForm()	
	return render(request, 'main/paper-presentation/abstract-review.html', {'abstract_review_form': abstract_review_form,
																			'abstract': abstract})

def paper_review(request, pk):
	abstract = get_object_or_404(Abstract, pk=pk)
	paper = get_object_or_404(Paper, abstract=abstract)
	if request.method == 'POST':
		paper_review_form = PaperReviewForm(request.POST, instance=paper)
		if paper_review_form.is_valid():
			paper = paper_review_form.save(commit=False)
			paper.status = 'PC'
			paper.save()
			return HttpResponseRedirect(reverse('dashboard'))
	else:
		paper_review_form = PaperReviewForm()
	return render(request, 'main/paper-presentation/paper-review.html', {'paper_review_form': paper_review_form,
																		 'abstract': abstract,
																		 'paper': paper})
