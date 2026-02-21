# RehabSense Backend



Professional Python backend for the AI Physiotherapy Platform RehabSense.



## Overview



This backend provides REST API and WebSocket endpoints for real-time pose detection, exercise analysis, and session management. It integrates seamlessly with the Next.js frontend running on `http://localhost:3000`.



## Features



- **REST API** for session management (start, update metrics, end)

- **WebSocket** for real-time frame processing and feedback

- **MediaPipe Holistic** for pose detection

- **Joint angle calculation** for exercise analysis

- **Repetition counting** with form validation

- **Posture analysis** with scoring and misalignment detection



## Requirements



- Python 3.13+ (fully compatible)

- pip or conda package manager



## Installation



1. Navigate to the backend directory:

```bash

cd backend

```



2. Create a virtual environment (recommended):

```bash

python -m venv venv

```



3. Activate the virtual environment:

   - **Windows:**

     ```bash

     venv\Scripts\activate

     ```

   - **macOS/Linux:**

     ```bash

     source venv/bin/activate

     ```



4. Install dependencies:

```bash

pip install -r requirements.txt

```



## Running the Backend



### Option 1: Using Python directly

```bash

python main.py

```



### Option 2: Using uvicorn directly

```bash

uvicorn main:app --reload --host 0.0.0.0 --port 8000

```



The backend will start on `http://localhost:8000`



## API Endpoints



### REST Endpoints



- **GET /** - Root endpoint (API info)

- **GET /health** - Health check

- **POST /api/sessions/start** - Start a new session

- **POST /api/sessions/{sessionId}/metrics** - Update session metrics

- **POST /api/sessions/{sessionId}/end** - End session and get summary



### WebSocket Endpoint



- **WS /api/ws/{sessionId}** - Real-time frame processing



## API Documentation



Once the server is running, visit:

- **Swagger UI:** http://localhost:8000/docs

- **ReDoc:** http://localhost:8000/redoc



## Project Structure



```

backend/

├── main.py                 # FastAPI app entrypoint

├── routers/

│   ├── __init__.py

│   ├── session.py         # Session REST endpoints

│   └── websocket.py       # WebSocket endpoint

├── services/

│   ├── __init__.py

│   ├── pose_detector.py   # MediaPipe pose detection

│   ├── angle_calculator.py # Joint angle calculations

│   ├── rep_counter.py     # Repetition tracking

│   └── posture_analyzer.py # Posture analysis

├── models/

│   ├── __init__.py

│   └── session_models.py  # Pydantic models

├── utils/

│   ├── __init__.py

│   └── helpers.py         # Utility functions

├── requirements.txt        # Dependencies

└── README.md              # This file

```



## Integration with Frontend



The backend is configured to accept requests from the frontend at `http://localhost:3000` via CORS middleware.



### Frontend Integration Example



```typescript

// Start a session

const response = await fetch('http://localhost:8000/api/sessions/start', {

  method: 'POST',

  headers: { 'Content-Type': 'application/json' },

  body: JSON.stringify({ exercise: 'squat' })

});

const { sessionId } = await response.json();



// Connect WebSocket for real-time processing

const ws = new WebSocket(`ws://localhost:8000/api/ws/${sessionId}`);

ws.onmessage = (event) => {

  const data = JSON.parse(event.data);

  // Update frontend state with metrics

};

```



## Data Models



All endpoints use Pydantic models that match the frontend SessionContext structure:



- `totalReps`: Total repetitions

- `correctReps`: Correct repetitions

- `incorrectReps`: Incorrect repetitions

- `postureAccuracy`: Posture accuracy (0-100%)

- `misalignmentsCount`: Number of misalignments

- `incorrectFormAlerts`: Number of form alerts

- `sessionDuration`: Duration in seconds

- `averageJointDeviation`: Average joint deviation (degrees)

- `performanceRating`: 'excellent', 'good', or 'needs-improvement'



## Exercise Types



Supported exercises:

- `squat` - Squat exercise

- `arm-raise` - Arm raise exercise

- `shoulder` - Shoulder rotation exercise



## Development Notes



- The backend uses in-memory session storage. For production, implement a database.

- MediaPipe Holistic model is initialized on first use (singleton pattern).

- WebSocket connections handle frame processing in real-time.

- All angle calculations use 3D coordinates from MediaPipe landmarks.



## Troubleshooting



### Import Errors

If you encounter import errors, ensure you're running from the `backend` directory and all dependencies are installed.



### MediaPipe Issues

If MediaPipe fails to initialize, ensure you have the correct version installed:

```bash

pip install mediapipe==0.10.8

```



### Port Already in Use

If port 8000 is already in use, change it in `main.py` or use:

```bash

uvicorn main:app --port 8001

```



## License



Part of the RehabSense project.

