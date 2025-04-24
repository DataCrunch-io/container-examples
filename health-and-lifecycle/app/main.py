import signal, uvicorn, logging, asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
sigterm_received = False

def sigterm_handler(sig, frame):
    global sigterm_received
    logger.info(f"Received signal {sig}, starting graceful shutdown")
    sigterm_received = True

@asynccontextmanager
async def lifespan(app):
    # Setup signal handlers during startup
    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)
    yield
    # Wait for existing requests to complete (max 30s)
    wait_seconds = 0
    while sigterm_received and wait_seconds < 30:
        logger.info(f"Waiting for requests to complete ({wait_seconds}s)")
        await asyncio.sleep(1)
        wait_seconds += 1

app = FastAPI(lifespan=lifespan)

# semaphore with 1 slot → acts like a Lock
max_concurrency = 1
busy_semaphore = asyncio.Semaphore(max_concurrency)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/predict")
async def predict():
    await busy_semaphore.acquire() # Acquire a slot
    try:
        await asyncio.sleep(15)  # Simulate long-running request
        return {"message": "Prediction completed"}
    finally:
        busy_semaphore.release()

@app.get("/health")
async def health_check():
    # Report unhealthy during shutdown to prevent new requests
    if sigterm_received:
        return JSONResponse(status_code=503, content={"status": "shutting_down"})
    # _value is how many slots remain
    if busy_semaphore._value == 0:
        return JSONResponse(status_code=200, content={"status": "busy"})
    return JSONResponse(status_code=200, content={"status": "healthy"})

if __name__ == "__main__":
    print("Starting the server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, timeout_graceful_shutdown=30)