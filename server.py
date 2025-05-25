# uvicorn server:app --reload 

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
import shutil
from download import scrape_youtube, dl_and_convert
from cut_up import cut_up_audio

app = FastAPI()

origins = [
    'http://127.0.0.1:5500'
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'],allow_headers=['*'])



#Creates unique user_id and unique folder for that user
def create_user_folder():
    user_id = uuid.uuid4()
    folder_name = f'temp-{user_id}'
    os.mkdir(folder_name)
    return folder_name





@app.get('/')
def home():
    return {"msg":"Server working"}


@app.get('/get-list')
def get_list(search_query: str):
    
    url_list = scrape_youtube(search_query)
    return {"url_list":url_list}
    

@app.get('/scrape-audio')
def scrape_audio(url:str):
    #create unique temp folder
    folder_name = create_user_folder()

    #mounts the temp folder as audio
    app.mount('/audio',StaticFiles(directory=folder_name),name='audio')

    #use url to get audio and create snippets
    audio_path = dl_and_convert(url)
    cut_up_audio(audio_path, folder_name)

    #return the list of files and the folder name
    try:
        files = os.listdir(f'./{folder_name}')
        return {'folder_name':folder_name, 'files':files}
    except:
        return {'msg':'Not found'}


@app.get('/download/{folder_name}/{file_name}')
def download(folder_name:str,file_name:str):
    filepath = f'./{folder_name}/{file_name}'
    if not os.path.exists(filepath):
        return {'msg':'File not found'}
    return FileResponse(
        path=filepath,
        media_type="application/octet-stream",
        filename=file_name,
        headers={'Content-Disposition':f'attachment; filename={file_name}'}
    )



@app.get('/delete-temp-folder')
def delete_temp_folder(folder_name:str):
    try:
        #look for temp folder
        if os.path.exists(f'./{folder_name}'):
            shutil.rmtree(f'./{folder_name}')
            return {'msg':f'{folder_name} deleted'}
    except:
        return {'msg':'Folder not found'}