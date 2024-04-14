import os

from fastapi.testclient import TestClient
import pandas as pd

from app import app

dirs_dirs = [
    "/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/Борис. Фразы(0-100)",
    "/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/Борис. Фразы(101-238",
    "/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/Борис. Фразы(239-399)"
]

ds = pd.read_excel('/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/raw_kaggle/Speeches.xlsx')

data = {}

for directory in dirs_dirs:
    for f in os.listdir(directory):
        fp = f'{directory}/{f}'
        try:
            lbl = ds.iloc[int(f.removesuffix('.m4a'))-1]['Русская речь']
            data[fp] = lbl
        except IndexError:
            pass

# data = {
#     '/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/Борис. Фразы(0-100)/23.m4a': 'Лабиринт',
#     '/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/Борис. Фразы(0-100)/38.m4a': 'Спектакль уже начался',
#     '/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/Борис. Фразы(0-100)/39.m4a': 'Музей',
#     '/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/Борис. Фразы(0-100)/59.m4a': 'отпечаток пальца',
#     '/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/Борис. Фразы(0-100)/63.m4a': 'Аршин проглотил',
#     '/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/Борис. Фразы(0-100)/124.m4a': 'Работать',
#     '/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/Борис. Фразы(0-100)/131.m4a': 'На Се́верный по́люс?',
#     '/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/data/Борис. Фразы(0-100)/159.m4a': 'Почему все так сложно',
# }

client = TestClient(app)


def test_recognize():
    for path, label in data.items():
        f = open(path, 'rb')
        response = client.post("/predict", files={
            'file': f
        })
        f.close()
        assert response.status_code == 200
        rj = response.json()
        client.post('/label', json={
            'request_id': rj['request_id'],
            'label': label
        })
    client.post('/train', json={})
    
    for path, label in data.items():
        f = open(path, 'rb')
        response = client.post("/predict", files={
            'file': f
        })
        f.close()
        assert response.status_code == 200
        rj = response.json()
        assert rj['result'] == label, f'Неверно распознана фраза {rj["result"]}'
