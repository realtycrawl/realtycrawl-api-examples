#!/usr/bin/env bash
set -euo pipefail
curl --fail-with-body --max-time 60 --proto "=https" "https://realtycrawl.dev/v1/meta/capabilities?platform=zillow&country=US"
