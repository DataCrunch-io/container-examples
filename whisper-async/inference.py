import requests
import sys
import os
import signal

def do_test_request() -> None:
    token = os.environ['DATACRUNCH_BEARER_TOKEN']
    deployment_name = os.environ['DATACRUNCH_DEPLOYMENT']
    baseurl = "https://containers.datacrunch.io"
    inference_url = f"{baseurl}/{deployment_name}/generate"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "respond-async"
    }

    payload = {
        "url": "https://anchor.fm/s/f4eff228/podcast/play/93688065/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fstaging%2F2024-9-29%2F388903574-44100-2-ef9795c05ea1d.mp3"
    }

    response = requests.post(inference_url, headers=headers, json=payload)
    if response.status_code == 202:
        print(response.json())
    else:
        print(f"inference failed. status code: {response.status_code}")
        print(response.text, file=sys.stderr)


def graceful_shutdown(signum, frame) -> None:
    print(f"\nSignal {signum} received at line {frame.f_lineno} in {frame.f_code.co_filename}")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    do_test_request()