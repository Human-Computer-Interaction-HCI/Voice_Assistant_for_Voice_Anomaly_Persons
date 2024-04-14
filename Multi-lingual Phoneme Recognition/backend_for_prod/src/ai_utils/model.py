from collections import deque
from os import PathLike
from typing import Self

from torch import nn
from torch.utils.data import DataLoader
import torch
import torchaudio

from .dataset import SpeechDataset, padded_stack
from utils import get_y_lengths, str_to_tensor

train_transforms = torchaudio.transforms.MelSpectrogram(n_mels=128)


class ResidualBlock(nn.Module):
    def __init__(self, in_channels, hidden_channels, kernel_size, stride, padding):
        super().__init__()
        self.conv1 = nn.Conv1d(
            in_channels, hidden_channels, kernel_size, stride, padding
        )
        self.conv2 = nn.Conv1d(
            hidden_channels, in_channels, kernel_size, stride, padding
        )
        self.relu = nn.ReLU()
        self.batchnorm1 = nn.BatchNorm1d(hidden_channels)
        self.batchnorm2 = nn.BatchNorm1d(in_channels)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        out = self.conv1(x)
        out = self.batchnorm1(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.conv2(out)
        out = self.batchnorm2(out)
        out = self.relu(out)
        out = self.dropout(out)
        return out + x


class Model(nn.Module):
    def __init__(self):
        super().__init__()

        self.cnn = nn.Sequential(
            nn.Conv1d(in_channels=128, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm1d(64),
            nn.Dropout1d(0.1),
            nn.MaxPool1d(2),
            ResidualBlock(64, 128, 3, 1, 1),
            nn.ReLU(),
            ResidualBlock(64, 128, 3, 1, 1),
            nn.ReLU(),
            ResidualBlock(64, 128, 3, 1, 1),
            nn.ReLU(),
            nn.Dropout1d(0.1),
            nn.MaxPool1d(2),
        )
        self.rnn = nn.GRU(
            input_size=64,
            hidden_size=32,
            num_layers=1,
            batch_first=True,
            bidirectional=True,
        )

        self.fc = nn.Linear(64, 35)
        self.act = nn.LogSoftmax(-1)

    def forward(self, X):
        # X: batch x 128 x len
        # X = X[:,:,::4]
        X = self.cnn(X)
        X = X.permute(0, 2, 1)
        X, _ = self.rnn(X)
        X = self.fc(X)
        X = self.act(X)
        return X

    def predict(self, x):
        if isinstance(x, list):
            spectrogram = [train_transforms(i).permute(0, 2, 1) for i in x]
        else:
            spectrogram = [train_transforms(x).permute(0, 2, 1)]
        spectrogram = padded_stack(spectrogram).permute(0, 2, 1)
        output = self(spectrogram)
        return output

    def train_on_data(
        self,
        dataset: SpeechDataset,
        /,
        epochs: int | None = None,
        loss_delta: float | None = 0.01,
        cer_delta: float | None = 0.01,
        batches_per_step: int = 1,
        plateu_length: int = 5,
    ):
        """
        cer_delta: пока игнорируется
        """

        dataloader = DataLoader(
            dataset, batch_size=4, shuffle=True, collate_fn=SpeechDataset.collate
        )
        last_losses = deque(maxlen=plateu_length)

        self.train()

        loss_function = nn.CTCLoss(zero_infinity=True)
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)

        optimizer.zero_grad()

        epoch = 0

        while True:
            epoch += 1
            last_losses.append(0)
            print(f"Epoch: {epoch}/{epochs}")
            if epochs is not None and epoch > epochs:
                break

            for bn, batch in enumerate(dataloader):
                output = self.predict(batch[0])
                target_t, target_len = str_to_tensor(batch[1])
                loss = loss_function(
                    output.permute(1, 0, 2), target_t, get_y_lengths(output), target_len
                )
                loss.backward()

                last_losses.append(last_losses[-1]+loss.item())
                if bn % batches_per_step == 0:
                    optimizer.step()
                    optimizer.zero_grad()

            if (
                len(last_losses) == plateu_length
                and abs(last_losses[-1] - sum(last_losses) / len(last_losses))
                < loss_delta
            ):
                break
            
            print(last_losses[-1])

    def save(self, path: PathLike):
        torch.save(self.state_dict(), path)

    @classmethod
    def load(cls, path: PathLike) -> Self:
        self = cls()
        self.load_state_dict(torch.load(path))
        self.eval()
        return self
