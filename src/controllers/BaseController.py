from helpers.config import get_settings,Settings
from fastapi import UploadFile
from models import ResponseSignal
class BaseController:
    
    def __init__(self):
        self.app_settings=get_settings()
        self.size_scale=1048576  #convert mb to bytes

    def validate_uploaded_file(self,file:UploadFile) :
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
                return False ,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        if file.size>self.app_settings.FILE_MAX_SIZE:
                return False ,ResponseSignal.FILE_SIZE_EXCEEDED.value
        return True,ResponseSignal.FILE_VALIDATED_SUCCESS.value