from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.think_again, name='think_again'),
	url(r'^paper-presentation/$', views.paper_presentation, name='paper_presentation'),
	url(r'^accounts/register/$', views.register, name='register'),
	url(r'^accounts/login/$', views.user_login, name='user_login'),
	url(r'^accounts/logout/$', views.user_logout, name='user_logout'),
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^abstract-submission/$', views.abstract_submission, name='abstract_submission'),
	url(r'^abstract-review/(?P<pk>\d+)/$', views.abstract_review, name='abstract_review'),
	url(r'^paper-submission/$', views.paper_submission, name='paper_submission'),
	url(r'^paper-review/(?P<pk>\d+)/$', views.paper_review, name='paper_review'),
]
