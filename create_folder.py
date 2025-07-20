from cleanup import cleanup_old_temp_folders
import uuid
import os

def create_user_folder(base_path):
    cleanup_old_temp_folders(base_path)
    user_id = uuid.uuid4()
    folder_name = f'temp-{user_id}'
    path = os.path.join(base_path, folder_name)
    os.mkdir(path)
    return folder_name