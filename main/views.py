from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, UserProfileForm, AbstractForm, PaperForm
from django.contrib.auth import authenticate, login, logout
from .models import Abstract, Paper


def index(request):
	return HttpResponse("Hello!")

def register(request):
	registered = False
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
			registered = True
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
				return HttpResponseRedirect(reverse('index'))

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
		if papaer_form.is_valid():
			paper_form.save()
			return HttpResponseRedirect(reverse('index'))
	else:
		paper_form = PaperForm()
	return render(request, 'main/paper-upload.html', {'paper_form': paper_form})

def dashboard(request):
	abstract_count = Abstract.objects.count()
	paper_count = Paper.objects.count()

	return render(request, 'main/dashboard.html', {'abstract_count': abstract_count,
													'paper_count': paper_count})
