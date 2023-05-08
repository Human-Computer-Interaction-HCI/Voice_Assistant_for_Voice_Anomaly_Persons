from typing import Annotated
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch

import model as m
from schemas import RecognitionResultSchema, PhonemeRecognitionRequest

app = FastAPI(root_path="http://localhost:8000")


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



processor = Wav2Vec2Processor.from_pretrained("/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/models/processor")
model = Wav2Vec2ForCTC.from_pretrained("/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/models/phonemizer")
corrector = m.Conv1DCorrector.load_from_checkpoint('models/corrector.ckpt')


@app.post("/recognize/phonemes", response_model=RecognitionResultSchema)
async def recognize_phonemes(file: Annotated[UploadFile, File(description="WAV audiofile to recognize", media_type="audio/wav")]):
    # if file.content_type not in ["audio/vnd.wave", 'audio/wav']:
    #     raise HTTPException(status.HTTP_400_BAD_REQUEST)
    out_path = tempfile.mktemp('.wav')
    with open(out_path, 'wb') as out_file:
        content = await file.read()
        out_file.write(content)

    wf, sr = librosa.load(out_path, sr=16000)

    tokens = processor(wf, sampling_rate=sr, return_tensors="pt").input_values

    with torch.no_grad():
        logits = model(tokens).logits
    
    prediction = torch.argmax(logits, -1)
    transcription = processor.batch_decode(prediction)

    return {
        "result": " ".join(transcription)
    }

@app.post('/recognize/phoneme_to_text')
def recognize(data: PhonemeRecognitionRequest):
    phonemes, _ = m.vectorize_phonemes([data.phonemes])
    result = corrector(phonemes)
    return {'result': m.decode_str(result, False)}
