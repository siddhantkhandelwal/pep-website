from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, UserProfileForm, AbstractForm, PaperForm, AbstractReviewForm, PaperReviewForm
from django.contrib.auth import authenticate, login, logout
from .models import Abstract, Paper, UserProfile
from django.contrib.auth.decorators import login_required


def index(request):
	return render(request, 'main/index.html', {})

def register(request):
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			profile.save()
			return HttpResponseRedirect(reverse('user_login'))
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 
		'main/register.html',
		{'user_form': user_form,
		'profile_form': profile_form,
		'registered': registered})

def user_login(request):
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
		return render(request, 'main/login.html', {})

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('user_login'))

def abstract_submission(request):
	if request.method == 'POST':
		abstract_form = AbstractForm(request.POST, request.FILES)
		if abstract_form.is_valid():
			abstract_form.save()
			return HttpResponseRedirect(reverse('index'))
	else:
		abstract_form = AbstractForm()
	return render(request, 'main/abstract-upload.html', {'abstract_form': abstract_form})

def paper_submission(request):
	if request.method == 'POST':
		paper_form = PaperForm(request.POST, request.FILES)
		if paper_form.is_valid():
			paper_form.save()
			return HttpResponseRedirect(reverse('index'))
	else:
		paper_form = PaperForm()
	return render(request, 'main/paper-upload.html', {'paper_form': paper_form})

@login_required
def dashboard(request):
	if request.user.is_superuser:
		return HttpResponseRedirect('/admin')
	user_profile = UserProfile.objects.get(user = request.user)
	abstracts_allotted = Abstract.objects.filter(professor=user_profile)
	return render(request, 'main/dashboard.html', {'user_profile': user_profile,
													'abstracts_allotted': abstracts_allotted})
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
	return render(request, 'main/abstract-review.html', {'abstract_review_form': abstract_review_form})

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
	return render(request, 'main/paper-review.html', {'paper_review_form': paper_review_form})
