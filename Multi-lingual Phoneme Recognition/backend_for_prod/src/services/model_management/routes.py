from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ai_utils.dataset import SpeechDataset
from ai_utils.dependencies import get_model, get_dataset, Model
from database import get_db
from db_models import User, UserModel
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
    model: Annotated[Model, Depends(get_model)],
    dataset: Annotated[SpeechDataset, Depends(get_dataset)],
):
    model.train_on_data(dataset, epochs=100)
    return {"status": "ok"}
