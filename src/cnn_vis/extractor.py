from torchvision.models import alexnet, AlexNet_Weights
import numpy as np
import requests
from threading import Thread, Lock
import cv2


class AlexNetExtractor:
    def __init__(self):
        weights = AlexNet_Weights.DEFAULT
        self.transforms = weights.transforms()
        self.model = alexnet(weights=weights)
        self.model.eval()  # Ensure the model is in evaluation mode
        self.activations = {}

        self.labels = requests.get(
            "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
        ).json()

        self.register_hooks()

    def get_activation(self, name):
        def hook(model, input, output):
            self.activations[name] = output.detach().numpy().squeeze()

        return hook

    def register_hooks(self):
        cnn_feature_keys = [0, 3, 6, 8, 10]
        for key in cnn_feature_keys:
            self.model.features[key].register_forward_hook(
                self.get_activation(f"conv_{key}")
            )

        clf_feature_keys = [1, 4, 6]
        for key in clf_feature_keys:
            self.model.classifier[key].register_forward_hook(
                self.get_activation(f"fc_{key}")
            )
    
    def run_inference(self, frame):
        img = self.transforms(frame).unsqueeze(0)
        
        probs = self.model(img)
        top_probs = np.argsort(probs.detach().numpy().squeeze())[::-1][:20]
        top_labels = [self.labels[i] for i in top_probs]
        
        return self.activations.copy(), top_labels, top_probs



    