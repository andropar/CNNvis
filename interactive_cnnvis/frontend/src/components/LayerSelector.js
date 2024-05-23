import React from 'react';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';

const LayerSelector = ({ onLayerChange, activations }) => {
    const handleChange = (event) => {
        onLayerChange(event.target.value);
    };

    const layerDescriptions = Object.keys(activations);

    const layerOptions = layerDescriptions.map((layer, idx) => (
        <MenuItem key={idx} value={layer}>{layer}</MenuItem>
    ));
    console.log(layerDescriptions)

    return (
        <FormControl fullWidth>
            <InputLabel id="model-select-label">Layer</InputLabel>
            <Select
                labelId="layer-select-label"
                id="layer-select"
                defaultValue={[]}
                label="Layer"
                onChange={handleChange}
                multiple
            >
                {layerOptions}
            </Select>
        </FormControl>
    );
};

export default LayerSelector;