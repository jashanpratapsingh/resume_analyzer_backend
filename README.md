# Resume Analyzer Backend

FastAPI backend for the Resume Analyzer application.

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with:
```
ANTHROPIC_API_KEY=your_api_key
ALLOWED_ORIGINS=http://localhost:5173,https://your-frontend-url.vercel.app
```

## Development

Run the development server:
```bash
uvicorn src.main:app --reload
```

## Deployment

1. Push to GitHub
2. Deploy to Render:
   - Create a new Web Service
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables from `.env`

## API Endpoints

- POST `/analyze`: Upload and analyze a resume PDF
  - Accepts: multipart/form-data with 'file' field
  - Returns: JSON with analysis results 