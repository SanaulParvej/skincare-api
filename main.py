from fastapi import FastAPI, UploadFile, File
from analyzer import analyze_product
import shutil
import os

app = FastAPI()

os.makedirs("uploads", exist_ok=True)


@app.get("/")
def home():
    return {"message": "API Running Successfully"}


@app.post("/scan")
async def scan(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_product(file_path)

    return result
