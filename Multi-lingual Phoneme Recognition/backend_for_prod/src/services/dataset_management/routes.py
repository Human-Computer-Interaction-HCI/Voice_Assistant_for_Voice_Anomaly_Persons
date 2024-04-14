from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from db_models import User, UserDataset, UserRecording
from services.auth.utils import get_current_user

from .schemas import DatasetListSchema

router = APIRouter()


@router.get("/list")
def list_datasets(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> DatasetListSchema:
    return {
        'datasets': db.query(UserDataset).filter(UserDataset.user_id == user.login).all()
    }

@router.get('/ds')
def list_recordings(label: str,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    dataset = db.query(UserDataset).filter(UserDataset.user_id == user.login).filter(UserDataset.label == label).first()
    recordings = db.query(UserRecording).filter(UserRecording.dataset_id == dataset.dataset_id).all()

    return {
        'recordings': recordings
    }