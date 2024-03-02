from torch import nn
import torchaudio

from .dataset import padded_stack

train_transforms = torchaudio.transforms.MelSpectrogram(n_mels=128)


class Model(nn.Module):
    def __init__(self):
        super().__init__()

        self.rnn = nn.GRU(128, 256, 1, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(256 * 2, 34)
        self.act = nn.LogSoftmax(-1)
    
    def forward(self, x):
        # X: batch x 128 x len
        x = x[:, :, ::4]
        x = x.permute(0,2,1)
        x, _ = self.rnn(x)
        x = self.fc(x)
        x = self.act(x)
        return x
    
    def predict(self, x):
        spectrogram = [train_transforms(x).permute(0, 2, 1)]
        spectrogram = padded_stack(spectrogram).permute(0, 2, 1)
        output = self(spectrogram)
        return output.argmax(-1)
 
