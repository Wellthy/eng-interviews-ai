from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import csv
import os
from datetime import datetime
from ai.model import classify_urgency

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Custom CSV handler
class CSVHandler(logging.Handler):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.file = None
        self.writer = None
        self._init_file()
    
    def _init_file(self):
        """Initialize or recover the CSV file."""
        file_exists = os.path.exists(self.filename)
        self.file = open(self.filename, 'a', newline='')
        self.writer = csv.writer(self.file)
        if not file_exists:
            self.writer.writerow(['timestamp', 'logger', 'level', 'message'])
            self.file.flush()
    
    def emit(self, record):
        try:
            timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
            logger_name = record.name
            level = record.levelname
            message = self.format(record)
            self.writer.writerow([timestamp, logger_name, level, message])
            self.file.flush()
        except Exception:
            self.handleError(record)
    
    def close(self):
        if self.file:
            self.file.close()
        super().close()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# CSV file handler
csv_handler = CSVHandler("data/logs.csv")
csv_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '%(message)s'  # Just the message for CSV, timestamp is handled separately
)
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))
csv_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(csv_handler)

app = FastAPI(title="Urgent Message Flagger", version="1.0.0")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

@app.post("/classify")
async def classify_message(message: Message):
    """
    Classify a message for urgency.
    
    Returns:
        dict: {
            "urgent": bool,
            "confidence_score": float,
            "model_version": str,
            "reasoning": str
        }
    """
    try:
        logger.info(f"Processing message: {message.text[:50]}...")
        result = classify_urgency(message.text)
        logger.info(f"Classification result: urgent={result['urgent']}, confidence={result['confidence_score']}")
        return result
    except Exception as e:
        logger.error(f"Error classifying message: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/logs")
async def view_logs(lines: int = 50):
    """
    Retrieve recent log entries from the CSV log file.
    
    Args:
        lines (int): Number of recent lines to return (default: 50)
    
    Returns:
        dict: Recent log entries as list of dicts
    """
    try:
        with open("data/logs.csv", "r") as f:
            reader = csv.DictReader(f)
            all_rows = list(reader)
            recent_rows = all_rows[-lines:] if len(all_rows) > lines else all_rows
        logger.info(f"Retrieved {len(recent_rows)} log entries")
        return {
            "total_entries": len(all_rows),
            "returned_entries": len(recent_rows),
            "logs": recent_rows
        }
    except FileNotFoundError:
        logger.warning("Log file not found")
        return {"error": "Log file not yet created", "logs": []}