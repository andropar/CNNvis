import numpy as np
from gpt2_cnnvis.backend.extractor import load_alexnet, transform_image
import torch
import torch.nn as nn


def scale(array, min=0, max=1):
    return (array - array.min()) / (array.max() - array.min()) * (max - min) + min

def stitch_feat_maps_to_rect(feat_maps, gap=10, gap_color=10):
    n_fmaps = feat_maps.shape[0]
    n_cols = 12
    n_rows = n_fmaps // n_cols + (1 if n_fmaps % n_cols != 0 else 0)
    fmap_size = feat_maps.shape[1]
    # Adjust the size of the stitched_fmaps to accommodate the gaps
    stitched_fmaps = (
        np.zeros(
            (
                fmap_size * n_rows + gap * (n_rows - 1),
                fmap_size * n_cols + gap * (n_cols - 1),
            )
        )
        + gap_color
    )

    for i, fmap in enumerate(feat_maps):
        r = i // n_cols
        c = i % n_cols
        row_start = r * (fmap_size + gap)
        col_start = c * (fmap_size + gap)
        stitched_fmaps[
            row_start : row_start + fmap_size, col_start : col_start + fmap_size
        ] = scale(fmap, max=255)

    return stitched_fmaps

def get_activations(model, input_image):
    activations = []
    
    x = input_image
    for layer in model.features:
        x = layer(x)
        if isinstance(layer, nn.Conv2d):
            activations.append(x)
    
    x = x.view(x.size(0), -1)  # Flatten for the classifier part
    
    for layer in model.classifier:
        x = layer(x)
        if isinstance(layer, nn.Linear):
            activations.append(x)
    
    return activations

def activations_to_list(activations):
    # Convert activations to a list of lists for JSON serialization
    
    return [[a.detach().numpy().tolist() for a in act] for act in activations]