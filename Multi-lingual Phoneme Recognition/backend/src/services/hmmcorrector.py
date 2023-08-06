from collections import Counter, defaultdict
import json
from typing import Iterable

import numpy as np

abc_to_idx:dict[str, int]={c:i for i, c in enumerate('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')}
idx_to_abc:dict[int, str] = {i:c  for c, i in abc_to_idx.items()}


class HMMCorrector:
    _state: np.ndarray
    eps: float
    
    def __init__(self, vocab:str, load=None, eps: float = 0.25) -> None:
        '''
        :param load: path to saved model
        '''
        self._state = np.ones((392, 33))/33
        self.eps = eps
        if load:
            try:
                self._state = np.load(load)
            except FileNotFoundError:
                self._state = np.ones((392, 33))/33

        f = open(vocab)
        self.phonemes: dict[str, int] = json.load(f)
        f.close()

        self.phonemes_reverse: dict[int, str] ={j:i for i, j in self.phonemes.items()}

    @staticmethod
    def get_triplets(ipa: list[str], text: str) -> Iterable[tuple[tuple[str, str], str]]:
        for i in range(min(len(ipa)-1, len(text))):
            yield (ipa[i], ipa[i+1]), text[i]
    
    @staticmethod
    def prepare_text(raw: str) -> str:
        return ''.join(i.lower() for i in raw if i.isalpha())
    
    def study_pairs(self, ipa: list[str], text: str):
        temp_matrix = np.zeros_like(self._state)
        for phoneme, letter in zip(ipa, text):
            if letter=='_':
                continue
            temp_matrix[self.phonemes[phoneme], abc_to_idx[letter]]+=1
        for row_idx in range(temp_matrix.shape[0]):
            if (s:=temp_matrix[row_idx, :].sum())>0:
                self._state[row_idx, :] = self._state[row_idx, :] * self.eps + temp_matrix[row_idx, :] * (1-self.eps)/s
        return
        text = self.prepare_text(text)

        for phoneme_bigram, letter in self.get_triplets(ipa, text):
            self._state[phoneme_bigram][letter] += 1
    
    def predict(self, ipa: list[str]) -> tuple[str, list[np.ndarray]]:
        result: list[np.ndarray] = []
        rs = ''

        for i in range(len(ipa)-1):
            phoneme_bigram_idx = self.phonemes[ipa[i]]#*len(self.phonemes)+self.phonemes[ipa[i+1]]
            distribution = self._state[phoneme_bigram_idx]
            result.append(distribution)
            rs += idx_to_abc[int(np.random.choice(np.arange(len(idx_to_abc)), p=distribution))]

        return rs, result
    
    def save(self, path):
        np.save(path, self._state)