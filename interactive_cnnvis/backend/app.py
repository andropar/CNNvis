import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from extractor import AlexNetExtractor, pil_image_from_bytes
from PIL import Image
import base64
import os
from io import BytesIO
from grad_cam import grad_cam

def scale(array, min=0, max=1):
    return (array - array.min()) / (array.max() - array.min()) * (max - min) + min

script_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
CORS(app)

extractor = AlexNetExtractor()

@app.route('/')
def index():
    return "CNN Visualization Backend is running!"

@app.route('/load_model', methods=['POST'])
def load_model():
    global extractor
    data = request.json
    model_type = data['model_type'] 
    pretrained = model_type == 'imagenet'
    extractor = AlexNetExtractor(pretrained=pretrained)
    return jsonify({"message": f"Model loaded with {model_type} weights"})


@app.route('/extract', methods=['POST'])
def extract():
    image_bytes = request.files['image'].read()
    
    input_image = pil_image_from_bytes(image_bytes)
    
    activations, top_labels, top_probs, top_probs_indices = extractor.run_inference(input_image)
    
    for layer in activations:
        if len(activations[layer].shape) == 3:
            b64_encoded_activation_images = []
            for features in activations[layer]:
                img = Image.fromarray(scale(features, max=255).astype(np.uint8), 'L')
                buffer = BytesIO()
                img.save(buffer, format="JPEG")
                b64_activation_map = base64.b64encode(buffer.getvalue()).decode('utf-8')
                b64_encoded_activation_images.append(b64_activation_map)
            activations[layer] = b64_encoded_activation_images
        else:
            activations[layer] = activations[layer].tolist()
    
    return jsonify({
        "activations": activations,
        "top_labels": top_labels[:10],
        "top_probs": top_probs.tolist()[:10],
        "top_label_inidces": top_probs_indices.tolist()[:10]
    })

@app.route('/grad_cam', methods=['POST'])
def get_grad_cam_output():
    class_target_index = int(request.form['index'])
    model = extractor.model
    transform = extractor.transforms
    image_bytes = request.files['image'].read()
    input_image = pil_image_from_bytes(image_bytes)
    img = transform(input_image).unsqueeze(0)

    heatmap = grad_cam(model, img, class_target_index)

    heatmap_image = Image.fromarray(heatmap)

    # overlay heatmap on the input image
    input_image = input_image.convert("RGBA")
    heatmap_image = heatmap_image.convert("RGBA").resize(input_image.size)
    blended = Image.blend(input_image, heatmap_image, alpha=0.5)

    buffer = BytesIO()
    blended.save(buffer, format="PNG")
    b64_heatmap = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return jsonify({"heatmap": b64_heatmap})

@app.route('/details', methods=['POST'])
def get_details():
    data = request.json
    layer = data['layer']
    feature_index = data['index']

    try:
        mei_img = Image.open(os.path.join(script_dir, f'data/{layer}/{"feature_map" if "conv" in layer else "neuron"}_{feature_index}.jpg'))
        buffer = BytesIO()
        mei_img.save(buffer, format="JPEG")
        b64_mei = base64.b64encode(buffer.getvalue()).decode('utf-8')
    except:
        b64_mei = None

    try:
        filter_img = Image.open(os.path.join(script_dir, f'data/{layer}/filter_{feature_index}.jpg'))
        buffer = BytesIO()
        filter_img.save(buffer, format="JPEG")
        b64_filter = base64.b64encode(buffer.getvalue()).decode('utf-8')
    except:
        b64_filter = None

    data = {
        "mei": b64_mei,
        "filter": b64_filter
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8005)