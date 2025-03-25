class SymNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.network = torch.nn.Sequential(
            Residual(3, 16, 3, torch.nn.ReLU()),
            torch.nn.MaxPool2d(kernel_size=3),
            Inception(16, 32, 8, 8),
            torch.nn.Dropout(0.6),
            torch.nn.MaxPool2d(kernel_size=3),
            Residual(80, 8, 5, torch.nn.ReLU()),
            torch.nn.MaxPool2d(kernel_size=3),
            torch.nn.Flatten(),
            torch.nn.Linear(in_features=72, out_features=64),
            torch.nn.Dropout(0.7),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=64, out_features=56),
            torch.nn.Dropout(0.5),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=56, out_features=41),
            torch.nn.LogSoftmax(dim=1)
        )

    def forward(self, x):
        return self.network(x)

d = DataLoader('dataset100_100/train', 50)
d2 = DataLoader('dataset100_100/val', 50)           
device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
model = SymNet().to(dtype=torch.float32, device=device)
optimizer = torch.optim.Adam(params=model.parameters())
loss_fn = torch.nn.NLLLoss()
i = 0
losses = []
losses2 = []
for imgs, trgs in d:
    optimizer.zero_grad()
    pred = model(imgs.to(device))
    loss = loss_fn(pred, trgs.to(device))
    losses.append(loss.item())
    loss.backward()
    optimizer.step()
    i += 1
    if i % 5 == 0:
        with torch.no_grad():
            for imgs2, trgs2 in d2:
                pred2 = model(imgs2.to(device))
                loss2 = loss_fn(pred, trgs2.to(device))
                losses2.append(loss2.item())
                break
        clear_output(True)
        fig, ax = plt.subplots(figsize=(30, 10))
        plt.title("График ошибки")
        plt.plot(losses, ".-", label="Ошибка на обучении")
        plt.plot(torch.arange(0, i, 5), losses2, ".-", label="Ошибка на валидации")
        plt.xlabel("Итерация обучения")
        plt.ylabel("Значение ошибки")
        plt.legend()
        plt.grid()
        plt.show()
