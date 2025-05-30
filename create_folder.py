import uuid
import os

def create_user_folder():
    user_id = uuid.uuid4()
    folder_name = f'temp-{user_id}'
    os.mkdir(folder_name)
    return folder_name