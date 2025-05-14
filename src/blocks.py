from torch import nn


class Residual(nn.Module):
    def __init__(self, in_ch, out_ch, kernel, f_act):
        super().__init__()
        if kernel % 2:
            self.main = nn.Sequential(
                nn.Conv2d(in_channels=in_ch, out_channels=out_ch, kernel_size=kernel, padding=(kernel - 1) // 2),
                nn.BatchNorm2d(out_ch)
            )
            self.blank = nn.Sequential(
                nn.Conv2d(in_channels=in_ch, out_channels=out_ch, kernel_size=1)
                if in_ch != out_ch else nn.Identity(),
                nn.BatchNorm2d(out_ch)
            )
            self.activation = f_act
        else:
            raise RuntimeError('Kernel size must not be even')

    def forward(self, x):
        return self.activation(self.main(x) + self.blank(x))
