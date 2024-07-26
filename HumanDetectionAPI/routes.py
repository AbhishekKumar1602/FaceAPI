from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Header
from PIL import Image
from fastapi.params import Form
import io
import numpy as np
from models import process_image
from pydantic import BaseModel

router = APIRouter()

class ImageCoverageResponse(BaseModel):
    Human_Detected: bool

API_KEY = "STFAPIEXP0001"

def authenticate_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True

@router.post("/human-detection/", response_model=ImageCoverageResponse)
async def image_coverage(
    file: UploadFile = File(...),
    min_file_size_kb: str = Form(None), 
    authorized: bool = Depends(authenticate_api_key)
    ):
    try:
        
        min_file_size_bytes = int(min_file_size_kb) * 1024

        contents = await file.read()
        if len(contents) < min_file_size_bytes:
            raise HTTPException(status_code=400, detail=f"File Size Must Be At Least {min_file_size_kb}KB")

        result = await process_image_async(contents, file.filename)

        return result

    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def process_image_async(contents, filename):
    try:
        image = Image.open(io.BytesIO(contents))

        image_np = np.array(image)

        result = await process_image(image_np, contents, filename)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
