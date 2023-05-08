import requests

root_server = 'http://localhost:8000'

def test_phoneme_recognition():
    sample_wav = '/home/boris/Yandex.Disk/UrFU/магистратура/диссертация/датасет 2/wavs/577.wav'
    f = open(sample_wav, 'rb')
    resp = requests.post(f'{root_server}/recognize/phonemes', files={'file': f})
    f.close()
    assert resp.json()['result'] == 'ɪ z ə n k r a ç t o v a n e m b a v a v l ɔ k a x z ə k r a t v ɔ ɔ n e t ʌ v s a v a ŋ ɡ a x'

def test_phonemes_to_text():
    resp = requests.post(f'{root_server}/recognize/phoneme_to_text', json={
        'phonemes': 'ɪ z ə n k r a ç t o v a n e m b a v a v l ɔ k a x z ə k r a t v ɔ ɔ n e t ʌ v s a v a ŋ ɡ a x'
    })
    r = resp.json()['result']
    assert '/' not in r, r
