import httpx
import pandas as pd

directory = (
    "/home/boris/projects/VoiceSpeaker/Multi-lingual Phoneme Recognition/data/raw_kaggle/Disorder Voices/Disorder Voices"
)

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcxMzY5NDY1Mn0.sEv27hOU34m7JYnfR2NHIBNzPYzA09IwvtKYt_jVglc"
}

ds = pd.read_excel("/home/boris/projects/VoiceSpeaker/Multi-lingual Phoneme Recognition/data/raw_kaggle/Speeches.xlsx")
ds.head()

for _, row in ds.iterrows():
    audio_id = row.iloc[0]
    label = row.iloc[1]
    if len(label)>100:
        continue
    print(audio_id)
    
    fp = f'{directory}/{audio_id}.wav'
    try:
        resp = httpx.post(f'http://localhost:8000/predict', headers=headers, files={'file': open(fp, 'rb')})
        request_id = resp.json()['request_id']
        httpx.post(f'http://localhost:8000/label', headers=headers, json={'request_id': request_id, 'label': label})
    except Exception as e:
        print(e)
        break

