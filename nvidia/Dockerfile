#Use NVIDIA's official CUDA image
FROM nvidia/cuda:12.6.2-cudnn-runtime-ubuntu22.04

# Install additional dependencies as needed
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install torch --index-url https://download.pytorch.org/whl/cu124

WORKDIR /src
COPY ./app /src/app

CMD ["fastapi", "run", "app/main.py"]
