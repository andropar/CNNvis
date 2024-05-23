from gpt2_cnnvis.backend.extractor import load_alexnet, transform_image
import torch

def predict(model, input_image):
    model.eval()
    with torch.no_grad():
        outputs = model(input_image)
        _, predicted = torch.max(outputs, 1)
        return predicted.item()