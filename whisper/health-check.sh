#!/bin/bash
if [ -z "$DATACRUNCH_CONTAINER_URL" ] || [ -z "$DATACRUNCH_BEARER_TOKEN" ]; then
  echo "Error: DATACRUNCH_CONTAINER_URL and DATACRUNCH_BEARER_TOKEN environment variables must be set"
  exit 1
fi

curl -X GET "$DATACRUNCH_CONTAINER_URL/fastapi-uvicorn-whisper-test/health" \
--header "Authorization: Bearer $DATACRUNCH_BEARER_TOKEN" \
--header "Content-Type: application/json"
