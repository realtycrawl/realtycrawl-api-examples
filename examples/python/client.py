"""Bounded RealtyCrawl requests. No automatic retries or redirects."""
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
ORIGIN = "https://realtycrawl.dev"
class RealtyCrawlError(RuntimeError):
    pass
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def request(method, path, parameters=None, *, max_credits=None, idempotency_key=None, api_key=None, opener=None):
    if method not in ("GET", "POST") or not re.fullmatch(r"/v1/[A-Za-z0-9_.:~/-]+", path) or ".." in path or "//" in path:
        raise RealtyCrawlError("Unsupported API method or path")
    public = path.startswith("/v1/meta/") or path == "/v1/openapi.json"
    headers = {"Accept": "application/json"}
    if not public:
        key = api_key or os.environ.get("REALTYCRAWL_API_KEY")
        if not key:
            raise RealtyCrawlError("Set REALTYCRAWL_API_KEY")
        if type(max_credits) is not int or max_credits < 1:
            raise RealtyCrawlError("Set a positive max_credits budget")
        headers["Authorization"] = "Bearer " + key
    if max_credits is not None:
        if type(max_credits) is not int or max_credits < 0:
            raise RealtyCrawlError("Invalid max_credits")
        headers["X-Max-Credits"] = str(max_credits)
    if method == "POST":
        if not idempotency_key or not re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", idempotency_key):
            raise RealtyCrawlError("Provide a stable idempotency_key (1-128 letters, digits, _, ., :, -)")
        headers["Idempotency-Key"] = idempotency_key
        headers["Content-Type"] = "application/json"
    params = parameters or {}
    body = json.dumps(params).encode() if method == "POST" else None
    if body and len(body) > 65536:
        raise RealtyCrawlError("Request exceeds 64 KiB")
    url = ORIGIN + path
    if method == "GET" and params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with (opener or urllib.request.build_opener(NoRedirect)).open(req, timeout=60) as response:
            raw = response.read(8*1024*1024+1)
    except urllib.error.HTTPError as error:
        raw = error.read(65536)
        try:
            payload = json.loads(raw)
        except ValueError:
            payload = {}
        detail = payload.get("error", {})
        raise RealtyCrawlError(f"HTTP {error.code}: {detail.get('code', 'API_ERROR')}. Request ID: {payload.get('request_id', error.headers.get('x-request-id', 'unknown'))}. No retry made.") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise RealtyCrawlError("Connection failed. No retry made; preserve the idempotency key.") from None
    if len(raw) > 8*1024*1024:
        raise RealtyCrawlError("Response exceeds 8 MiB; narrow the request")
    try:
        result = json.loads(raw)
    except ValueError:
        raise RealtyCrawlError("Invalid response JSON") from None
    if path != "/v1/openapi.json" and (not isinstance(result, dict) or "data" not in result or not result.get("meta", {}).get("request_id")):
        raise RealtyCrawlError("Invalid RealtyCrawl response envelope")
    return result
