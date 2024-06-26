from pydantic import BaseModel


class UserDatasetSchema(BaseModel):
    label: str

    class Config:
        from_attributes = True

class DatasetListSchema(BaseModel):
    datasets: list[UserDatasetSchema]
