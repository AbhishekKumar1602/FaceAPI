import cv2
import numpy as np
import httpx
from fastapi import HTTPException 
from dependencies import face_cascade, eye_cascade
from pydantic import BaseModel
import os
import io

class ImageCoverageResponse(BaseModel):
    Human_Detected: bool

def detect_face(image_np):
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=50)

    if len(faces) == 0:
        return None
    x, y, w, h = max(faces, key=lambda item: item[2] * item[3])
    return (x, y, w, h)

def detect_eyes(image_np, face_rect):
    x, y, w, h = face_rect
    roi_gray = image_np[y:y + h, x:x + w]
    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)
    return [(ex, ey, ew, eh) for (ex, ey, ew, eh) in eyes]

def draw_face_rectangle(image_np, face_rect, eyes, save_path):
    x, y, w, h = face_rect
    cv2.rectangle(image_np, (x, y), (x + w, y + h), (255, 0, 0), 2)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(image_np, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)
    cv2.imwrite(save_path, image_np)

def are_eyes_closed(image_np, eyes):
    closed_eye_count = 0
    for (ex, ey, ew, eh) in eyes:
        eye_roi = image_np[ey:ey+eh, ex:ex+ew]
        gray_eye = cv2.cvtColor(eye_roi, cv2.COLOR_BGR2GRAY)
        _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
        white_pixels = cv2.countNonZero(threshold_eye)
        total_pixels = threshold_eye.size
        white_ratio = white_pixels / total_pixels
        if white_ratio < 0.2:  
            closed_eye_count += 1
    return closed_eye_count == len(eyes)

async def process_image(image_np, contents, filename):
    face_rect = detect_face(image_np)
    if face_rect is None:
        return ImageCoverageResponse(Human_Detected=False)

    eyes = detect_eyes(image_np, face_rect)
    draw_face_rectangle(image_np, face_rect, eyes, f"/home/FaceAPI/HumanDetectionAPI/images/{filename}")

    if are_eyes_closed(image_np, eyes):
        return ImageCoverageResponse(Human_Detected=False)

    image_height = image_np.shape[0]
    estimated_face_area = estimate_face_area_from_image(image_np, face_rect, image_height, f"/home/FaceAPI/HumanDetectionAPI/images/{filename}")

    image_area = image_np.shape[0] * image_np.shape[1]
    coverage_percentage = (estimated_face_area / image_area) * 100

    if coverage_percentage < 10:
        raise HTTPException(status_code=293, detail="Insufficient Face Coverage, Click Image From Closer Distance")

    return ImageCoverageResponse(Human_Detected=True)

def estimate_face_area_from_image(image_np, face_rect, image_height, save_path):
    x, y, face_width, face_height = face_rect
    face_area = face_width * face_height
    return face_area
