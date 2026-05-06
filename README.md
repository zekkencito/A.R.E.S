# A.R.E.S. (Audit Resource & Environment System)
### Mars Challenge 2026 - Elemento Tierra

A.R.E.S. is an advanced web-based resource auditing and environmental simulation system designed for the Mars Challenge 2026. Its primary purpose is to ensure the survival of Martian exploration crews by rigorously calculating the water resources required to safely wash toxic perchlorates from the Martian soil, which is critical for base construction, agriculture, and water filtration.

## Architecture

The system utilizes a robust client-server architecture:

- **Frontend (React + Three.js + TailwindCSS)**: Provides a highly immersive, real-time 3D simulation of the Martian terrain using a scanner drone. It dynamically visualizes the assigned land sectors and provides an interactive dashboard to adjust environmental telemetry (Temperature, Humidity, Pressure, and Area).
- **Backend (Python + FastAPI)**: Serves as the deterministic processing core. It calculates exact water requirements based on real-time telemetry and communicates with an external LLM (Groq) to generate tactical audio reports using Edge TTS.

## Features

- **Interactive 3D Visualization**: Control a scanner drone with WASD/QE controls to visually inspect the simulated Mars landscape.
- **Deterministic Resource Calculation**: Precise mathematical modeling to calculate evaporation, sublimation, and soil retention based on environmental variables.
- **Critical Alert System**: Evaluates current water reserves against required water. Triggers critical alerts if reserves are insufficient or excessive (preventing soil erosion and landslides).
- **AI-Powered Crew Link**: Includes a direct text-based communication interface with "DaLiA", the onboard AI, which retains context of the current telemetry and required resources to assist the crew dynamically.

## Installation and Setup

### Prerequisites
- Node.js v18+
- Python 3.10+

### Backend Setup
1. Open a terminal in the repository root.
2. Create and activate a Python virtual environment.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Define your `VITE_GROQ_API_KEY` environment variable on your system or server.
5. Run the FastAPI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Frontend Setup
1. Open a new terminal in the repository root.
2. Install the Node dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file in the root directory and specify the backend URL:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
4. Start the Vite development server:
   ```bash
   npm run dev
   ```

## License
Developed for the Mars Challenge 2026. All rights reserved.
