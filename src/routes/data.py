from fastapi import status,APIRouter,Depends,UploadFile
from helpers.config import get_settings,Settings
from fastapi.responses import JSONResponse
import os
import aiofiles
from models import ResponseSignal
from controllers import DataController,ProjectControllers,ProcessController
import logging 
from .schemes.data import ProcessRequest

logger = logging.getLogger('uvicorn.error')
data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_router.post("/upload/{project_id}")
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
    file_path,file_id=DataController().generate_unique_filename(orig_file_name=file.filename,project_id=project_id)
    try:
        await file.seek(0)
        total_size = 0
        async with aiofiles.open(file_path,"wb") as f:
            while chunk:=await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                total_size += len(chunk)
                # Validate size DURING upload
                if total_size > app_settings.FILE_MAX_SIZE:
                    await f.close()
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    return JSONResponse(
                        status_code=401,
                        content={"signal": ResponseSignal.FILE_SIZE_EXCEEDED.value}
                    )
                
                await f.write(chunk)
    except Exception as e:
        logger.error(f"error while uploading : {e}")
        return JSONResponse(
            content={
        "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
        
            })
    return JSONResponse(
            content={
        "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
        "file_id":file_id
        
            })        
    

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,process_request:ProcessRequest):
    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    overlap_size=process_request.overlap_size

    process_controller=ProcessController(project_id=project_id)
    file_content=process_controller.get_file_content(file_id=file_id)
    file_chunks=process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":ResponseSignal.PROCESSING_FAILED.value
            }
        )
    return file_chunks
        

    