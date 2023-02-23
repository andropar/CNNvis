from torchvision.models import alexnet, AlexNet_Weights
from PIL import Image
import cv2
import numpy as np
import requests


def scale(array, min=0, max=1):
    return (array - array.min()) / (array.max() - array.min()) * (max - min) + min


if __name__ == "__main__":
    weights = AlexNet_Weights.DEFAULT
    transforms = weights.transforms()

    model = alexnet(weights=weights)

    activation = {}

    def get_activation(name):
        def hook(model, input, output):
            activation[name] = output.detach().numpy().squeeze()

        return hook

    cnn_feature_keys = [0, 3, 6, 8, 10]
    for key in cnn_feature_keys:
        model.features[key].register_forward_hook(get_activation(f"conv_{key}"))

    clf_feature_keys = [1, 4, 6]
    for key in clf_feature_keys:
        model.classifier[key].register_forward_hook(get_activation(f"fc_{key}"))

    n_cols = 9
    spacing_px = 20

    labels = requests.get(
        "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    ).json()

    cv2.namedWindow("CNNvis")
    vc = cv2.VideoCapture(0)

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        rval, frame = vc.read()

        img = transforms(Image.fromarray(frame)).unsqueeze(0)
        probs = model(img)

        fmap_imgs = []
        for i, key in enumerate(activation.keys()):
            fmaps = scale(activation[key])
            fmaps = fmaps**0.5

            n_fmaps = fmaps.shape[0]
            fmap_size = fmaps.shape[1] if len(fmaps.shape) == 3 else 1
            n_rows = n_fmaps // n_cols + 1

            stitched_activations = np.zeros((fmap_size * n_rows, fmap_size * n_cols))

            for i, fmap in enumerate(fmaps):
                r = i // n_cols
                c = i % n_cols
                stitched_activations[
                    r * fmap_size : (r + 1) * fmap_size,
                    c * fmap_size : (c + 1) * fmap_size,
                ] = fmap

            fmap_imgs.append(stitched_activations)

        max_fmap_height = (
            max([fmap_img.shape[0] for fmap_img in fmap_imgs]) + frame.shape[0] // 20
        )
        total_fmap_width = (
            sum([fmap_img.shape[1] for fmap_img in fmap_imgs])
            + len(fmap_imgs) * spacing_px
            + 200
        )

        stitched_fmaps = np.zeros((max_fmap_height, total_fmap_width))
        c = 0
        for fmap_img in fmap_imgs:
            # leave spacing_px between each fmap
            stitched_fmaps[: fmap_img.shape[0], c : c + fmap_img.shape[1]] = fmap_img
            c += fmap_img.shape[1] + spacing_px

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # resize to same ratio, but 10 times smaller
        frame = cv2.resize(frame, (0, 0), fx=0.2, fy=0.2)

        frame_height, frame_width = frame.shape
        # put frame to lower left corner of stitched fmaps
        stitched_fmaps[-frame_height:, :frame_width] = scale(frame)

        # put predicted labels and probabilities to the right of the stitched fmaps
        if vc.get(1) % 1000 == 0:
            probs = probs.detach().numpy().squeeze()
            top_probs = probs.argsort()[-20:][::-1]
            for i, prob in enumerate(top_probs):
                cv2.putText(
                    stitched_fmaps,
                    f"{labels[prob]} ({probs[prob]:.3f})",
                    (total_fmap_width - 200, 20 + i * 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                )

        cv2.imshow("preview", stitched_fmaps)

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    vc.release()
    cv2.destroyWindow("preview")
