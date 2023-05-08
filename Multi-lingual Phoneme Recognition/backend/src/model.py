import torch
import torch.nn.functional as F
from torch import nn
import json
import pytorch_lightning as pl

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

f = open("/home/boris/Projects/Voice_Assistant_for_Voice_Anomaly_Persons/Multi-lingual Phoneme Recognition/models/processor/vocab.json")
phonemes: dict[str, int] = json.load(f)
f.close()

phonemes_reverse ={j:i for i, j in phonemes.items()}

params = {
    'batch_size': 4,
    'phonemes': 392
}

abc = "?абвгдеёжзийклмнопрстуфхшщчцьыъэюя"
def vectorize_str(labels: tuple[str]):
    lengths = torch.LongTensor(size=(len(labels),))
    letters = torch.zeros(size=(len(labels),  max(map(len, labels)), len(abc)), dtype=torch.double)
    
    for i, label in enumerate(labels):
        lengths[i] = len(label)
        j=0
        for c in label.lower():
            if not c in abc:
                lengths[i]-=1
            else:
                letters[i,j, abc.index(c)]=1
                # letters[i,j]= abc.index(c)
                j+=1
    
    return letters, lengths
def decode_str(X, pred=True):
    r = []
    for i in range(X.shape[0]):
        s = []
        s1 = []
        for j in range(X.shape[1]):
            if (ix:=X[i,j].argmax()) >= 1:
                s.append(abc[ix])
            s1.append(abc[X[i,j,1:].argmax()+1])
        if not pred:
            r.append(''.join(s)+'/'+''.join(s1))
        else:
            r.append(''.join(s))
    return r

def vectorize_phonemes(labels: tuple[str]):
    lengths = torch.LongTensor(size=(len(labels),))
    letters = torch.zeros(
        size=(
            len(labels),
            max(map(lambda x: len(x.split()), labels)),
            params['phonemes']
        ),
        dtype=torch.float
    )
    # letters = torch.zeros(size=(len(labels),  max(map(len, labels))), dtype=float)

    for i, label in enumerate(labels):
        lengths[i] = len(label.split())
        for j, c in enumerate(label.split()):
            letters[i,j, phonemes[c]]=1
    
    return letters, lengths
def decode_phonemes(X):
    r = []
    for i in range(X.shape[0]):
        s = []
        for j in range(X.shape[1]):
            if X[i,j].argmax() >= 0:
                s.append(phonemes_reverse[int(X[i,j].argmax())])
        r.append(''.join(s))
    return r

class Conv1DCorrector(pl.LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.conv = nn.Conv1d(
            params['phonemes'],
            20,
            3,
            padding=1
        )

        self.lstm = nn.LSTM(20, 40, batch_first=True)
        self.linear = nn.Linear(40, len(abc))

    def forward(self, x: torch.Tensor):
        # x: batch x len x phonemes
        x = x.permute(0,2,1)
        # x = x.reshape(x.shape[0], 1, x.shape[1], x.shape[2])# x: batch x 1 x phonhemes x len
        x = self.conv(x)
        x = x.permute(0,2, 1)
        x, (h, c) = self.lstm(x)
        x = self.linear(x)
        return F.log_softmax(x, -1)
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters())
    def training_step(self, train_batch, batch_idx):
        labels, lengths = vectorize_str(train_batch[1])
        phonemes_vec, _ = vectorize_phonemes(train_batch[2])
        
        prediction = self(phonemes_vec.to(device))
        
        ilengths = lengths.clone()
        for i in range(prediction.shape[0]):
            ilengths[i] = prediction.shape[1]
        
        lv = F.ctc_loss(prediction.permute(1, 0, 2), labels.argmax(dim=-1), ilengths, lengths, zero_infinity=True)
        
        if batch_idx==0:
            logging.info("train \"%s\" recognized as \"%s\"", '|'.join(decode_str(labels, False)), '|'.join(decode_str(prediction)))
        
        self.log('train_loss', lv, True, batch_size=len(train_batch))
        return lv
    def validation_step(self, train_batch, batch_idx):
        labels, lengths = vectorize_str(train_batch[1])
        phonemes_vec, _ = vectorize_phonemes(train_batch[2])
        
        prediction = self(phonemes_vec.to(device))
        
        ilengths = lengths.clone()
        for i in range(prediction.shape[0]):
            ilengths[i] = prediction.shape[1]
        
        lv = F.ctc_loss(prediction.permute(1, 0, 2), labels.argmax(dim=-1), ilengths, lengths, zero_infinity=True)

        if batch_idx==0:
            logging.info("val \"%s\" recognized as \"%s\"", '|'.join(decode_str(labels, False)), '|'.join(decode_str(prediction)))
        
        self.log('val_loss', lv, True, batch_size=len(train_batch))
