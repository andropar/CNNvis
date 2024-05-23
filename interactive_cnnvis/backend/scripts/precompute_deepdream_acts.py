import os

import numpy as np
import torch
from lucent.optvis import objectives, param, render, transform
from PIL import Image
from torch.nn import functional as F
from torchvision import models


def scale(array, min=0, max=1):
    return (array - array.min()) / (array.max() - array.min()) * (max - min) + min


class AlexNetFeatureVisualizer:
    def __init__(
        self, output_dir="/Users/jrothadmin/repos/CNNvis/interactive_cnnvis/backend/data"
    ):
        self.model = models.alexnet(pretrained=True).eval()
        self.output_dir = output_dir
        self.activations = {}
        self.fc_activations = {}
        self.hooks = []
        self.conv_layers = [0, 3, 6, 8, 10]
        self.fc_layers = [6]

        # Ensure the model is in eval mode
        self.model.eval()

        # Move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        # Register hooks
        self.register_hooks()

        # Run random image through model to get activations
        img = torch.randn(1, 3, 224, 224).to(self.device)
        with torch.no_grad():
            self.model(img)

    def register_hooks(self):
        for key in self.conv_layers:
            layer = self.model.features[key]
            hook = layer.register_forward_hook(self.save_activation(f"conv_{key}"))
            self.hooks.append(hook)

        for key in self.fc_layers:
            layer = self.model.classifier[key]
            hook = layer.register_forward_hook(self.save_fc_activation(f"fc_{key}"))
            self.hooks.append(hook)

    def save_activation(self, name):
        def hook(model, input, output):
            self.activations[name] = output.detach()

        return hook

    def save_fc_activation(self, name):
        def hook(model, input, output):
            self.fc_activations[name] = output.detach()

        return hook

    def generate_exciting_images(self):
        # for i, activation in enumerate(self.activations.values()):
        #     conv_layer = self.conv_layers[i]
        #     num_feature_maps = activation.shape[1]
        #     layer_path = os.path.join(self.output_dir, f"conv_{conv_layer}")
        #     os.makedirs(layer_path, exist_ok=True)

        #     for filter_idx in range(num_feature_maps):
        #         img_path = os.path.join(layer_path, f"feature_map_{filter_idx}.jpg")
        #         if os.path.exists(img_path):
        #             continue

        #         print(f"Generating for {conv_layer} feature map {filter_idx}")
        #         obj = objectives.channel(f"features_{conv_layer}", filter_idx)
        #         img_param = lambda: param.image(224, fft=True, decorrelate=True)
        #         img = render.render_vis(
        #             self.model,
        #             obj,
        #             param_f=img_param,
        #             transforms=transform.standard_transforms,
        #             show_image=False,
        #         )[-1][0]
        #         img = Image.fromarray((img * 255).astype(np.uint8))

        #         # Save the image
        #         img.save(img_path)

        #         # Save the filter
        #         filter = (
        #             self.model.features[conv_layer]
        #             .weight.data[filter_idx, 0]
        #             .cpu()
        #             .numpy()
        #         )
        #         img = Image.fromarray(scale(filter, max=255).astype(np.uint8), mode='L').resize(
        #             (224, 224), Image.NEAREST
        #         )
        #         filter_path = os.path.join(layer_path, f"filter_{filter_idx}.jpg")
        #         img.save(filter_path)

        for i, activation in enumerate(self.fc_activations.values()):
            fc_layer = self.fc_layers[i]
            num_neurons = activation.shape[1]
            layer_path = os.path.join(self.output_dir, f"fc_{fc_layer}")
            os.makedirs(layer_path, exist_ok=True)

            for neuron_idx in range(num_neurons):
                img_path = os.path.join(layer_path, f"neuron_{neuron_idx}.jpg")
                if os.path.exists(img_path):
                    continue

                print(f"Generating for {fc_layer} neuron {neuron_idx}")
                obj = objectives.channel(f"classifier_{fc_layer}", neuron_idx)
                img_param = lambda: param.image(224, fft=True, decorrelate=True)
                img = render.render_vis(
                    self.model,
                    obj,
                    param_f=img_param,
                    transforms=transform.standard_transforms,
                    show_image=False,
                )[-1][0]
                img = Image.fromarray((img * 255).astype(np.uint8))

                # Save the image
                img.save(img_path)

    def close_hooks(self):
        for hook in self.hooks:
            hook.remove()


if __name__ == "__main__":
    visualizer = AlexNetFeatureVisualizer()
    visualizer.generate_exciting_images()
    visualizer.close_hooks()
