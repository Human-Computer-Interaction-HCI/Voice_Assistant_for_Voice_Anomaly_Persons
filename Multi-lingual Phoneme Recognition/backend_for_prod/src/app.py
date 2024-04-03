import os
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from ai_utils.dependencies import get_model, get_dataset, Model, SpeechDataset
from database import get_db
from services.auth.routes import router as auth_router
from schemas import LabelingRequestSchema, PredictionSchema
from utils import clear_str, get_audio, to_str, webm_to_wav

app = FastAPI()


data_dir = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict", response_model=PredictionSchema)
async def predict(
    file: Annotated[UploadFile, File(...)],
    model: Annotated[Model, Depends(get_model)],
    db: Annotated[Session, Depends(get_db)],
):
    request_id = secrets.token_urlsafe(8)
    out_path = f"{data_dir}/{request_id}.webm"
    with open(out_path, "wb") as f:
        f.write(await file.read())

    webm_to_wav(out_path, out_path + ".wav")

    os.remove(out_path)

    audio = get_audio(out_path + ".wav")

    result = model.predict(audio).argmax(-1)[0]

    return {"result": to_str(result), "request_id": request_id}


@app.post("/label")
async def label(
    data: LabelingRequestSchema, dataset: Annotated[SpeechDataset, Depends(get_dataset)]
):
    dataset.add_audio(f"{data_dir}/{data.request_id}.webm.wav", clear_str(data.label))
    return {"status": "ok"}


@app.post("/train")
async def train(
    model: Annotated[Model, Depends(get_model)],
    dataset: Annotated[SpeechDataset, Depends(get_dataset)],
):
    model.train_on_data(dataset, epochs=100)
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
