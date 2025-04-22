#!/bin/bash
curl -X POST \
  -F "file=@audio.wav" \
  http://127.0.0.1:8989/generate
