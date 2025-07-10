from mediafire import MediaFireApi
from config import MEDIAFIRE_EMAIL, MEDIAFIRE_PASSWORD

def upload_to_mediafire(file_path):
    api = MediaFireApi()
    session = api.login(email=MEDIAFIRE_EMAIL, password=MEDIAFIRE_PASSWORD)
    uploaded = api.upload_file(file_path, folder_key=None, session_token=session['session_token'])
    return uploaded['direct_download']
