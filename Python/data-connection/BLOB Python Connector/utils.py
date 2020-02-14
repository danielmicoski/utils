from azure.storage.blob import BlockBlobService
import os

def get_azure_connection(account_name, account_key):
    """
    Get azure connection to handle blob files presented on container.

    :param String account_name: Azure storage account name
    :param String account_key: Azure storage account key to allows connection with azure.
    :return: Instance of Blob Service Class
    :rtype: Object
    """
    return BlockBlobService(account_name=account_name, account_key=account_key)

def download_blob_file(connection,container_name,blob_name,path_output):
    """
    Get blob file from cloud and downloads on local machine.

    :param Object connection: Azure connection instance
    :param str container_name: Azure Container name.
    :param str blob_name: Azure Blob name to download.
    :param str blob_name: Path where file will be saved.
    :return: True if download works and False if something went wrong.
    :rtype: Boolean
    """
    try:
        connection.get_blob_to_path(container_name=container_name,blob_name=blob_name, file_path=path_output)
        actual_size = os.path.getsize(path_output)
        print('File saved in {0}'.format(path_output))
        return True
    except ValueError:
        print("Something went wrong")
        return False


def upload_blob_file(connection,container_name,local_file_name, full_path):
    """
    Upload local file to cloud.

    :param Object connection: Azure connection instance
    :param str container_name: Azure Container name.
    :param str local_file_name: File name to upload.
    :param str full_path: Path file that will be uploaded.
    :return: True if upload works and False if something went wrong.
    :rtype: Boolean
    """
    try:
        connection.create_blob_from_path(container_name,local_file_name,full_path)
        print('File {0} uploaded'.format(local_file_name))
        return True
    except ValueError:
        print("Something went wrong")
        return False