from torch import nn

class SymNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            Residual(1, 16, 3, nn.ReLU()),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            Residual(16, 24, 5, nn.ReLU()),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            nn.Flatten(),
            nn.Linear(in_features=1536, out_features=512),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 41),
            nn.LogSoftmax(dim=1)
        )

    def forward(self, x):
        return self.network(x)
