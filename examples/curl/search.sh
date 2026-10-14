#!/usr/bin/env bash
set -euo pipefail
: "${REALTYCRAWL_API_KEY:?Set REALTYCRAWL_API_KEY}"
: "${REALTYCRAWL_IDEMPOTENCY_KEY:?Set a unique key; reuse only for an identical retry}"
curl --fail-with-body --max-time 60 --proto '=https' \
  https://realtycrawl.dev/v1/zillow/listings/search \
  -H "Authorization: Bearer $REALTYCRAWL_API_KEY" \
  -H 'Content-Type: application/json' \
  -H 'X-Max-Credits: 50' \
  -H "Idempotency-Key: $REALTYCRAWL_IDEMPOTENCY_KEY" \
  --data '{"location":{"kind":"bbox","bbox":[-97.82,30.2,-97.65,30.35]},"transaction":"sale","limit":1}'
