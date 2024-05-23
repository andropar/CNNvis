import torch
import torch.nn as nn

import numpy as np
from PIL import Image
import io
from torchvision.models.alexnet import AlexNet_Weights
from torchvision.models import alexnet
import requests


class AlexNetExtractor:
    def __init__(self, pretrained=True):
        weights = AlexNet_Weights.DEFAULT
        self.transforms = weights.transforms() 
        self.model = alexnet(weights=weights if pretrained else None)
        self.model.eval()  # Ensure the model is in evaluation mode

        self.cnn_feature_keys = [0, 3, 6, 8, 10]
        self.clf_feature_keys = [1, 4, 6]
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
        for key in self.cnn_feature_keys:
            self.model.features[key].register_forward_hook(
                self.get_activation(f"conv_{key}")
            )

        for key in self.clf_feature_keys:
            self.model.classifier[key].register_forward_hook(
                self.get_activation(f"fc_{key}")
            )
    
    def run_inference(self, frame):
        img = self.transforms(frame).unsqueeze(0)
        
        probs = self.model(img).cpu().detach().numpy().squeeze()
        top_prob_indices = np.argsort(probs)[::-1][:10]
        top_probs = probs[top_prob_indices]
        top_labels = [self.labels[i] for i in top_prob_indices]
        
        return self.activations.copy(), top_labels, top_probs, top_prob_indices

def pil_image_from_bytes(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    return image