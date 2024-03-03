from collections import deque

from torch import nn
from torch.utils.data import DataLoader
import torch
import torchaudio

from .dataset import SpeechDataset, padded_stack
from utils import get_y_lengths, str_to_tensor

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
        x = x.permute(0, 2, 1)
        x, _ = self.rnn(x)
        x = self.fc(x)
        x = self.act(x)
        return x

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
        '''
        cer_delta: пока игнорируется
        '''

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
            if epochs is not None and epoch > epochs:
                break

            for bn, batch in enumerate(dataloader):
                output = self.predict(batch[0])
                target_t, target_len = str_to_tensor(batch[1])
                loss = loss_function(
                    output.permute(1, 0, 2), target_t, get_y_lengths(output), target_len
                )
                loss.backward()

                last_losses.append(loss.item())

                if bn % batches_per_step == 0:
                    optimizer.step()
                    optimizer.zero_grad()

            if (
                len(last_losses) == plateu_length
                and abs(last_losses[-1] - sum(last_losses) / len(last_losses)) < loss_delta
            ):
                break
