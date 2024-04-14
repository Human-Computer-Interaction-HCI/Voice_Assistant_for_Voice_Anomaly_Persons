from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ai_utils.dataset import SpeechDataset
from ai_utils.dependencies import get_model, get_dataset, Model
from database import get_db
from db_models import User, UserDataset, UserModel
from services.auth.utils import get_current_user

router = APIRouter()


@router.get("/info")
def model_id(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    model_obj = db.query(UserModel).filter(UserModel.user_id == user.login).first()
    return {"id": model_obj.model_id}


@router.post("/train")
async def train(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    model: Annotated[Model, Depends(get_model)],
    user_dataset: Annotated[UserDataset, Depends(get_dataset)],
):
    print('Start train')
    dataset = SpeechDataset()
    for i in user_dataset.recordings:
        if i.label:
            dataset.add_audio(recording_id_to_path(i.recording_id), i.label)
    model.train_on_data(dataset, epochs=100)
    # todo: refactor model saving
    model.save(f'data/models/{db.query(UserModel).filter(UserModel.user_id == user.login).first().model_id}')
    return {"status": "ok"}

#######################

def recording_id_to_path(recording_id: str):
    return f"/home/boris/projects/VoiceSpeaker/Multi-lingual Phoneme Recognition/backend_for_prod/src/data/{recording_id}.webm.wav"
