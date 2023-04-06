import argparse

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import librosa

parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--file",
    required=True,
    help="Path to WAV audio-file to recognize",
)
args = parser.parse_args()

# load model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")

audio_path = args.file

target_sampling_rate = 16000
wf, sr = librosa.load(audio_path, sr=target_sampling_rate)

# tokenize
input_values = processor(wf, sampling_rate=sr, return_tensors="pt").input_values

# retrieve logits
with torch.no_grad():
    logits = model(input_values).logits

# take argmax and decode
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)
print(transcription)
