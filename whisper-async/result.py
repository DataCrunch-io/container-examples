import requests
import sys
import os
import signal

def get_result() -> None:
    token = os.environ['DATACRUNCH_BEARER_TOKEN']
    deployment_name = os.environ['DATACRUNCH_DEPLOYMENT']
    async_task_id = os.environ['DATACRUNCH_TASK_ID']
    baseurl = "https://containers.datacrunch.io"
    status_url = f"{baseurl}/result/{deployment_name}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Inference-Id": async_task_id
    }

    response = requests.get(status_url, headers=headers)
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

    get_result()