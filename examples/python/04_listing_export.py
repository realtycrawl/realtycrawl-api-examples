import json, re, sys
from client import request
if len(sys.argv) != 2 or not re.fullmatch(r"[A-Za-z0-9_.:~-]{1,256}", sys.argv[1]):
    raise SystemExit("Usage: python3 examples/python/04_listing_export.py LISTING_ID")
print(json.dumps(request("GET", "/v1/listings/" + sys.argv[1] + "/facts", {"fields": "year_built,description", "format": "csv"}, max_credits=1), indent=2))
