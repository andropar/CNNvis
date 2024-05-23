import React from 'react';
import { Typography, Grid, Button } from '@mui/material';

const Predictions = ({ predictions, handlePredictionClick }) => {
    return (
        <div>

            <Grid container spacing={2}>
                {predictions.map((prediction, index) => (
                    <Grid item xs={6} sm={3} key={index}>
                        <Button variant="outlined" onClick={() => handlePredictionClick(prediction)}>
                            {prediction[0]}: {(prediction[1] / 100).toFixed(3)}
                        </Button>
                    </Grid>
                ))}
            </Grid>
        </div>
    );
};

export default Predictions;