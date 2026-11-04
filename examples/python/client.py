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
    if parameters is not None and not isinstance(parameters, dict):
        raise RealtyCrawlError("parameters must be a JSON object")
    params = dict(parameters or {})
    response_options = {name: params.pop(name) for name in ("fields", "format") if name in params}
    response_format = response_options.get("format", "json")
    if response_format not in ("json", "csv", "ndjson"):
        raise RealtyCrawlError("format must be json, csv, or ndjson")
    if "fields" in response_options and not isinstance(response_options["fields"], str):
        raise RealtyCrawlError("fields must be a comma-separated string")
    if public and response_options:
        raise RealtyCrawlError("Response fields and exports are available only on data operations")
    if response_format != "json":
        headers["Accept"] = "text/csv" if response_format == "csv" else "application/x-ndjson"
    body = json.dumps(params).encode() if method == "POST" else None
    if body and len(body) > 65536:
        raise RealtyCrawlError("Request exceeds 64 KiB")
    url = ORIGIN + path
    query = {**(params if method == "GET" else {}), **response_options}
    if query:
        url += "?" + urllib.parse.urlencode(query)
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with (opener or urllib.request.build_opener(NoRedirect)).open(req, timeout=60) as response:
            raw = response.read(8*1024*1024+1)
            response_headers = getattr(response, "headers", {})
    except urllib.error.HTTPError as error:
        try:
            raw = error.read(65536)
        finally:
            error.close()
        try:
            payload = json.loads(raw)
        except ValueError:
            payload = {}
        detail = payload.get("error", {})
        raise RealtyCrawlError(f"HTTP {error.code}: {detail.get('code', 'API_ERROR')}. Request ID: {payload.get('request_id', (error.headers or {}).get('x-request-id', 'unknown'))}. No retry made.") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise RealtyCrawlError("Connection failed. No retry made; preserve the idempotency key.") from None
    if len(raw) > 8*1024*1024:
        raise RealtyCrawlError("Response exceeds 8 MiB; narrow the request")
    content_type = response_headers.get("content-type", "").split(";", 1)[0].strip().lower()
    if content_type in ("text/csv", "application/x-ndjson"):
        request_id = response_headers.get("x-request-id")
        if not request_id:
            raise RealtyCrawlError("Export response is missing its request ID")
        def count(name):
            value = response_headers.get(name)
            return int(value) if value is not None and re.fullmatch(r"[0-9]+", value) else None
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            raise RealtyCrawlError("Invalid export encoding") from None
        return {"format": "csv" if content_type == "text/csv" else "ndjson", "content": content, "meta": {"request_id": request_id, "credits_used": count("x-credits-used"), "credits_remaining": count("x-credits-remaining"), "row_count": count("x-row-count"), "idempotent_replay": response_headers.get("x-idempotent-replay") == "true"}}
    try:
        result = json.loads(raw)
    except ValueError:
        raise RealtyCrawlError("Invalid response JSON") from None
    if path != "/v1/openapi.json" and (not isinstance(result, dict) or "data" not in result or not isinstance(result.get("meta"), dict) or not result["meta"].get("request_id")):
        raise RealtyCrawlError("Invalid RealtyCrawl response envelope")
    return result
