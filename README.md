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

Check that the requested capability is active for your platform and country first. The sample searches use a contiguous-US Zillow sale bounding box, `limit=1`, and `X-Max-Credits: 50`. Zillow searches cost 3 credits per returned listing; other successful platform crawls cost 50 credits. Stored listing reads cost 1 credit and use observations owned by your account, expiring after 24 hours. Research inventory is not live coverage.

## Expanded Zillow workflows

The [generated operation inventory](reference/operations.md) lists this release's complete operation IDs and routes. Current capabilities and the live OpenAPI remain authoritative. Expanded selectors and detail sections carry documentation-backed beta evidence and warnings.

| Workflow | Request | Budget and evidence |
|---|---|---|
| Sale/rental/sold search | `POST /v1/zillow/listings/search` | 3 credits per returned listing; US bbox, documented price/bed/bath/living-area/property-type filters and sorts |
| Fresh detail by ZPID | `GET /v1/zillow/listings/{native_id}` | 50 credits; optional `transaction=rent` or `status=sold` |
| Bounded detail batch | `POST /v1/zillow/listings/batch` with `native_ids` | Reserve 50 per requested ID, charge successful items only; 1–5 unique numeric ZPIDs within a shared 50-second deadline |
| Retained detail sections | `GET /v1/listings/{listing_id}/{facts,tax-history,schools,nearby,agent}` | 1 credit; collect supported fresh detail first; missing sections are unavailable |
| Field selection and exports | Data routes with `fields` and `format` query options | Same source inputs and billing; JSON, CSV or NDJSON |

Run `node examples/node/04-zillow-detail.mjs ZPID` for fresh detail, or `node examples/node/05-zillow-batch.mjs ZPID_ONE ZPID_TWO` for a batch. The batch example uses `REALTYCRAWL_IDEMPOTENCY_KEY`; inspect each item's status and error code, including `BATCH_DEADLINE_EXCEEDED`, before a deliberate retry. Run `node examples/node/06-listing-export.mjs LISTING_ID` or `python3 examples/python/04_listing_export.py LISTING_ID` to export retained facts.

Node and Python clients accept `fields` and `format` in their parameters and place them in the query string for both GET and POST. Successful CSV/NDJSON responses return `{format, content, meta}` containing text, request ID, credits, row count and replay metadata. Errors retain structured JSON handling. Stored section reads preserve unknown price bases, school units/scales and source-reported tax evidence.

Run examples individually. They do not retry or paginate automatically. Keep the same idempotency key and body for an identical retry after a connection failure; use a new key for a new logical request. The clients keep credentials on the RealtyCrawl origin, refuse redirects and use a 60-second timeout. Python and Node responses are bounded to 8 MiB.

Interpret `data` with the full `meta` envelope. Preserve source URLs, timestamps, warnings, currencies, units and unknown values. Empty results do not prove an empty market. Asking prices are not verified transaction prices.

## Validate

```bash
npm test
npm run test:live
(cd examples/go && go test ./...)
```

Offline tests use synthetic data and mock transports. Live verification fetches only public metadata and OpenAPI; it spends no credits.

[Documentation](https://realtycrawl.dev/docs) · [MCP](https://github.com/realtycrawl/realtycrawl-mcp) · [Agent skills](https://github.com/realtycrawl/realtycrawl-agent-skills) · [Examples](https://github.com/realtycrawl/realtycrawl-api-examples)

## Release compatibility

Zillow listing searches cost 3 credits per returned listing (default limit 10); fresh detail and successful batch items cost 50 each; other source crawls cost 50 credits per successful platform; stored-observation reads cost 1 credit. Metadata and idempotent replays are free. `X-Max-Credits` is a maximum budget, not a charge; inspect the live operation contract and `X-Credits-Used` before quoting costs. Check platform-operation capabilities separately: documentation-backed beta coverage is callable but has not received fresh live source acceptance. Preserve its warnings.

## Cross-platform workflows

The contract documents source-specific listing and stay filters, exact source-detail selectors, typed retained energy/flood/planning context, and saved-observation batches across the 196 in-scope sources. Fresh listing and stay detail beta requires explicit operator enablement. New bindings have documentation and offline-test evidence; check live capabilities before executing.

`getMarketSummary` derives growth from the official FHFA state index; `getPropertyZoning` reads retained NYC tax-lot labels and ratios without legal interpretation. Stay media/context reads preserve source unknowns and cost one credit; fresh supported stay details cost 50 credits on success. See the generated operation inventory for exact source associations and inputs.

`getListingLeaseTerms` reads saved commercial space counts, area ranges and labeled asking rates from CommercialCafe, CommercialSearch, CityFeet and PropertyShark. `getListingLayoutOptions` reads advertised rental ranges from Rentals.ca and Point2Homes. Both cost one credit and keep unit identity and current availability unverified. Rentals.ca documents five city regions; US state searches, HomeFinder ZIP selectors, Bproperty areas and a single Graana source page have separate documented beta scopes.

Additional source URL filters are documented for Redfin condos by US ZIP, Domain exact 1–3 bedroom apartments in Sydney NSW 2000, and Property24 positive ZAR bounds/minimum bedrooms within its source-area path. Exact REW Vancouver house, Booli Stockholm apartment and Coldwell Banker Austin condo details require separate opt-in beta enablement. REW is URL-only; source bids, tax observations and partial bathrooms keep their original meaning. These additions have offline contract evidence without fresh provider acceptance.

Use POST /v1/{platform}/listings/batch with items containing canonical URLs or supported native IDs (1–5), retaining existing selector requirements. Reserve 50 credits per item and charge only successful details. The existing Zillow native_ids batch contract is unchanged. Use POST /v1/observations/batch with resources containing a public read operation and returned ID (1–25); reserve 1 credit per item and charge only successful saved reads. Missing or expired observations remain per-item failures. No automatic retries or retention extension.

StreetEasy supplies school observations and Rightmove supplies embedded brokerage attribution where present. Tax history and nearby-home sections remain source-specific. FHFA state-market definitions can be read with GET /v1/markets/{market_id}.
