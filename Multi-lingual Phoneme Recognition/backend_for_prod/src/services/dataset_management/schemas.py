from pydantic import BaseModel


class UserDatasetSchema(BaseModel):
    label: str

    class Config:
        orm_mode = True

class DatasetListSchema(BaseModel):
    datasets: list[UserDatasetSchema]
