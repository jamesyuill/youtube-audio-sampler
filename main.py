# uvicorn server:app --reload 

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import os
import tempfile
import shutil
import traceback
from download import scrape_youtube, dl_and_convert
from create_folder import create_user_folder
from cut_up import cut_up_audio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


app = FastAPI()

origins = ["http://127.0.0.1:1430",
    "null" ]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'],allow_headers=['*'])

class CopyFileRequest(BaseModel):
    source_path: str
    target_folder: str
    target_filename: str







@app.get('/')
def home():
    return {"msg":"Server working"}


@app.get('/get-list')
def get_list(search_query: str):
    print('searching:', search_query)
    try:
        #create unique temp folder
        global folder_name
        folder_name = create_user_folder(BASE_DIR)
        print('folder created: ', folder_name)

        url_list = scrape_youtube(search_query)
        return {"url_list":url_list, "folder_name":folder_name}
    except Exception as e:
        print("Exception occurred:")
        traceback.print_exc()
        return {"error": str(e)}
    



@app.get('/scrape-audio')
def scrape_audio(url:str):
    print(f'Scrape request received: {url}')
    try:
        #use url to get audio and create snippets
        dl_and_convert(BASE_DIR, url)
        
        cut_up_audio(BASE_DIR, folder_name)

    #return the list of files and the folder name
        files = os.listdir(f'{BASE_DIR}/{folder_name}')
        return {'folder_name':folder_name, 'files':files}
    except Exception as e:
        traceback.print_exc()
        return {'error':str(e)}



@app.get('/play/{folder_name}/{file_name}')
def play(folder_name: str, file_name:str):
    path = BASE_DIR + '/' + folder_name + '/' + file_name
    return FileResponse(
        path,
        media_type = "audio/wav",
        headers={
            "Cache-Control":"no-store,no-cache, must-revalidate",
            "Pragma":"no-cache",
            "Expires":"0"
        }
    )



@app.get('/save_file/{folder_name}/{file_name}')
def save_file(folder_name:str,file_name:str):
    filepath = os.path.join(BASE_DIR, folder_name, file_name)
    downloads_path = os.path.join(os.path.expanduser("~/Downloads"),file_name)
    destination_path = get_unique_path(downloads_path)
    try:
        
        shutil.copy2(filepath,destination_path)
        return {'msg':'file saved'}
    except Exception as e:
        import traceback
        return {'msg':f'an error occured:{e}','trace':traceback.format_exc()}



def DeleteFileBackground(path):
    return BackgroundTask(lambda: os.remove(path))



def get_unique_path(path_str:str)-> Path:
    path = Path(path_str)
    if not path.exists():
        return path
    
    counter = 1
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    while True:
        new_name = f'{stem}({counter}){suffix}'
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1





@app.get('/download-all/{folder_name}')
def download_all(folder_name:str):
    downloads_path = os.path.expanduser("~/Downloads")
    
    try:
        ZIP_NAME = "all_samples.zip"
        temp_file = tempfile.NamedTemporaryFile(dir=BASE_DIR,suffix=".zip", delete=False)
        temp_file.close()

        folderpath = os.path.join(BASE_DIR, folder_name)
        temp_file_name = shutil.make_archive(base_name=temp_file.name[:-4], format='zip',root_dir=folderpath)
    except Exception as e:
        return {'msg':f'an error occured whilst creating the temp zip folder:{e}'}


    try:
        zip_path = os.path.join(BASE_DIR, temp_file_name)
        shutil.copy2(zip_path,downloads_path)
        
        #removes temp zip folder
        os.remove(zip_path)
        
        return {'msg':'folder saved'}
    except Exception as e:
        return {'msg':f'an error occured:{e}'}


if __name__ == "__main__":
    uvicorn.run('main:app',host="127.0.0.1",port=8000)