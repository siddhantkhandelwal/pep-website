from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.paper_presentation, name='paper_presentation'),
	url(r'^accounts/register/$', views.register, name='register'),
	url(r'^accounts/login/$', views.user_login, name='user_login'),
	url(r'^accounts/logout/$', views.user_logout, name='user_logout'),
	#url(r'^accounts/password-reset/$', views.user_password_reset, name='user_password_reset'),
	#url(r'^accounts/edit-profile/$', views.edit_profile, name='edit_profile'),
	url(r'^portal/$', views.dashboard, name='dashboard'),
	url(r'^portal/abstract-submission/$', views.abstract_submission, name='abstract_submission'),
	url(r'^portal/abstract-review/(?P<pk>\d+)/$', views.abstract_review, name='abstract_review'),
	url(r'^portal/assign-professor/(?P<pk>\d+)/$', views.assign_professor, name='assign_professor'),
	url(r'^portal/paper-submission/$', views.paper_submission, name='paper_submission'),
	url(r'^portal/paper-review/(?P<pk>\d+)/$', views.paper_review, name='paper_review'),
	url(r'^about/$', views.about, name='about'),
]
