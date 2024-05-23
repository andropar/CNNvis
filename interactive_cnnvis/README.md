# CNN visualisation app

## Setup
This app uses a Flask (Python) backend to extract features on the fly and a React (Javascript) frontend to display the visualisation. Note that I only tested this on Chrome! :)

### Docker
1. Run `docker run -p 8005:8005 -p 3000:5000 -it johannesroth/cnnvis:latest`
2. Access the app in your browser at `localhost:3000` 

### Manual setup
#### Backend 
0. `cd` into the backend directory
1. Create a new `conda` environment with `conda create --name cnnvis python=3.7`
2. Activate the environment with `conda activate cnnvis`
3. Install the required packages with `pip install -r requirements.txt`
4. Start the backend server with `python app.py`

#### Frontend
0. `cd` into the frontend directory
1. Install `npm` (follow this guide: https://nodejs.org/en/download/package-manager)
2. Start the frontend server with `npm start`, this should open a new tab in your browser with the app running (otherwise, access localhost:3000)