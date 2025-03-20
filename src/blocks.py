import torch

class Residual(torch.nn.Module):
    def __init__(self, in_ch, out_ch, kernel, f_act):
        super().__init__()
        if kernel % 2:
            self.main = torch.nn.Conv2d(in_channels = in_ch, out_channels = out_ch, kernel_size = kernel, padding = (kernel - 1)//2)
            self.blank = torch.nn.Conv2d(in_channels = in_ch, out_channels = out_ch, kernel_size = 1) if in_ch != out_ch else torch.nn.Identify()
            self.activation = f_act
        else:
            raise RuntimeError('Kernel size must not be even')

    def forward(self, x):
        return self.activation(self.main(x) + self.blank(x))

class Inception(torch.nn.Module):
    def __init__(self, in_ch, out_1, out_3, out_5):
        super().__init__()
        self.l1 = torch.nn.Conv2d(in_channels = in_ch, out_channels = out_1, kernel_size = 1)
        self.l3 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels = in_ch, out_channels = out_1, kernel_size = 1),
            torch.nn.Conv2d(in_channels = out_1, out_channels = out_3, kernel_size = 3, padding = 1)
        )
        self.l5 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels = in_ch, out_channels = out_1, kernel_size = 1),
            torch.nn.Conv2d(in_channels = out_1, out_channels = out_5, kernel_size = 5, padding = 2)
        )
        self.pool = torch.nn.Sequential(
            torch.nn.MaxPool2d(kernel_size = 3, stride = 1, padding = 1),
            torch.nn.Conv2d(in_channels = in_ch, out_channels = out_1, kernel_size = 1)
        )

    def forward(self, x):
        return torch.cat([self.l1(x), self.l3(x), self.l5(x), self.pool(x)], dim=1)
