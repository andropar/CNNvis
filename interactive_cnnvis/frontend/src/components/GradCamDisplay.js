import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';
import { Button, Box, Typography } from '@mui/material';
import axios from 'axios';

const CameraFeed = ({ currentImg, currentHeatMapDisplayImg, currentSelectedPrediction }) => {

    return (
        <Box>
            <Typography sx={{ mb: 2 }}>Für die Vorhersage von "{currentSelectedPrediction}"</Typography>
            <Box display="flex" flexDirection="column" alignItems="center">
                <img
                    src={currentHeatMapDisplayImg ? currentHeatMapDisplayImg : currentImg}
                    alt="Webcam capture"
                    style={{
                        width: '100%',
                        borderRadius: '10px',
                        objectFit: 'cover'
                    }}
                />
            </Box>
        </Box>
    );
};

export default CameraFeed;
