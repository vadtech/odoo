import requests
import urllib
import os
import logging

#TODO: documentation 
_logger = logging.getLogger(__name__)

tenantId = '20b97325-b26a-412d-9c70-c7f300d7af4d'
clientId = '7931f06f-44cb-4c0c-a876-0d1367e0ec1d'
clientSecret = 'QV48Q~hnVSams6booTxbawSSRmrH9ikBkKPh0a9r'
scope = 'https://graph.microsoft.com/.default'
user_id = '20b84634-c230-4ee1-bfee-5d619efff2c2'


def access_token():
    url = f'https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token'
    data = {'client_id': clientId,
            'scope': scope,
            'client_secret': clientSecret,
            'grant_type': 'client_credentials',
            }
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    result = requests.post(url,  headers=header, data=data)
    return result.json()['access_token']


headers = {'Authorization': f'Bearer {access_token()}',
           'Content-type': 'application/json'
           }


def get_users():
    """ print users in tenant"""
    users = requests.get(
        'https://graph.microsoft.com/v1.0/users', headers=headers)
    _logger.info(users.json())


def create_folder(folder_name):
    """create a folder with name"""
    file_body = {
        "name": folder_name,
        "folder": {}}
    files = requests.post(
        'https://graph.microsoft.com/v1.0/drive/root/children', headers=headers, json=file_body)
    _logger.info(files.json())


def list_files(folder_id):
    """"file in folder with id """
    folders = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/{folder_id}/children", headers=headers)
    folders_odoo = folders.json()['value']
    for f in folders_odoo:
        _logger.info(f['name'], f['id'], sep="  ")


def get_folder_id(folder_name='Odoo-backups'):
    """"file in folder with id """
    result = requests.get(
        f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/root/children", headers=headers)
    folders = result.json()['value']
    for folder in folders:
        if folder['name'] == folder_name:
            return folder['id']


def upload_file(folder_id, filename):
    file_url = urllib.parse.quote(filename)
    result = requests.post(
        f'https://graph.microsoft.com/v1.0/users/{user_id}/drive/items/{folder_id}:/{file_url}:/createUploadSession',
        headers=headers,
        json={
            '@microsoft.graph.conflictBehavior': 'replace',
            'description': 'A large test file',
            'fileSystemInfo': {'@odata.type': 'microsoft.graph.fileSystemInfo'},
            'name': filename
        }
    )
    upload_session = result.json()
    upload_url = upload_session['uploadUrl']

    st = os.stat(filename)
    size = st.st_size
    CHUNK_SIZE = 10485760
    chunks = int(size / CHUNK_SIZE) + 1 if size % CHUNK_SIZE > 0 else 0
    _logger.info(f" -----------------logger {upload_url} -------------------")

    try:
        with open(filename, 'rb') as fd:
            start = 0
            _logger.info(" -----------------filename -------------------")

            for chunk_num in range(chunks):
                _logger.info(" -----------------chunk_num -------------------")
                chunk = fd.read(CHUNK_SIZE)
                bytes_read = len(chunk)
                upload_range = f'bytes {start}-{start + bytes_read - 1}/{size}'
                _logger.info(
                    f'chunk: {chunk_num} bytes read: {bytes_read} upload range: {upload_range}')
                result = requests.put(
                    upload_url,
                    headers={
                        'Content-Length': str(bytes_read),
                        'Content-Range': upload_range
                    },
                    data=chunk
                )
                result.raise_for_status()
                start += bytes_read
                _logger.info(result.json())
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'fail',
                'reason': e}
