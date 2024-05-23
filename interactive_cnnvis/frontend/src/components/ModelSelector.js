import React from 'react';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';

const ModelSelector = ({ onModelChange }) => {
    const handleChange = (event) => {
        onModelChange(event.target.value);
    };

    return (
        <FormControl fullWidth>
            <InputLabel id="model-select-label">Modeltyp</InputLabel>
            <Select
                labelId="model-select-label"
                id="model-select"
                defaultValue="imagenet"
                label="Model Type"
                onChange={handleChange}
            >
                <MenuItem value="random">Random Weights</MenuItem>
                <MenuItem value="imagenet">ImageNet Pre-trained</MenuItem>
            </Select>
        </FormControl>
    );
};

export default ModelSelector;