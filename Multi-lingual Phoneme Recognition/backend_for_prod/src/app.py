import os
import secrets
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from ai_utils import Model, SpeechDataset
from schemas import PredictionSchema
from utils import get_audio, to_str, webm_to_wav

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
     allow_headers=["*"]
)

model = Model()
dataset = SpeechDataset()

@app.post('/predict', response_model=PredictionSchema)
async def predict(file: Annotated[UploadFile, File(...)]):
    request_id = secrets.token_urlsafe(8)
    out_path = f'../data/{request_id}.webm'
    with open(out_path, 'wb') as f:
        f.write(await file.read())
    
    webm_to_wav(out_path, out_path+'.wav')

    os.remove(out_path)

    audio = get_audio(out_path+'.wav')

    result = model.predict(audio)[0]

    return {'result': to_str(result), 'request_id': request_id}
