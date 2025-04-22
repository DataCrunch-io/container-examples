Whisper Container

Here is an example of fully operational Whisper-large-v3-turbo endpoint containerized for use with DataCrunch containers.

This container implements two endpoints:

* `/generate` - a standard Whisper speech-to-text endpoint
* `/health` - health-check on the container used by DataCrunch Containers to make sure the container us running and healthy.

Build:

```bash
docker build -t $YOUR_REGISTRY/whisper:v1 .
```

Push to a Docker registry:
```bash
docker push $YOUR_REGISTRY/whisper:v1
```

When the container starts, it will fetch the model weights from Hugging Face. Therefore, to run the container you will need to supply your [Hugging Face User access token](https://huggingface.co/docs/hub/en/security-tokens) as an environment variable `HF_TOKEN`. This can be easily done via DataCrunch Containers UI.

Once the container has been deployed on DataCrunch, and the endpoint is runnning, you can testing by running the following, which will send the `audio.wav` file to the endpoint for transcription:

```bash
export DATACRUNCH_CONTAINER_URL=https://containers.datacrunch.io/<NAME_OF_YOUR_DEPLOYMENT>
export DATACRUNCH_BEARER_TOKEN=dc_<YOUR_BEARER_TOKEN>

./inference.sh
```

If your setup is correct, you should see the following output:
```json
{"result":" Joe Keaton disapproved of films and Buster also had reservations about the medium."}
```