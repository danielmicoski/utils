from utils_prod import get_azure_connection,\
        download_blob_file,\
        upload_blob_file


data_config = {
    'account_name': 'account_name',
    'account_key': 'account_key',
    'container_name': 'container',
    'input_files': ['input.csv'],
    'output_files': 'teste.csv',
    'path_output': 'sources/',
    'path_to_upload': 'sources/',
    'download_files': 'True',
    'upload_files': 'True'
}

# Connect
azure_connect = get_azure_connection(data_config['account_name'], data_config['account_key'])


# Download Files
status_blob_download = download_blob_file(azure_connect, container_name = data_config['container_name'], blob_name = data_config['input_files'][0], path_output = data_config['path_output']+data_config['input_files'][0])

if status_blob_download is True:
    print('Download: OK')

# Upload Files

status_blob_upload = upload_blob_file(azure_connect, container_name = data_config['container_name'], local_file_name = data_config['output_files'], full_path = data_config['path_to_upload']+data_config['output_files'])

if status_blob_upload is True:
    print('Upload: OK')