# uvicorn server:app --reload 

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import os
import tempfile
import shutil
from download import scrape_youtube, dl_and_convert
from create_folder import create_user_folder
from cut_up import cut_up_audio

app = FastAPI()

#need to change this for frontend obvs!!!
origins = [
    'http://127.0.0.1:5500'
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'],allow_headers=['*'])









@app.get('/')
def home():
    return {"msg":"Server working"}


@app.get('/get-list')
def get_list(search_query: str):
    #create unique temp folder
    global folder_name
    folder_name = create_user_folder()

    url_list = scrape_youtube(search_query)
    return {"url_list":url_list, "folder_name":folder_name}
    



@app.get('/scrape-audio')
def scrape_audio(url:str):

    
    #also need to create a unique download folder too

    #mounts the temp folder as audio
    # app.mount('/audio',NoCacheStaticFiles(directory=folder_name),name='audio')

    #use url to get audio and create snippets
    audio_path = dl_and_convert(url)
    cut_up_audio(audio_path, folder_name)

    #return the list of files and the folder name
    try:
        files = os.listdir(f'./{folder_name}')
        return {'folder_name':folder_name, 'files':files}
    except:
        return {'msg':'Not found'}



@app.get('/play/{folder_name}/{file_name}')
def play(folder_name: str, file_name:str):
    path = folder_name + '/' + file_name
    return FileResponse(
        path,
        media_type = "audio/wav",
        headers={
            "Cache-Control":"no-store,no-cache, must-revalidate",
            "Pragma":"no-cache",
            "Expires":"0"
        }
    )



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

def DeleteFileBackground(path):
    return BackgroundTask(lambda: os.remove(path))



@app.get('/download-all/{folder_name}')
def download_all(folder_name:str):
    ZIP_NAME = "all_samples.zip"

    temp_file = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    temp_file.close()

    shutil.make_archive(base_name=temp_file.name[:-4], format='zip',root_dir=folder_name)

    return FileResponse(
        path=temp_file.name,
        filename=ZIP_NAME,
        media_type='application/zip',
        headers={
            "Cache-Control":"no-store"
        },
        background=DeleteFileBackground(temp_file.name)
    )