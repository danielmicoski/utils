from azure.storage.blob import BlobServiceClient
from azure.storage.blob.aio import BlobClient
import os

def get_azure_connection(account_name, account_key):
    """
    Get azure connection to handle blob files presented on container.

    :param String account_name: Azure storage account name
    :param String account_key: Azure storage account key to allows connection with azure.
    :return: Instance of Blob Service Class
    :rtype: Object
    """
    return "DefaultEndpointsProtocol=https;AccountName="+account_name+";AccountKey="account_key"+;EndpointSuffix=core.windows.net"

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
        blob = BlobClient.from_connection_string(conn_str=connection, container_name=container_name, blob_name=blob_name)
        with open(path_output,'wb') as myblob:
            blob_data = blob.download_blob()
            blob_data.readinto(myblob)
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
        blob = BlobClient.from_connection_string(conn_str=connection, container_name=container_name, blob_name=local_file_name)
        with open(full_path,'rb') as data:
            blob.upload_blob(data)
        print('File {0} uploaded'.format(local_file_name))
        return True
    except ValueError:
        print("Something went wrong")
        return False