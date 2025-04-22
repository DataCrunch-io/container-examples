#!/bin/bash
if [ -z "$DATACRUNCH_CONTAINER_URL" ] || [ -z "$DATACRUNCH_BEARER_TOKEN" ]; then
  echo "Error: DATACRUNCH_CONTAINER_URL and DATACRUNCH_BEARER_TOKEN environment variables must be set"
  exit 1
fi

echo "Calling API at $DATACRUNCH_CONTAINER_URL/generate"

curl -X POST \
-F "file=@audio.wav" \
"$DATACRUNCH_CONTAINER_URL/generate" \
--header "Authorization: Bearer $DATACRUNCH_BEARER_TOKEN"
