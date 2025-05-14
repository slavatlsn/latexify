from torch import nn
import torchvision.transforms as t
import cv2

transform = t.Compose([
    t.ToPILImage(),
    t.Resize((32, 32)),
    t.Grayscale(num_output_channels=1),
    t.ToTensor()
])

label_map = [
    "(", ")", "a", "+", "b", "c", "d", "/", "e", "8", "=", "f", "5", "4",
    "g", "h", "i", "j", "k", "l", "m", "n", "9", "o", "1", "p", "q", "r",
    "s", "7", "6", "-", "t", "3", "2", "u", "v", "w", "x", "y", "z", "0",
    "*", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    r"\times", r"\div"
]


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


classifier = SymNet()
classifier.load_state_dict(load("SymNet.pth", map_location=device(device)))
classifier.eval()

def symbol(img_path):
    gray_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    input_tensor = transform(gray_img).unsqueeze(0)
    output = classifier(input_tensor)
    class_id = argmax(output).item()
    return label_map[class_id]
