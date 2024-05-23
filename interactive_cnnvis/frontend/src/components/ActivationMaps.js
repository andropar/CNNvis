import React from 'react';
import LayerActivations from './LayerActivations';
import { Grid, Typography, Box } from '@mui/material';

const ActivationMaps = ({ activations, selectedLayers, onDetailClick }) => {

    const activation_grids = []
    for (const [layerDescription, images] of Object.entries(activations)) {
        if (selectedLayers.includes(layerDescription)) {
            activation_grids.push(
                <Grid item key={layerDescription} xs={12}>
                    <Typography variant="subtitle1">{layerDescription}</Typography>
                    <LayerActivations images={images} layerName={layerDescription} onDetailClick={onDetailClick} />
                </Grid>
            )
        }
    }

    return (
        <div>
            <Typography variant="h6">Activation Maps</Typography>
            <Box sx={{ overflowX: 'auto' }}>
                <Grid container spacing={1}>
                    {activation_grids}
                </Grid>
            </Box>
        </div>
    );
};

export default ActivationMaps;
