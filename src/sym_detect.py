class SymNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.network = torch.nn.Sequential(
            Residual(1, 16, 3, torch.nn.ReLU()),  # 1 канал на входе
            # torch.nn.Dropout(0.4),
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1),  # 32x32 -> 16x16
            
            Residual(16, 24, 5, torch.nn.ReLU()), # out_channels = 18
            torch.nn.MaxPool2d(kernel_size=3, stride=2, padding=1),    # 16x16 -> 6x4
            
            torch.nn.Flatten(),
            torch.nn.Linear(in_features=1536, out_features=512),  # 28*3*2=168 -> 74
            torch.nn.ReLU(),
            torch.nn.Dropout(0.25),
            torch.nn.Linear(512, 256),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.2),
            torch.nn.Linear(256, 41),
            torch.nn.LogSoftmax(dim=1)
        )

    def forward(self, x):
        return self.network(x)
