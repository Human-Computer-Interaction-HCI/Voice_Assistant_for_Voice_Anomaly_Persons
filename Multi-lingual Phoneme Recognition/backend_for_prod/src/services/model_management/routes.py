from secrets import token_urlsafe
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from ai_utils.dataset import SpeechDataset
from ai_utils.dependencies import get_model, get_dataset, Model, get_model_id
from ai_utils.metric_store import MetricStore
from database import get_db
from db_models import User, UserDataset, UserModel
from services.auth.utils import get_current_user
from tasks import train_model

router = APIRouter()


@router.get("/info")
def model_id(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    model_obj = db.query(UserModel).filter(UserModel.user_id == user.login).first()
    return {"id": model_obj.model_id}


@router.post("/train")
def train(
    model_id: Annotated[int, Depends(get_model_id)],
    user_dataset: Annotated[UserDataset, Depends(get_dataset)],
    background_tasks: BackgroundTasks,
):
    print("Start train")
    dataset = []
    for i in user_dataset.recordings:
        if i.label:
            dataset.append((recording_id_to_path(i.recording_id), i.label))

    task_id = token_urlsafe(8)

    # train_model.delay(model_id, dataset, task_id)/
    background_tasks.add_task(train_model, model_id, dataset, task_id)

    return {"task_id": task_id}


@router.get("/metrics")
def get_metrics(task_id: str):
    return MetricStore([], task_id).get_metrics()


@router.get("/current_metrics")
def get_current_metrics(
    model: Annotated[Model, Depends(get_model)],
    user_dataset: Annotated[UserDataset, Depends(get_dataset)],
):
    dataset = SpeechDataset()
    for i in user_dataset.recordings:
        if i.label:
            dataset.add_audio(recording_id_to_path(i.recording_id), i.label)
    return model.get_metrics(dataset)


#######################


def recording_id_to_path(recording_id: str):
    return f"/home/boris/projects/VoiceSpeaker/Multi-lingual Phoneme Recognition/backend_for_prod/src/data/{recording_id}.webm.wav"
