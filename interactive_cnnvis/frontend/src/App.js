import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import CameraFeed from './components/CameraFeed';
import GradCamDisplay from './components/GradCamDisplay';
import ModelSelector from './components/ModelSelector';
import ActivationMaps from './components/ActivationMaps';
import LayerSelector from './components/LayerSelector';
import Predictions from './components/Predictions';
import DetailsPanel from './components/DetailsPanel';
import { AppBar, Toolbar, Box, Divider, Container, Grid, Typography, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

function App() {
  const [modelType, setModelType] = useState('imagenet');
  const [activations, setActivations] = useState({});
  const [selectedMap, setSelectedMap] = useState(null);
  const [prediction, setPrediction] = useState([]);
  const [selectedLayers, setSelectedLayers] = useState([]);
  const [currentImg, setCurrentImg] = useState(null);
  const [currentHeatMapDisplayImg, setCurrentHeatMapDisplayImg] = useState(null);
  const [currentSelectedPrediction, setCurrentSelectedPrediction] = useState(null);
  const [gradCamDisplayExpanded, setGradCamDisplayExpanded] = useState(false);
  const [detailsPanelExpanded, setDetailsPanelExpanded] = useState(false);
  const [predictionsExpanded, setPredictionsExpanded] = useState(false);

  useEffect(() => {
    if (currentImg) {
      setPredictionsExpanded(true);
    } else {

      setPredictionsExpanded(false);
    }
  }, [currentImg]);

  useEffect(() => {
    if (currentHeatMapDisplayImg) {
      setGradCamDisplayExpanded(true);
    } else {
      setGradCamDisplayExpanded(false);
    }
  }, [currentHeatMapDisplayImg]);

  useEffect(() => {
    if (selectedMap) {
      setDetailsPanelExpanded(true);
    } else {
      setDetailsPanelExpanded(false);
    }
  }, [selectedMap]);

  const handleModelChange = (type) => {
    setModelType(type);
    const requestModelChange = async () => {
      const response = await axios.post('http://localhost:8005/load_model', { 'model_type': type });
      if (response.data) {
        console.log(response.data);
      }
    }
    requestModelChange();
  };

  const handleSelectedLayers = (layers) => {
    setSelectedLayers(layers);
  }

  const handleActivations = (acts) => {
    setActivations(acts);
  };

  const handleSelectMap = (layerName, imageIdx) => {
    setSelectedMap({
      layerName: layerName,
      imageIdx: imageIdx,
      image: activations[layerName][imageIdx]
    });
  };

  const handlePrediction = (pred) => {
    setPrediction(pred);
  };

  const handlePredictionClick = (prediction) => {
    const requestGradCamOutput = async () => {
      const formData = new FormData();
      console.log(prediction)
      formData.append('index', prediction[2]);

      // Assuming currentImg is a File or Blob object
      const imageBlob = await fetch(currentImg).then(res => res.blob());
      formData.append('image', imageBlob);

      const response = await axios.post('http://localhost:8005/grad_cam', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if (response.data) {
        setCurrentHeatMapDisplayImg(`data:image/jpeg;base64,${response.data.heatmap}`);
        setCurrentSelectedPrediction(prediction[0]);
      }
    }
    requestGradCamOutput();
  }

  const handleCurrentImg = (img) => {
    setCurrentImg(img);
    setCurrentHeatMapDisplayImg(null);
  }

  return (
    <Container maxWidth={false}>
      <AppBar position="static" color="transparent" elevation={0} style={{ marginBottom: '0.5rem', marginTop: '0.5rem', borderRadius: '20px' }}>
        <Toolbar>
          <Typography variant="h6" gutterBottom>
            Wie Maschinen sehen - ein Blick in das Innenleben von CNNs
          </Typography>
          <img src='https://www.cbs.mpg.de/assets/institutes/headers/cbs-desktop-de-59a3e3087d4a45500e94aa0c600fae5b905f92faf3e004d0a94f3ed9dcd154e7.svg' alt='Max Planck Institute for Human Cognitive and Brain Sciences' style={{ width: '20%', marginLeft: 'auto' }} />
          <img src='https://www.uni-giessen.de/++theme++jlu-giessen-plone-6-theme/++theme++jlu-giessen-plone-6-theme/images/logo.png' alt='Justus Liebig University Giessen' style={{ width: '6%' }} />
        </Toolbar>
      </AppBar>
      <Divider style={{ marginBottom: '1.5rem' }} />
      <Grid container spacing={2}>
        <Grid item xs={12} md={3} xl={3}>
          <CameraFeed setActivations={handleActivations} setPrediction={handlePrediction} modelType={modelType} setCurrentImg={handleCurrentImg} />
          <Accordion sx={{ mb: 2 }} expanded={gradCamDisplayExpanded} onChange={() => setGradCamDisplayExpanded(!gradCamDisplayExpanded)} style={{ borderRadius: '10px', marginTop: 0 }}

          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1a-content"
              id="panel1a-header"
            >
              <Typography fontWeight={'bold'}>Wichtige Bildbereiche</Typography>
            </AccordionSummary>
            <AccordionDetails style={{ margin: 0 }}>
              {currentImg &&
                <GradCamDisplay currentImg={currentImg} currentHeatMapDisplayImg={currentHeatMapDisplayImg} currentSelectedPrediction={currentSelectedPrediction} />}
            </AccordionDetails>
          </Accordion>
          <Accordion sx={{ mb: 2 }} expanded={detailsPanelExpanded} onChange={() => setDetailsPanelExpanded(!detailsPanelExpanded)} style={{ borderRadius: '10px' }}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel2a-content"
              id="panel2a-header"
            >
              <Typography fontWeight={'bold'}>Details zu gewählten Features</Typography>
            </AccordionSummary>
            <AccordionDetails style={{ margin: 0 }}>
              {selectedMap &&
                <DetailsPanel selectedMap={selectedMap} />}
            </AccordionDetails>
          </Accordion>
        </Grid>

        <Grid item xs={12} md={9} xl={9}>
          <ModelSelector onModelChange={handleModelChange} />
          <Box py={2}>
            <LayerSelector onLayerChange={handleSelectedLayers} activations={activations} selectedLayers={selectedLayers} />
          </Box>
          <Accordion sx={{ mb: 2 }} expanded={predictionsExpanded} onChange={() => setPredictionsExpanded(!predictionsExpanded)} style={{ borderRadius: '10px', marginTop: 0 }}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel3a-content"
              id="panel3a-header"
            >
              <Typography fontWeight={'bold'}>Vorhersagen</Typography>
            </AccordionSummary>
            <AccordionDetails style={{ margin: 0 }}>
              {prediction &&
                <Predictions predictions={prediction} handlePredictionClick={handlePredictionClick} />}
            </AccordionDetails>
          </Accordion>
          <ActivationMaps activations={activations} onDetailClick={handleSelectMap} selectedLayers={selectedLayers} />
        </Grid>
      </Grid>
    </Container>
  );
}

export default App;