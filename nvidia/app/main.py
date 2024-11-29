from fastapi import FastAPI
import torch

app = FastAPI()


@app.get("/")
async def root():
    device = 'cpu'
    if torch.cuda.is_available():
        device = 'gpu'
    
    return {"message": f"Hello world, I can run on {device}"}
