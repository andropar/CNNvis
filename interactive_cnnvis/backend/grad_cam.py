from PIL import Image
from flask import app, request, send_file
import torch
import torch.nn.functional as F
import numpy as np
import cv2

def find_gradient_heatmap_(img, regression_predictor, latent_dim=1):
    """Extracts the gradients set by a hook in the regression predicto"""
    dim_original = regression_predictor(img, transform=True)[1]
    dim_original = dim_original[latent_dim]
    # Attach grad to leaf node
    img.requires_grad = True

    # Do a forward pass whilte preserving the graph
    with torch.enable_grad():
        dim_predict = regression_predictor(img, transform=True)[1]
        latent = dim_predict[latent_dim]
        latent.backward()
        gradients = regression_predictor.get_activations_gradient()

    # Pool  the gradients across the channels
    pooled_gradients = torch.mean(gradients, dim=[0, 2, 3])

    # Get the activations of the last convolutional layer
    activations = regression_predictor.get_activations(img)[0].detach()

    # Idea: the sensitivity of activations to a target class can be
    # understood as the importance of the activation map to the class
    # (given by the gradient), hence we weight the activation maps
    # with the gradients
    for i in range(512):
        activations[:, i, :, :] *= pooled_gradients[i]

    heatmap = torch.mean(activations, dim=1).squeeze()
    heatmap = F.relu(heatmap)
    heatmap /= torch.max(heatmap)
    heatmap = heatmap.cpu().numpy()
    return heatmap

def grad_cam(model, input_image, target_idx):
    model.eval()
    
    gradients = []
    activations = []
    
    def backward_hook(module, grad_input, grad_output):
        gradients.append(grad_output[0])
    
    def forward_hook(module, input, output):
        activations.append(output)

    target_layer = model.features[-1]
    target_layer.register_forward_hook(forward_hook)
    target_layer.register_backward_hook(backward_hook)
    
    output = model(input_image)
    model.zero_grad()

    target = output[0][target_idx]
    
    target.backward()
    
    gradient = gradients[0]
    activation = activations[0]
    pooled_gradients = torch.mean(gradient, dim=[0, 2, 3])
    
    for i in range(activation.shape[1]):
        activation[:, i, :, :] *= pooled_gradients[i]
    
    heatmap = torch.mean(activation, dim=1).squeeze().cpu().detach().numpy()
    heatmap = np.maximum(heatmap, 0)
    
    heatmap /= np.max(heatmap)
    
    heatmap = cv2.resize(heatmap, (input_image.shape[3], input_image.shape[2]), cv2.INTER_NEAREST)
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    return heatmap

# @app.route('/grad_cam', methods=['POST'])
# def compute_grad_cam():
#     data = request.json
#     model_type = data['model_type']
#     image_bytes = request.files['image'].read()
    
#     model = load_alexnet(model_type)
#     input_image = transform_image(image_bytes)
    
#     target_layer = model.features[11]  # Example layer
#     heatmap = grad_cam(model, input_image, target_layer)
    
#     heatmap_image = Image.fromarray(heatmap)
#     heatmap_image.save('heatmap.jpg')
    
#     return send_file('heatmap.jpg', mimetype='image/jpeg')