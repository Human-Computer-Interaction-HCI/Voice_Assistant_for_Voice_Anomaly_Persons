from pathlib import Path

import pandas as pd
import tqdm

from xls_r_decoder.wav2phonemes import recognize, decode

df = pd.read_csv("/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/xls-r_dataset.csv")

wav_dir = '/home/boris/Yandex.Disk/UrFU/магистратура/диссертация/датасет 2/wavs2/v2'


raw_audio_path = list(Path(wav_dir).glob('*.wav'))

new_df = []

for audio in tqdm.tqdm(raw_audio_path):
    new_df.append([audio, "unknown", decode(recognize([audio]).argmax(-1))[0]])

print(*new_df, sep='\n')

with open('датасет3.csv', 'w') as f:
    f.write(',text,IPA\n')
    for i in new_df:
        f.write(f'{i[0]},{i[1]},{i[2]}\n')