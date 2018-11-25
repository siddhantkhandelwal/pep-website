from django.conf.urls import url
from . import views

app_name="main"

urlpatterns = [
	url(r'^$', views.paper_presentation, name='paper_presentation'),
	url(r'^about/$', views.about, name='about'),
	url(r'^accounts/register/$', views.register, name='register'),
	url(r'^accounts/login/$', views.user_login, name='user_login'),
	url(r'^accounts/logout/$', views.user_logout, name='user_logout'),
	#url(r'^accounts/password-reset/$', views.user_password_reset, name='user_password_reset'),
	#url(r'^accounts/edit-profile/$', views.edit_profile, name='edit_profile'),
	url(r'^pepadmin/upload-to-drive/(?P<pk>\d+)/$', views.upload_to_drive, name='upload_to_drive'),
	url(r'^pepadmin/check-duplicate-abstracts/$', views.check_duplicate_abstracts, name='check_duplicate_abstracts'),
	url(r'^pepadmin/$', views.pepadmin, name='pepadmin'),
	url(r'^portal/$', views.portal, name='portal'),
	url(r'^portal/abstract-submission/$', views.abstract_submission, name='abstract_submission'),
	url(r'^portal/abstract-review/(?P<pk>\d+)/$', views.abstract_review, name='abstract_review'),
	url(r'^portal/assign-professor/(?P<pk>\d+)/$', views.assign_professor, name='assign_professor'),
	url(r'^portal/paper-submission/$', views.paper_submission, name='paper_submission'),
	url(r'^portal/paper-review/(?P<pk>\d+)/$', views.paper_review, name='paper_review'),
]
