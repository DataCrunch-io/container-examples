#!/bin/bash
if [ -z "$DATACRUNCH_DEPLOYMENT" ] || [ -z "$DATACRUNCH_BEARER_TOKEN" ]; then
  echo "Error: DATACRUNCH_DEPLOYMENT and DATACRUNCH_BEARER_TOKEN environment variables must be set"
  exit 1
fi

ENDPOINT=https://containers.datacrunch.io/$DATACRUNCH_DEPLOYMENT/health
echo "Connecting to health-check endpoint at $ENDPOINT..."

curl -X GET $ENDPOINT \
--header "Authorization: Bearer $DATACRUNCH_BEARER_TOKEN" \
--header "Content-Type: application/json"