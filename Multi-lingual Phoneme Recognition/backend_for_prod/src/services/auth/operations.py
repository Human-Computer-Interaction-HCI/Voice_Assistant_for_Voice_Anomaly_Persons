from sqlalchemy.orm import Session

from db_models import User, UserDataset, UserModel

def create_default_user_dataset_and_model(db: Session, user: User):
    dataset = UserDataset()
    dataset.user_id = user.login

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    model = UserModel()
    model.user_id = user.login
    model.dataset_id = dataset.dataset_id
    model.label = 'default'

    db.add(model)
    db.commit()
    db.refresh(model)