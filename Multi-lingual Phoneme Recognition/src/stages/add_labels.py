import csv
import re
from pathlib import Path

labels_fd = open('/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/dv3.csv')
labels_reader = csv.reader(labels_fd)

words: dict[int, str] = {}
for line in labels_reader:
    words[int(line[0])] = line[1]

labels_fd.close()

def is_path(s: str) -> bool:
    return s[0]=='/'

dataset_fd = open('/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/xls-r_dataset_v3.csv')


audio_id_regexp = re.compile(r'\d+\.wav$')
def get_audio_id(path: Path) -> int:
    return int(re.search(audio_id_regexp, str(path)).group(0)[:-4])

new_ds = open('/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/xls-r_dataset_v4.csv', 'w')
new_ds_writer = csv.writer(new_ds)

for line in csv.reader(dataset_fd):
    id_, text, transcription = line
    if id_ == '':
        continue
    if is_path(text):
        text = words[get_audio_id(text)]
    else:
        print(text)
    new_ds_writer.writerow((id_, text, transcription ))
new_ds.close()