import os
import uvicorn
from fastapi import FastAPI, UploadFile, File
from app.application.use_case.log_processing_pipeline import LogProcessingPipeline
from pathlib import Path
import uuid

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

@app.post('/log/parsing')
async def log_parsing(file: UploadFile = File(...)):
    file_id = uuid.uuid4()
    file_name = f'{file_id}.{file.filename}'
    total_size: int = 0
    file_path = Path(BASE_DIR / file_name)

    with open(file_path.resolve(), 'wb') as f:
        while chunk:= await file.read(1024*1024):
            f.write(chunk)
            total_size += len(chunk)
    
    log_processing_pipeline = LogProcessingPipeline(
        file_path.resolve(),
        os.cpu_count(),
        os.cpu_count(),
    )
    parsed_data = log_processing_pipeline.run()
    return parsed_data

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)