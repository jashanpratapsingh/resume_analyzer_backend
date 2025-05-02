from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.resume_analyzer.resume_analyzer import ResumeAnalyzer
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Get allowed origins from environment variable or use default
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,https://ai-resume-analyzer.vercel.app,https://ai-resume-analyzer-claude.onrender.com"
).split(",")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the resume analyzer
analyzer = ResumeAnalyzer()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}")
    
    if not file:
        logger.error("No file received")
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    if not file.filename:
        logger.error("No filename received")
        raise HTTPException(status_code=400, detail="No filename provided")
    
    if not file.filename.lower().endswith('.pdf'):
        logger.error(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        # Create a temporary directory if it doesn't exist
        temp_dir = os.getenv('TEMP_DIR', 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, f"temp_{file.filename}")
        
        # Save the uploaded file temporarily
        try:
            content = await file.read()
            with open(temp_path, "wb") as buffer:
                buffer.write(content)
            logger.info(f"File saved temporarily at: {temp_path}")
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

        try:
            # Analyze the resume
            logger.info("Starting resume analysis")
            analysis = analyzer.analyze_resume(temp_path)
            logger.info("Resume analysis completed successfully")
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing resume: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                logger.info(f"Temporary file removed: {temp_path}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 