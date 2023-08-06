from contextlib import asynccontextmanager
from typing import Annotated
import tempfile
import subprocess

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from Levenshtein import ratio
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch

import model as m
from schemas import (
    FineTuningRequest,
    RecognitionResultSchema,
    PhonemeRecognitionRequest,
)
from services.hmmcorrector import HMMCorrector


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    hmm_corrector.save("corrector.npy")


app = FastAPI(root_path="http://localhost:8000", lifespan=lifespan)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


processor = Wav2Vec2Processor.from_pretrained(
    "/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/models/processor"
)
model = Wav2Vec2ForCTC.from_pretrained(
    "/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/models/phonemizer"
)
# corrector = m.Conv1DCorrector.load_from_checkpoint("models/corrector.ckpt")

hmm_corrector = HMMCorrector("models/vocab.json", "corrector.npy")

W=['он', 'когда', 'ночь', 'занемог', 'не', 'мог', 'его', 'скука', 'подносить', 'сидеть', 'шагу', 'не', 'возьмет', 'пример', 'думать', 'коварство', 'прочь', 'заставил', 'мой', 'лучше', 'подушки', 'себя', 'же', 'лекарство', 'боже', 'какое', 'другим', 'тебя', 'ему', 'выдумать', 'низкое', 'с', 'полуживого', 'уважать', 'отходя', 'больным', 'самых', 'поправлять', 'печально', 'правил', 'день', 'честных', 'и', 'в', 'но', 'и', 'шутку', 'дядя', 'черт', 'про', 'ни', 'наука', 'мой', 'забавлять', 'какая', 'вздыхать']

@app.post("/recognize/phonemes", response_model=RecognitionResultSchema)
async def recognize_phonemes(
    file: Annotated[
        UploadFile,
        File(description="WAV audiofile to recognize", media_type="audio/wav"),
    ]
):
    # if file.content_type not in ["audio/vnd.wave", 'audio/wav']:
    #     raise HTTPException(status.HTTP_400_BAD_REQUEST)
    out_path = tempfile.mktemp(".webm")
    with open(out_path, "wb") as out_file:
        content = await file.read()
        out_file.write(content)

    subprocess.run(["ffmpeg", "-i", out_path, out_path + ".wav"])

    wf, sr = librosa.load(out_path + ".wav", sr=16000)

    tokens = processor(wf, sampling_rate=sr, return_tensors="pt").input_values

    with torch.no_grad():
        logits = model(tokens).logits

    prediction = torch.argmax(logits, -1)
    transcription = processor.batch_decode(prediction)

    return {"result": " ".join(transcription)}


@app.post("/recognize/phonemes_to_text", response_model=RecognitionResultSchema)
def recognize(data: PhonemeRecognitionRequest):
    phonemes = data.phonemes.split()
    result, _ = hmm_corrector.predict(phonemes)
    # r=[]
    # # Ищем самое близкое слово
    # st=0
    # while st < len(result):
    #     md=0
    #     mw=''
    #     for i in range(len(result),st,-1):
    #         for w in W:
    #             distance = ratio(w, result[st:i])
    #             if distance>md:
    #                 st1=i
    #                 md=distance
    #                 mw=w
    #     st = st1
    #     r.append(mw)
    return {"result": f'{result}'}


@app.post("/recognize/fine_tune")
def fine_tune(data: FineTuningRequest):
    hmm_corrector.study_pairs(data.phonemes.split(), data.text)
    return {}
