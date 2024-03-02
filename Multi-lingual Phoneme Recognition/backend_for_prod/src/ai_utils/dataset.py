import torch
from torch.utils.data import Dataset

from utils import get_audio


class SpeechDataset(Dataset):
    """
    мический вариант датасета для аудио.
    Позволяет добавлять аудио с разметкой в существующий объект.
    """

    def __init__(self):
        self.audio_list = []
        self.label_list = []

    def add_audio(self, audio, label):
        self.audio_list.append(audio)
        self.label_list.append(label)

    def __len__(self):
        return len(self.audio_list)

    def __getitem__(self, idx):
        return get_audio(self.audio_list[idx]), self.label_list[idx]
    
    @staticmethod
    def collate(batch):
        wfs, lbls = [], []
        for audio, label in batch:
            wfs.append(audio)
            lbls.append(label)
        return wfs, lbls

def padded_stack(list_of_tensors, maxlen=16):
    maxlen = max(x.shape[1] for x in list_of_tensors)
    output = torch.zeros((len(list_of_tensors), maxlen, list_of_tensors[0].shape[-1]))
    for i, t in enumerate(list_of_tensors):
        output[i, :min(maxlen, t.shape[1]), :] = t[0,:maxlen, :]
    return output
