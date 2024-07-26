from api import predict, app
from api.functions import download_image
from config import PORT
import os
from fastapi import FastAPI, UploadFile, File
from random import randint
from fastapi.responses import JSONResponse
import uvicorn

model = predict.load_model('nsfw_detector/nsfw_model.h5')


@app.post("/")
async def detect_nsfw(file: UploadFile = File(...)):
    if not file.filename:
        return JSONResponse(content={"ERROR": "NO FILE UPLOADED"}, status_code=400)


    # Save the uploaded image locally
    image_path = f"uploaded_image_{randint(1000, 9999)}.jpg"
    with open(image_path, "wb") as image_file:
        image_file.write(file.file.read())

    # Classify the image
    results = predict.classify(model, image_path)
    os.remove(image_path)  # Remove the saved image

    print(results)

    # Extract and return relevant information
    if not isinstance(results, dict) or not results.get('data'):
        return {"ERROR": "NSFW classification results not available"}

    nsfw_data = results.get('data', {})

    # Check if the required keys exist
    if 'sexy' not in nsfw_data or 'porn' not in nsfw_data or 'hentai' not in nsfw_data:
        return {"ERROR": "NSFW classification data incomplete"}

    nsfw_score = nsfw_data['porn'] + nsfw_data['hentai']
    is_nsfw = nsfw_score >= 50
    
    return {
        "is_nsfw": is_nsfw,
        "nsfw_score": nsfw_score,
        "classification_results": results
    }



if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=PORT, log_level="info")


