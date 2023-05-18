from pathlib import Path

import tqdm

from xls_r_decoder.wav2phonemes import recognize_chunked, decode

wav_dir = '/home/boris/Yandex.Disk/UrFU/магистратура/диссертация/датасет 3/wavs'

chunk_size = 15 # seconds

with open('датасет6.csv', 'a') as f:
    f.write(',text,IPA\n')
    for audio in tqdm.tqdm(Path(wav_dir).glob('*.wav'), total=1000):
        phonemes = ''
        for i in recognize_chunked(audio, chunk_size):
            phonemes += decode(i.argmax(-1))[0]+' '
        i=[audio, "unknown", phonemes]
        print(i[2])
        f.write(f'{i[0]},{i[1]},{i[2]}\n')