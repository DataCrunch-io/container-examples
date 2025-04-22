import uvicorn
import torch
from fastapi import FastAPI, UploadFile
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import soundfile as sf
import io

def create_app() -> FastAPI:
    fast_api = FastAPI()

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

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
        device=device,
    )

    @fast_api.get("/health")
    async def health_check():
        return {"status": "ok"}

    @fast_api.post("/generate")
    async def upload_audio(file: UploadFile):
        audio_bytes = await file.read()
        data, sampling_rate = sf.read(io.BytesIO(audio_bytes))
        result = speech_pipe({"array": data, "sampling_rate": sampling_rate})
        return {"result": result["text"]}

    return fast_api

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8989)