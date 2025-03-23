class SymNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.network = torch.nn.Sequential(
            Residual(3, 7, 3, torch.nn.ReLU()),
            torch.nn.MaxPool2d(kernel_size=3),
            Residual(7, 64, 5, torch.nn.Tanh()),
            torch.nn.MaxPool2d(kernel_size=2),
            Inception(64, 32, 8, 8),
            torch.nn.MaxPool2d(kernel_size=2),
            Residual(80, 16, 5, torch.nn.ReLU()),
            torch.nn.MaxPool2d(kernel_size=3),
            torch.nn.Flatten(),
            torch.nn.Linear(in_features=64, out_features=96),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=96, out_features=64),
            torch.nn.Tanh(),
            torch.nn.Linear(in_features=64, out_features=41),
            torch.nn.Softmax(-1)
        )

    def forward(self, x):
        return self.network(x)

d = DataLoader('dataset100_100/train', 100)
device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
model = SymNet().to(dtype=torch.float32, device=device)
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=1e-2,
    momentum=0.9,
    nesterov=True,
)
loss_fn = torch.nn.NLLLoss()
