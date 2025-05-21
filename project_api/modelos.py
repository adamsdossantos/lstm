import torch.nn as nn
import torch
from pydantic import BaseModel



class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_stack_layers):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_stack_layers = num_stack_layers
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_stack_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        batch_size = x.size(0)
        h0 = torch.zeros(self.num_stack_layers, batch_size, self.hidden_size)
        c0 = torch.zeros(self.num_stack_layers, batch_size, self.hidden_size)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out


class PriceData(BaseModel):
    history: list[float]