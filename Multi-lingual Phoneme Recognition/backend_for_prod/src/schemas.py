from pydantic import BaseModel

class PredictionSchema(BaseModel):
    result: str
    request_id: str

class LabelingRequestSchema(BaseModel):
    request_id: str
    label: str
