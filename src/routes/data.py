from fastapi import status,APIRouter,Depends,UploadFile
from helpers.config import get_settings,Settings
from fastapi.responses import JSONResponse
import os
import aiofiles
from models import ResponseSignal
from controllers import DataController,ProjectControllers
import logging 
logger = logging.getLogger('uvicorn.error')
data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/(project_id)")
async def upload_data(project_id:str,file:UploadFile,
                        app_settings:Settings=Depends(get_settings)):
    is_valid,result_signal=DataController().validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
        "signal":result_signal
        
    })
    project_dir_path=ProjectControllers().get_project_path(project_id=project_id)
    file_path=DataController().generate_unique_filename(orig_file_name=file.filename,project_id=project_id)
    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunk:=await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"error while uploading : {e}")
        return JSONResponse(
            content={
        "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
        
            })
    return JSONResponse(
            content={
        "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value
        
            })        
    

