# RealtyCrawl API examples

Runnable cURL, Node.js, Python and Go examples for source-linked real estate observations. These call the hosted API and do not contain the service implementation. Use Node.js 22+, Python 3.9+, curl 7.76+, or Go 1.22+.

## Run one example

```bash
# Public discovery: no key or credits
node examples/node/01-capabilities.mjs
python3 examples/python/01_capabilities.py
bash examples/curl/capabilities.sh

# Set REALTYCRAWL_API_KEY securely in your shell, then choose ONE search:
export REALTYCRAWL_IDEMPOTENCY_KEY="unique-logical-search-id"
node examples/node/02-search.mjs
# Or: python3 examples/python/02_search.py
# Or: bash examples/curl/search.sh
# Or: (cd examples/go && go run .)

# Use data[0].id returned by the search (one credit):
node examples/node/03-listing.mjs LISTING_ID
# Or: python3 examples/python/03_listing.py LISTING_ID
```

Check that the requested capability is active for your platform and country first. The sample searches use a contiguous-US Zillow sale bounding box, `limit=1`, and `X-Max-Credits: 50`. Each successful platform crawl costs 50 credits. Stored listing reads cost 1 credit and use observations owned by your account, expiring after 24 hours. Research inventory is not live coverage.

Run examples individually. They do not retry or paginate automatically. Keep the same idempotency key and body for an identical retry after a connection failure; use a new key for a new logical request. The clients keep credentials on the RealtyCrawl origin, refuse redirects and use a 60-second timeout. Python and Node responses are bounded to 8 MiB.

Interpret `data` with the full `meta` envelope. Preserve source URLs, timestamps, warnings, currencies, units and unknown values. Empty results do not prove an empty market. Asking prices are not verified transaction prices.

## Validate

```bash
npm test
npm run test:live
(cd examples/go && go test ./...)
```

Offline tests use synthetic data and mock transports. Live verification fetches only public metadata and OpenAPI; it spends no credits.

[Documentation](https://docs.realtycrawl.dev) · [MCP](https://github.com/realtycrawl/realtycrawl-mcp) · [Agent skills](https://github.com/realtycrawl/realtycrawl-agent-skills) · [Examples](https://github.com/realtycrawl/realtycrawl-api-examples)
