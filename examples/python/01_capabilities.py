import json
from client import request
print(json.dumps(request("GET", "/v1/meta/capabilities", {"platform":"zillow","country":"US"}), indent=2))
