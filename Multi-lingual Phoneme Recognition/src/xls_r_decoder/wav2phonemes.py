from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import librosa

processor = Wav2Vec2Processor.from_pretrained("/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/models/processor")
model = Wav2Vec2ForCTC.from_pretrained("/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/models/phonemizer")

def recognize(file_path: list[str]) -> torch.Tensor:
    target_sampling_rate = 16000
    wf = []
    for i in file_path:
        wf_, sr = librosa.load(i, sr=target_sampling_rate)
        wf.append(wf_)

    # tokenize
    input_values = processor(wf, sampling_rate=sr, return_tensors="pt", padding=True).input_values

    # retrieve logits
    with torch.no_grad():
        logits = model(input_values).logits

    return logits

def recognize_chunked(file_path: str, chunk_size=5) -> torch.Tensor:
    target_sampling_rate = 16000
    wf = []
    duration = librosa.get_duration(path=file_path)
    delta = 0
    while delta < duration:
        wf_, sr = librosa.load(file_path, sr=target_sampling_rate, offset=delta, duration=chunk_size)
        # tokenize
        input_values = processor(wf_, sampling_rate=sr, return_tensors="pt", padding=True).input_values

        # retrieve logits
        with torch.no_grad():
            logits = model(input_values).logits

        yield logits

        delta += chunk_size

def decode(X):
    return processor.batch_decode(X)

# usage


# df = pd.read_csv('/home/boris/Projects/МИиМИС/Курсовая/speech_recognition/data/dataset.csv')
# X=recognize(df.iloc[0:3]['abnormal'])
# decode(torch.argmax(X, dim=-1))

# processor.save_pretrained('models/processor')
# model.save_pretrained('models/phonemizer')
