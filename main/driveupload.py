from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
import os
import datetime
from django.utils import timezone
import pytz
from models import Abstract, Paper, ParticipantProfile, ProfessorProfile, StaffProfile, College, SupervisorProfile, Category

def upload_thread(pk):
        global uploaded_files
        global uploaded_files_path
	uploaded_files = []
        uploaded_files_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "uploaded_files")
        if pk==0:
            with open(uploaded_files_path, "r+") as f:
                uploaded_files = f.read().splitlines()
        elif pk==1:
            with open(uploaded_files_path, "r+") as f:
                f.truncate()
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
            # if date_folder_name not in uploaded_files:
            date_folder_id_upto_15th = create_folder(
                drive, date_folder_name, root_folder_id)
            uploaded_files.append(date_folder_name + " - " + date_folder_id_upto_15th)
            # else:
                # date_folder_id_upto_15th = [entry.split(' - ')[2] for entry in uploaded_files if entry.contains('Upto 15th Nov - ')]

            date_folder_name = 'After 15th Nov'
            # if date_folder_name not in uploaded_files:
            date_folder_id_after_15th = create_folder(
                drive, date_folder_name, root_folder_id)
            uploaded_files.append(date_folder_name + "-" + date_folder_id_after_15th)
            # else:
                # date_folder_id_after_15th = [entry.split(' - ')[2] for entry in uploaded_files if entry.contains('After 15th Nov - ')]

            category_folders_dict_upto_15th = create_category_folders(
                drive, date_folder_id_upto_15th)

            category_folders_dict_after_15th = create_category_folders(
                drive, date_folder_id_after_15th)

            for category in Category.objects.all():
                # id = category_folders_dict[category.name]
                for abstract in Abstract.objects.filter(category=category):
                    if abstract.document.name.split("/")[2] not in uploaded_files:
                        if abstract.submission_date <= timezone.datetime(2018, 11, 17).replace(tzinfo=pytz.timezone('Asia/Kolkata')):
                            id = category_folders_dict_upto_15th[category.name]
                        else:
                            id = category_folders_dict_after_15th[category.name]

                        file = drive.CreateFile(metadata={"title": abstract.document.name.split("/")[2],
                                                        "parents": [{"kind": "drive#fileLink",
                                                                    "id": id}]})
                        file.SetContentFile(abstract.document.path)
                        file.Upload()
                        uploaded_files.append(file['title'])
            return 'Task Completed'
        except:
            return 'Error'
        finally: 
            with open(uploaded_files_path, "w+") as f:
                for uploaded_file in uploaded_files:
                    f.write(uploaded_file + '\n')

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

def execute():
    upload_thread(1)
    print("Starting Execution")
