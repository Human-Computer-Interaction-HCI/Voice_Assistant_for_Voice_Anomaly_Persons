from pydantic import BaseModel, Field

class RecognitionResultSchema(BaseModel):
    result: str = Field(title="Результат распознавания")

class PhonemeRecognitionRequest(BaseModel):
    phonemes: str
