import subprocess

import librosa
import torch


def get_audio(path: str):
    return torch.Tensor(librosa.load(path, sr=16000)[0]).view(1, -1)


def webm_to_wav(path: str, out_path: str):
    subprocess.run(["ffmpeg", "-i", path, out_path])


abc = "?абвгдеёжзийклмнопрстуфхшщчцьыъэюя "

def clear_str(s):
    return "".join(i for i in s.lower() if i in abc)


def str_to_tensor(strs: list[str]) -> tuple[torch.Tensor, torch.Tensor]:
    lengths = torch.zeros((len(strs),), dtype=int)
    result = []
    for idx, i in enumerate(strs):
        result.append([abc.index(j) for j in i.lower() if j in abc[1:]])
        lengths[idx] = len(result[-1])
    res_tensor = torch.zeros((len(strs), lengths.max().item()))
    for idx0, i in enumerate(result):
        for idx1, c in enumerate(i):
            res_tensor[idx0, idx1] = c
    return res_tensor, lengths

def to_str(r):
    return ''.join(abc[j] for j in r)

def get_y_lengths(y):
    return torch.ones(y.shape[0], dtype=int)*y.shape[-2]
