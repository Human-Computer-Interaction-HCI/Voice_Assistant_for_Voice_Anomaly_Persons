import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from ai_utils.dataset import SpeechDataset
from ai_utils.model import Model
from database import get_db
from db_models import User, UserDataset, UserModel
from services.auth.utils import get_current_user


def get_model(user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> Model | None:
    model_obj = db.query(UserModel).filter(UserModel.user_id == user.login).first()
    if model_obj is None:
        return None
    
    if not os.path.exists(f'data/models/{model_obj.model_id}'):
        Model().save(f'data/models/{model_obj.model_id}')
    return Model.load(f'data/models/{model_obj.model_id}')

def get_dataset(user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> UserDataset | None:
    return db.query(UserDataset).filter(UserDataset.user_id == user.login).first()


