import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';
import { Button, Box } from '@mui/material';
import axios from 'axios';

const videoConstraints = {
    height: 480,
    facingMode: "user"
};

const CameraFeed = ({ setActivations, setPrediction, modelType, setCurrentImg }) => {
    const webcamRef = useRef(null);

    const capture = React.useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        setCurrentImg(imageSrc);
        fetchActivationsAndPrediction(imageSrc);
    }, [webcamRef, setActivations, setPrediction, modelType]);

    const [isCapturing, setIsCapturing] = useState(false);
    let intervalId = useRef(null);

    const repeatedCapture = () => {
        if (isCapturing) {
            clearInterval(intervalId.current);
            setIsCapturing(false);
        } else {
            intervalId.current = setInterval(capture, 100);
            setIsCapturing(true);
        }
    }

    const fetchActivationsAndPrediction = async (imageSrc) => {
        const blob = await fetch(imageSrc).then(res => res.blob());
        const formData = new FormData();
        formData.append('image', blob);
        formData.append('model_type', modelType);

        try {
            const response = await axios.post('http://localhost:8005/extract', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            if (response.data) {
                setActivations(response.data.activations); // Assuming the response structure is known and correct
                const top_labels = response.data.top_labels;
                const top_probs = response.data.top_probs;
                const top_prob_indices = response.data.top_label_inidces;
                const predictions = top_labels.map((label, index) => [label, top_probs[index], top_prob_indices[index]]);
                setPrediction(predictions);  // Assuming 'prediction' is part of the same response
            }
        } catch (error) {
            console.error('Error fetching activations and prediction:', error);
        }
    };

    return (
        <Box display="flex" flexDirection="column" alignItems="center">
            <Webcam
                audio={false}
                height={200}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                style={{ borderRadius: '10px', objectFit: 'cover' }}
                videoConstraints={videoConstraints}
            />
            <Box display="flex" justifyContent="space-between" py={2}>
                <Button variant="contained" color="primary" onClick={capture}>
                    Foto
                </Button>
                {/* <Button variant="contained" color="secondary" onClick={repeatedCapture}>
                    {isCapturing ? 'Stoppe Video' : 'Starte Video'}
                </Button> */}
            </Box>
        </Box>
    );
};

export default CameraFeed;
