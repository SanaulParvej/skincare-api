from fastapi import FastAPI
from pydantic import BaseModel
from analyzer import analyze_product

app = FastAPI()


class ProductText(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "API Running Successfully"}


@app.post("/scan")
async def scan(data: ProductText):

    result = analyze_product(data.text)

    return result
