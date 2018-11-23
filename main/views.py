from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, AbstractForm, PaperForm, AbstractReviewForm, PaperReviewForm, ParticipantProfileForm, PasswordResetForm, AssignProfessorForm
from django.contrib.auth import authenticate, login, logout
from .models import Abstract, Paper, ParticipantProfile, ProfessorProfile, StaffProfile, College, SupervisorProfile, Category
from django.contrib.auth.decorators import login_required

# import sendgrid
# import os
# from sendgrid.helpers.mail import *

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
import os
import datetime
from django.utils import timezone
import pytz
from django_file_md5 import calculate_md5


def paper_presentation(request):
    return HttpResponseRedirect(reverse('main:portal'))
    # return render(request, 'main/paper-presentation/paper-presentation.html', {})


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
                if user.username == 'pepadmin':
                    return HttpResponseRedirect(reverse('main:pepadmin'))
                else:
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
        password_reset_form = PasswordResetForm(
            data=request.POST, instance=user)
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
        user_profile_form = ParticipantProfileForm(
            data=request.POST, instance=user)
        if user_profile_form.is_valid():
            user_profile = user_profile_form.save()
            return HttpResponseRedirect(reverse('main:portal'))
    else:
        user_profile_form = ParticipantProfileForm()
    return render(request, 'main/paper-presentation/edit-profile.html', {'user_profile_form': user_profile_form})


@login_required
def portal(request):
    if request.user.is_superuser:
        # return HttpResponseRedirect('/admin')
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
        # professors = ProfessorProfile.objects.filter(category_id__in=[category.id for category in user_profile.categories.all()])
        assign_professor_form = AssignProfessorForm()
        return render(request, 'main/paper-presentation/portal.html', {'user_profile': user_profile,
                                                                       # 'categories': categories,
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
                abstracts_allotted = abstracts_allotted.exclude(
                    uid=paper.abstract.uid)
        return render(request, 'main/paper-presentation/portal.html', {'user_profile': user_profile,
                                                                       'abstracts_allotted': abstracts_allotted,
                                                                       'papers_allotted': papers_allotted,
                                                                       'access_level': access_level})

    else:
        user_profile = ParticipantProfile.objects.get(user=request.user)
        participant_abstracts = Abstract.objects.filter(
            participant=user_profile)
        participant_papers = []
        for paper in Paper.objects.all():
            if paper.abstract in participant_abstracts:
                participant_papers.append(paper)
                participant_abstracts = participant_abstracts.exclude(
                    uid=paper.abstract.uid)
        access_level = 0
        return render(request, 'main/paper-presentation/portal.html', {'abstracts': participant_abstracts,
                                                                       'papers': participant_papers,
                                                                       'access_level': access_level,
                                                                       'user_profile': user_profile})


@login_required
def abstract_submission(request):
    if request.method == 'POST':
        user_profile = ParticipantProfile.objects.get(user=request.user)
        abstract_form = AbstractForm(request.POST, request.FILES)
        if abstract_form.is_valid():
            abstract = abstract_form.save(commit=False)
            if abstract.document.name.split('.')[1] != 'pdf':
                return render(request, 'main/paper-presentation/abstract-upload.html', {'abstract_upload_form_errors': 'Only PDF file format is Supported',
                                                                                        'abstract_form': abstract_form, })

            abstract.participant = user_profile
            for staff in StaffProfile.objects.filter(categories__in=[abstract.category]):
                abstract.staff.add(staff)
            abstract.document.name = str(
                abstract.uid) + '-' + abstract.title + '.' + abstract.document.name.split('.')[1]
            abstract.save()

            # sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
            # from_email = Email("pep@bits-apogee.org")
            # to_email = Email(user_profile.user.email)
            # subject = "Paper Presentation Event"
            # msg = abstract.title + str(abstract.uid) + abstract.participant.author
            # content = Content("text/plain", msg)
            # mail = Mail(from_email, subject, to_email, content)
            # response = sg.client.mail.send.post(request_body=mail.get())
            # print(response.status_code)
            # print(response.body)
            # print(response.headers)

            return HttpResponseRedirect(reverse('main:portal'))
    else:
        abstract_form = AbstractForm()
    return render(request, 'main/paper-presentation/abstract-upload.html', {'abstract_form': abstract_form})


@login_required
def abstract_review(request, pk):
    abstract = get_object_or_404(Abstract, pk=pk)
    if request.method == 'POST':
        abstract_review_form = AbstractReviewForm(
            request.POST, instance=abstract)
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
            paper.document.name = str(paper.abstract.uid) + '-' + \
                paper.abstract.title + '.' + \
                paper.document.name.split('.')[1]
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


def pepadmin(request):
    return render(request, 'main/paper-presentation/pepadmin.html', {})


@login_required
def check_duplicate_abstracts(request):
    abstracts = Abstract.objects.all()
    
    md5_dict = {}

    for abstract in abstracts:
        md5_dict[abstract.uid] = calculate_md5(abstract.document)
    
    rev_multiduct_md5_dict = {}

    for uid, md5 in md5_dict.items():
        rev_multiduct_md5_dict.setdefault(md5, set()).add(uid)
    
    response = []
    
    for uid_set in [uids for md5, uids in rev_multiduct_md5_dict.items() if len(uids) > 1]:
        response.append(uid_set)
    return HttpResponse(response) 


@login_required
def upload_to_drive(request):

    global uploaded_files
    global uploaded_files_path
    uploaded_files_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "uploaded_files")

    with open(uploaded_files_path, "r+") as f:
        uploaded_files = f.read().splitlines()

    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("creds.txt")

    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("creds.txt")

    drive = GoogleDrive(gauth)  # authentication.

    try:
        root_folder_name = 'PEP Portal'
        root_folder_id = create_root_folder(drive, root_folder_name)
        uploaded_files.append(root_folder_name)

        # category_folders_dict = create_category_folders(
        #     drive, root_folder_id)

        date_folder_name = 'Upto 15th Nov'
        date_folder_id_upto_15th = create_folder(
            drive, date_folder_name, root_folder_id)
        uploaded_files.append(date_folder_name)

        date_folder_name = 'After 15th Nov'
        date_folder_id_after_15th = create_folder(
            drive, date_folder_name, root_folder_id)
        uploaded_files.append(date_folder_name)

        category_folders_dict_upto_15th = create_category_folders(
            drive, date_folder_id_upto_15th)

        category_folders_dict_after_15th = create_category_folders(
            drive, date_folder_id_after_15th)

        for category in Category.objects.all():
            # id = category_folders_dict[category.name]
            for abstract in Abstract.objects.filter(category=category):
                if abstract.document.name.split("/")[2] not in uploaded_files:
                    
                    if abstract.submission_date <= timezone.datetime(2018, 11, 15).replace(tzinfo=pytz.timezone('Asia/Kolkata')):
                        id = category_folders_dict_upto_15th[category.name]
                    else:
                        id = category_folders_dict_after_15th[category.name]

                    file = drive.CreateFile(metadata={"title": abstract.document.name.split("/")[2],
                                                    "parents": [{"kind": "drive#fileLink",
                                                                "id": id}]})
                    file.SetContentFile(abstract.document.path)
                    file.Upload()
                    uploaded_files.append(file['title'])
    finally: 
        with open(uploaded_files_path, "w+") as f:
            for uploaded_file in uploaded_files:
                f.write(uploaded_file + '\n')

    return HttpResponseRedirect(reverse('main:pepadmin'))


def get_file_list(drive):
    file_list = drive.ListFile(
        {'q': "'root' in parents and trashed=false"}).GetList()
    return file_list


def search_file_in_list(file_list, file_name_to_search):
    for file in file_list:
        if file['title'] == file_name_to_search:
            id = file['id']
            return id
    return -1


def create_folder(drive, folder_name, parent_folder_id=''):
    folder_metadata = {
        'title': folder_name,
        # The mimetype defines this new file as a folder, so don't change this.
        'mimeType': 'application/vnd.google-apps.folder',
    }

    if parent_folder_id != '':
        folder_metadata['parents'] = [{'id': parent_folder_id}]

    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id']
    # return search_file_in_list(get_file_list(drive), folder_name)


def create_root_folder(drive, root_folder_name):
    file_list = get_file_list(drive)
    id = search_file_in_list(file_list, root_folder_name)

    if id == -1:
        create_folder(drive, root_folder_name)
        id = search_file_in_list(get_file_list(drive), root_folder_name)
    return id


def create_category_folders(drive, root_folder_id):
    category_folders_details = {}
    categories = Category.objects.all()
    for category in categories:
        if root_folder_id + category.name not in uploaded_files:
            id = create_folder(drive, category.name, root_folder_id)
            category_folders_details[category.name] = id
            uploaded_files.append(root_folder_id + category.name)
    return category_folders_details
