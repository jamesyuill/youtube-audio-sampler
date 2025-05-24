# uvicorn server:app --reload 

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import uuid
import shutil

app = FastAPI()

app.mount('/audio',StaticFiles(directory='temp'),name='audio')

#Creates unique user_id and unique folder for that user
def create_user_folder():
    user_id = uuid.uuid4()
    folder_name = f'temp-{user_id}'
    os.mkdir(folder_name)
    return folder_name


@app.get('/')
def home():
    return {"msg":"Server working"}


@app.get('/scrape')
def scrape(search_query: str):
    #need to personalise tempfolder for this specific user
    folder_name = create_user_folder()
    return {"Search Query":search_query, "folder-name":folder_name}

@app.get('/list-audio-files')
def list_audio_files(folder_name: str):
    try:
        files = os.listdir(f'./{folder_name}')
        return {'files':files}
    except:
        return {'msg':'Not found'}




@app.get('/delete-temp-folder')
def delete_temp_folder(folder_name:str):
    try:
        #look for temp folder
        if os.path.exists(f'./{folder_name}'):
            shutil.rmtree(f'./{folder_name}')
            return {'msg':f'{folder_name} deleted'}
    except:
        return {'msg':'Folder not found'}