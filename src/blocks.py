import torch

class Residual(torch.nn.Module):
    def __init__(self, in_ch, out_ch, kernel, f_act):
        super().__init__()
        if kernel % 2:
            self.main = torch.nn.Conv2d(in_channels = in_ch, out_channels = out_ch, kernel_size = kernel, padding = (kernel - 1)//2)
            self.blank = torch.nn.Conv2d(in_channels = in_ch, out_channels = out_ch, kernel_size = 1) if in_ch != out_ch else torch.nn.Identity()
            self.activation = f_act
        else:
            raise RuntimeError('Kernel size must not be even')

    def forward(self, x):
        return self.activation(self.main(x) + self.blank(x))
