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

def decode(X):
    return processor.batch_decode(X)

# usage


# df = pd.read_csv('/home/boris/Projects/МИиМИС/Курсовая/speech_recognition/data/dataset.csv')
# X=recognize(df.iloc[0:3]['abnormal'])
# decode(torch.argmax(X, dim=-1))

# processor.save_pretrained('models/processor')
# model.save_pretrained('models/phonemizer')
