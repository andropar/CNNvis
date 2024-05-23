from torchvision.models import alexnet
from torchvision.models.alexnet import AlexNet_Weights

if __name__ == "__main__":
    weights = AlexNet_Weights.DEFAULT
    model = alexnet(weights=weights )
    