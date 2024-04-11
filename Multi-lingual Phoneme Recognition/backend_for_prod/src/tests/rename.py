import os

path = "/home/boris/projects/VoiceSpeaker/Multi-lingual Phoneme Recognition/backend_for_prod/src/data/"

files = os.listdir(path)

for fp in files:
    if fp.endswith(".m4a.wav"):
        os.rename(path + fp, path + fp.replace(".m4a", ".webm"))
                
