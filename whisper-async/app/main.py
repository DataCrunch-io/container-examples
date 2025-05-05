import uvicorn
import io
import os
import numpy as np
import torch
import requests
from fastapi import FastAPI, HTTPException, BackgroundTasks, status
from starlette.responses import JSONResponse
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from pydub import AudioSegment
from typing import Dict


def create_app() -> FastAPI:
    fast_api = FastAPI()

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    fast_api.state.webhook = os.getenv('WEBHOOK', None)

    model_id = "openai/whisper-large-v3-turbo"
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)
    speech_pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device
    )

    @fast_api.get("/health")
    async def health_check() -> Dict:
        return {"status": "ok"}

    @fast_api.post("/generate")
    async def generate(body: Dict) -> Dict:
        url = await get_audio_url(body)
        response = await get_audio_file(url)
        return await execute_pipeline(response)

    @fast_api.post("/generate_webhook")
    async def generate_webhook(body: Dict, background_tasks: BackgroundTasks) -> JSONResponse:
        # Please set WEBHOOK environment variable if you want to use webhooks
        if fast_api.state.webhook is None:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"status": "error", "details": "webhook not defined"}
            )
        background_tasks.add_task(process_and_send, body)
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={"status": "accepted"}
        )

    async def process_and_send(body: Dict):
        try:
            url = await get_audio_url(body)
            response = await get_audio_file(url)
            result = await execute_pipeline(response)
            await send_to_webhook(fast_api.state.webhook, result)
        except Exception as e:
            print(f"[background task] error: {e}")

    async def send_to_webhook(webhook_url: str, payload: dict):
        try:
            requests.post(webhook_url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
        except Exception as e:
            print(f"Failed to send webhook: {e}")

    async def get_audio_url(body: Dict) -> str:
        url = body.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="Request JSON must include a top‑level `url` field")

        return url

    async def get_audio_file(url: str) -> requests.Response:
        resp = requests.get(url)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Could not fetch audio file (status {resp.status_code})")

        return resp

    async def execute_pipeline(response: requests.Response) -> Dict:
        audio = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
        samples /= (1 << (audio.sample_width * 8 - 1))

        if audio.channels > 1:
            samples = samples.reshape((-1, audio.channels)).mean(axis=1)

        sampling_rate = audio.frame_rate
        max_secs = 30
        step = max_secs * sampling_rate
        transcripts = []
        for start in range(0, len(samples), step):
            chunk = samples[start: start + step]
            out = speech_pipe(
                {"array": chunk, "sampling_rate": sampling_rate},
            )
            transcripts.append(out["text"])
        full_text = " ".join(transcripts)
        return {"result": full_text}

    return fast_api

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8989)