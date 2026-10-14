import json, os
from client import request
body = {'location': {'kind': 'bbox', 'bbox': [-97.82, 30.2, -97.65, 30.35]}, 'transaction': 'sale', 'limit': 1}
print(json.dumps(request("POST", "/v1/zillow/listings/search", body, max_credits=50, idempotency_key=os.environ.get("REALTYCRAWL_IDEMPOTENCY_KEY")), indent=2))
