from apscheduler.schedulers.blocking import BlockingScheduler
import time
import os
import shutil

def cleanup_old_temp_folders(max_age_hours = 2):
    print('running cleanup')
    now = time.time()
    max_age_seconds = max_age_hours * 3600
    
    for folder_name in os.listdir('./'):
        if folder_name.startswith('temp-'):

            folder_mtime = os.path.getmtime(f'./{folder_name}')
            age = now - folder_mtime

            if age > max_age_seconds:
                try:
                    shutil.rmtree(f'./{folder_name}')
                    print(f'Deleted: {folder_name}')
                except:
                    print(f'Error deleting {folder_name}')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(cleanup_old_temp_folders, 'cron',hour=4,minute=0)
    scheduler.start()