from unicodedata import bidirectional
import torch

from torch.nn import Module
from torch import nn

class TSPrediction(Module):

    def __init__(self, out_size) -> None:
        super().__init__()

        self.out_size = out_size

        self.initial_embedding = nn.Sequential(
            nn.Conv1d(in_channels= out_size, out_channels=1024, kernel_size=3, padding="same"),
            nn.BatchNorm1d(1024),
            nn.Conv1d(in_channels= 1024, out_channels=512, kernel_size=3, padding="same"),
            nn.BatchNorm1d(512),
            nn.Conv1d(in_channels= 512, out_channels=256, kernel_size=3, padding="same"),
            nn.BatchNorm1d(256),
        )

        self.lstm = nn.LSTM(input_size = 256, hidden_size = 256, bidirectional=True)

        self.decoder = nn.Sequential(
            nn.Linear(in_features= 512, out_features=512),
            nn.ReLU(),
            nn.Linear(in_features= 512, out_features=1024),
            nn.ReLU(),
            nn.Linear(in_features= 1024, out_features=self.out_size),
        )
    

    def forward(self, input):
        x = torch.transpose(input, 1,2)
        x = self.initial_embedding(x)

        x, _ = self.lstm(torch.transpose(x,1,2))
        x = torch.transpose(x,1,2)

        x = torch.flatten(nn.AdaptiveAvgPool1d(1)(x), start_dim=1)
        
        x = self.decoder(x)

        return x






