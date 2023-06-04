from collections import Counter, defaultdict
import json
from typing import Iterable


class HMMCorrector:
    _state: defaultdict[tuple[str, str], Counter]
    
    def __init__(self, load=None) -> None:
        '''
        :param load: path to saved model
        '''
        self._state = defaultdict(lambda: Counter())
        if load:
            with open(load, 'rb') as f:
                obj = json.load(f)
                for p1, ps in obj.items():
                    for p2, ls in ps.items():
                        for i, l in ls.items():
                            self._state[(p1, p2)][i]  = l

    @staticmethod
    def get_triplets(ipa: list[str], text: str) -> Iterable[tuple[tuple[str, str], str]]:
        for i in range(min(len(ipa)-1, len(text))):
            yield (ipa[i], ipa[i+1]), text[i]
    
    @staticmethod
    def prepare_text(raw: str) -> str:
        return ''.join(i.lower() for i in raw if i.isalpha())
    
    def study_pairs(self, ipa: list[str], text: str):
        text = self.prepare_text(text)

        for phoneme_bigram, letter in self.get_triplets(ipa, text):
            self._state[phoneme_bigram][letter] += 1
    
    def predict(self, ipa: list[str]) -> str:
        result: list[str] = []

        for i in range(len(ipa)-1):
            r = self._state[(ipa[i], ipa[i+1])].most_common(1)
            if len(r)>0:
                result.append(r[0][0])

        return ''.join(result)
    
    def save(self, path):
        with open(path, 'w') as f:
            json.dump({i[0]:{i[1]: dict(j)} for i,j in self._state.items()}, f, ensure_ascii=False)
