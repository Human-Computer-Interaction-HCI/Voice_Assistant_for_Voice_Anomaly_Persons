import os
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, File, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from ai_utils.dependencies import get_model, Model
from database import get_db
from db_models import User, UserDataset, UserRecording
from services.auth.routes import router as auth_router
from services.auth.utils import get_current_user
from services.dataset_management.routes import router as dataset_management_router
from services.model_management.routes import router as model_management_router
from schemas import LabelingRequestSchema, PredictionSchema
from utils import get_audio, to_str, webm_to_wav

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
    user: Annotated[User, Depends(get_current_user)],
):
    request_id = secrets.token_urlsafe(8)
    out_path = f"{data_dir}/{request_id}.webm"
    with open(out_path, "wb") as f:
        f.write(await file.read())

    webm_to_wav(out_path, out_path + ".wav")

    os.remove(out_path)

    audio = get_audio(out_path + ".wav")

    result = model.predict(audio).argmax(-1)[0]

    default_ds = (
        db.query(UserDataset)
        .filter(UserDataset.label == "default", UserDataset.user_id == user.login)
        .first()
    )

    recording = UserRecording()
    recording.recording_id = request_id
    recording.dataset_id = default_ds.dataset_id

    db.add(recording)
    db.commit()

    return {"result": to_str(result), "request_id": request_id}


@app.get("/predict", response_model=PredictionSchema)
async def predict(
    request_id: str,
    model: Annotated[Model, Depends(get_model)],
    response: Response
):
    out_path = f"{data_dir}/{request_id}.webm"  # revert to.wav
    try:
        audio = get_audio(out_path + ".wav")
    except FileNotFoundError:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"result": "File not found", "request_id": request_id}

    result = model.predict(audio).argmax(-1)[0]

    return {"result": to_str(result), "request_id": request_id}


@app.post("/label")
async def label(
    data: LabelingRequestSchema,
    db: Annotated[Session, Depends(get_db)],
):
    recording = (
        db.query(UserRecording)
        .filter(UserRecording.recording_id == data.request_id)
        .first()
    )
    recording.label = data.label
    db.commit()
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(dataset_management_router, prefix="/datasets", tags=["ds"])
app.include_router(model_management_router, prefix="/model", tags=["model"])
