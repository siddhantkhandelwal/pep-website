from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^index', views.index, name='index'),
	url(r'^accounts/register/$', views.register, name='register'),
	url(r'^accounts/login/$', views.user_login, name='user_login'),
	url(r'^accounts/logout/$', views.user_logout, name='user_logout'),
	url(r'^dashboard', views.dashboard, name='dashboard'),
	url(r'^abstract_submission', views.abstract_submission, name='abstract_submission'),
	url(r'^paper_submission', views.paper_submission, name='paper_submission'),
]