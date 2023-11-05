from fastapi import FastAPI
from controllers import router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
#origins = ["https://app-061c7eb9-4e4d-4bff-a3ba-ac5f184e2f25.cleverapps.io"]  
origins = ["*"] # for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
