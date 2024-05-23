import { Grid, useTheme, useMediaQuery } from "@mui/material";
import { useState } from "react";
import { interpolateRgb } from 'd3-interpolate';
import { scaleLinear } from 'd3-scale';

const LayerActivations = ({ images, layerName, onDetailClick }) => {
    const theme = useTheme();

    const [selectedImageIdx, setSelectedImageIdx] = useState(null);

    const handleClick = (imageIdx) => {
        setSelectedImageIdx(imageIdx);
        onDetailClick(layerName, imageIdx);
    };

    if (layerName.includes('conv')) {
        return (
            <Grid container spacing={1}>
                {images.map((image, imageIdx) => (
                    <Grid item key={imageIdx} xs={12} sm={6} md={4} lg={1} xl={1} onClick={() => handleClick(imageIdx)} >
                        <img src={`data:image/jpeg;base64,${image}`} alt={`Image ${imageIdx + 1}`} style={{ width: '100%', border: imageIdx === selectedImageIdx ? '2px solid red' : '2px solid white' }} />
                    </Grid>
                ))}
            </Grid>
        );
    } else {
        // will be fully connected layer output (list of numbers), join these together into a string
        // Assuming images is an array of numbers
        const data = images.map((value, index) => ({ name: index, value }));

        // Find the maximum value in the data array
        const maxValue = Math.max(...data.map(item => item.value));
        const minValue = Math.min(...data.map(item => item.value));

        // Function to convert a value to a color
        const valueToColor = (value) => {
            const colorScale = scaleLinear()
                .domain([minValue, maxValue])
                .range(['#00008b', '#add8e6'])
                .interpolate(interpolateRgb);

            return colorScale(value);
        }

        return (
            <div>
                <div style={{ display: 'flex', flexDirection: 'row' }}>
                    <div>
                        <div style={{ width: '20px', height: '20px', backgroundColor: '#00008b' }}></div>
                    </div>
                    <div style={{ marginLeft: 5, marginRight: 5 }}>to </div>
                    <div>
                        <div style={{ width: '20px', height: '20px', backgroundColor: '#add8e6' }}></div>
                    </div>
                </div>
                <div style={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap', marginTop: 5 }}>
                    {data.map((item, index) => (
                        <div
                            key={index}
                            style={{
                                width: '20px',
                                height: '20px',
                                backgroundColor: valueToColor(item.value),
                                margin: '2px',
                                cursor: 'pointer'
                            }}
                            onClick={() => onDetailClick(layerName, index)}
                        />
                    ))}
                </div>
            </div >
        );
    }
};

export default LayerActivations;