import httpx
import pandas as pd

directory = (
    "/home/boris/projects/VoiceSpeaker/Multi-lingual Phoneme Recognition/data/Ilya"
)

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcxMjc0MjgxNH0.7dWXazwL_yDqKvkwken9YnJLvCmNWQBla4nHx1vYs0s"
}

ds = pd.read_excel(directory + "/markup.xlsx")
ds.head()

for _, row in ds.iterrows():
    audio_id = row.iloc[0]
    label = row.iloc[2]
    fp = f'{directory}/{audio_id}.m4a'
    try:
        resp = httpx.post(f'http://localhost:8000/predict', headers=headers, files={'file': open(fp, 'rb')})
        request_id = resp.json()['request_id']
        httpx.post(f'http://localhost:8000/label', headers=headers, json={'request_id': request_id, 'label': label})

