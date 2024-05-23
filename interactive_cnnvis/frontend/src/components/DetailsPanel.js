import React from 'react';
import { Typography, Paper, Box } from '@mui/material';
import axios from 'axios';
import { useEffect, useState } from 'react';


const DetailsPanel = ({ selectedMap }) => {

    const [detailFilter, setDetailFilter] = useState(null);
    const [detailMEI, setDetailMEI] = useState(null);

    const postData = {
        'layer': selectedMap.layerName,
        'index': selectedMap.imageIdx
    }

    const fetchDetails = async () => {
        try {
            const response = await axios.post('http://localhost:8005/details', postData);
            if (response.data) {
                // Assuming the response structure is known and correct
                setDetailFilter(`data:image/jpeg;base64,${response.data.filter}`);
                setDetailMEI(`data:image/jpeg;base64,${response.data.mei}`);
            }
        } catch (error) {
            console.error('Error fetching activations and prediction:', error);
        }
    }

    useEffect(() => {
        fetchDetails();
    }, [selectedMap]);

    return (
        <Box>
            <Typography>Gewähltes Feature: ({selectedMap.layerName}, Index: {selectedMap.imageIdx})</Typography>
            {/* Assuming selectedMap is an object with relevant details */}
            <Box>
                {!selectedMap.layerName.includes('fc') &&
                    <Box sx={{ paddingTop: '20px', ml: 2, mr: 2 }}>
                        <Typography variant="h6">Feature Map Details</Typography>
                        <Box component="img" src={`data:image/jpeg;base64,${selectedMap.image}`} alt="Feature Map Details" sx={{ width: '100%' }} />
                    </Box>
                }
                {detailFilter && selectedMap.layerName === 'conv_0' &&
                    <Box sx={{ paddingTop: '20px', ml: 2, mr: 2 }}>
                        <Typography variant="h6">Filter</Typography>
                        <Box component="img" src={detailFilter} alt="Filter" sx={{ width: '100%' }} />
                    </Box>
                }
                {detailMEI &&
                    <Box sx={{ paddingTop: '20px', ml: 2, mr: 2 }}>
                        <Typography variant="h6">MEI</Typography>
                        <Box component="img" src={detailMEI} alt="MEI" sx={{ width: '100%' }} />
                    </Box>
                }
            </Box>
        </Box>
    );
};

export default DetailsPanel;