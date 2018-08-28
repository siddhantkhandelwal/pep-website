from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login



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