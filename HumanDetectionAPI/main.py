from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as image_router

app = FastAPI()

app.include_router(image_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
