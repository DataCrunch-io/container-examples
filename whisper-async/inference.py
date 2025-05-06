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
        "url": "https://tile.loc.gov/storage-services/media/ls/sagan/1958124-3-1.mp3"
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