#!/bin/bash
if [ -z "$DATACRUNCH_DEPLOYMENT" ] || [ -z "$DATACRUNCH_BEARER_TOKEN" ]; then
  echo "Error: DATACRUNCH_DEPLOYMENT and DATACRUNCH_BEARER environment variables must be set"
  exit 1
fi

PAYLOAD='{
  "url": "https://anchor.fm/s/f4eff228/podcast/play/93688065/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fstaging%2F2024-9-29%2F388903574-44100-2-ef9795c05ea1d.mp3"
}'

ENDPOINT="https://containers.datacrunch.io/$DATACRUNCH_DEPLOYMENT/generate" 
echo "Performing async inference at $ENDPOINT"

curl -X POST $ENDPOINT \
--header "Authorization: Bearer $DATACRUNCH_BEARER_TOKEN" \
--header "Content-Type: application/json" \
--header "Prefer: respond-async" \
--data "$PAYLOAD"