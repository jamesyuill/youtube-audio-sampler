
import os
import shutil

def cleanup_old_temp_folders(base_path):
    print('running cleanup')
    
    for folder_name in os.listdir(base_path):
        if folder_name.startswith('temp-'):
            try:
                folderpath = os.path.join(base_path, folder_name)
                shutil.rmtree(folderpath)
                print(f'Deleted: {folder_name}')
            except:
                print(f'Error deleting {folder_name}')