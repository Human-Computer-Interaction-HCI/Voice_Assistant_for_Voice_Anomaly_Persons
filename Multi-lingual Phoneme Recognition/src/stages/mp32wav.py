import os
from pathlib import Path
import re
import subprocess

import dvc.api
import tqdm

params = dvc.api.params_show()['mp3ToWAV']

raw_audio_path = list(Path(params['raw_audio']).glob('*.mp3'))
out_path = Path(params['processed_audio'])

if not out_path.exists():
    os.mkdir(out_path)

audio_id_regexp = re.compile(r'\d+\.mp3$')
def get_audio_id(path: Path) -> int:
    return int(re.search(audio_id_regexp, str(path)).group(0)[:-4])

for i in tqdm.tqdm(raw_audio_path):
    out_file_path = out_path / f'{get_audio_id(i)}.wav'
    if out_file_path.exists():
        continue
    subprocess.run(['ffmpeg', '-i', str(i), out_file_path])
