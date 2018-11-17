'''
Requirements
client_secrets.json 
PyDrive : pip install PyDrive

Note:
Steps to get the authentication going:
    Request Google Drive API access through Google Cloud Console
    Steps explained at: https://pythonhosted.org/PyDrive/quickstart.html
    
    Instructions for getting Google Drive API access:
    1. Go to Google Developers Console - https://console.developers.google.com and create a new project
    
    2. Click on Enable and manage APIs, click on Drive API, then click on Enable API.
    
    3. In API Manager, click on Credentials on the left panel. Select Add Credentials, choose OAuth 2.0 client ID, then Web Application. You may need to configure a consent screen, where the required part is the Product name, and the rest you can leave blank.
    
    4. In the Create client ID window, with Web application selected as Application type, specify the Name for your application, put http://localhost:8080 for Javascript origins and http://localhost:8080/ for redirect URIs. IMPORTANT: One of these ends with /, the other does not.
    
    5. Download the client_secrets.json file from Google Developers Console
    
    6. Go to Google Developers Console -https://console.developers.google.com and find the Use Google API section and click on Enable and manage APIs. Select Credentials on the left panel. You should see a list of your OAuth 2.0 client IDs. Check off the one you've created in step 1, and click on the download JSON button(looks like an arrow down icon). Rename the downloaded file to client_secrets.json.
    
    7. Place the client_secrets.json into the project directory
It is best to place the downloaded client_secrets.json file in the same directory as your python program that has the following line: gauth.LocalWebserverAuth()
'''

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys

def export_to_gdrive(file_name):
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
    
    drive = GoogleDrive(gauth)#authentication.

    id = ''
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        if file1['title'] == 'PEP Portal':
            id = file1['id']
            file = drive.CreateFile(metadata={"title": file_name,
                                      "parents": [{"kind":"drive#fileLink", 
                                      "id": id}]})
    if id == '':
        folder_metadata = {
            'title' : 'PEP Portal',
            # The mimetype defines this new file as a folder, so don't change this.
            'mimeType' : 'application/vnd.google-apps.folder'
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        for file1 in file_list:
            if file1['title'] == 'PEP Portal':
                id = file1['id']
        file = drive.CreateFile(metadata={"title": file_name,
                                      "parents": [{"kind":"drive#fileLink", 
                                      "id": id}]})

    
    file.SetContentFile(file_name)
    file.Upload()

if __name__ == "__main__":
    export_to_gdrive(sys.argv[1])
