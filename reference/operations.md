# Packaged API operation inventory

Generated from the application OpenAPI by `scripts/package-public-repos.mjs`. This release defines 52 operation templates. Check the live OpenAPI and capabilities for current source, market and selector availability; research and unavailable operations are not callable. Documentation-backed beta has offline contract evidence, without fresh live verification.

| Operation ID | Method and path | Status | Credit unit |
|---|---|---|---|
| listPlatforms | GET /v1/meta/platforms | active |  |
| listCapabilities | GET /v1/meta/capabilities | active |  |
| listSchemas | GET /v1/meta/schemas | active |  |
| searchListings | POST /v1/listings/search | beta | per_successful_platform_with_overrides |
| searchPlatformListings | POST /v1/{platform}/listings/search | beta | per_successful_platform_with_overrides |
| getPlatformListing | GET /v1/{platform}/listings/{native_id} | beta | successful_source_crawl |
| resolveListing | POST /v1/listings/resolve | beta | successful_source_crawl |
| getListing | GET /v1/listings/{listing_id} | beta | stored_observation_read |
| getListingMedia | GET /v1/listings/{listing_id}/media | beta | stored_observation_read |
| getListingHistory | GET /v1/listings/{listing_id}/history | beta | stored_observation_read |
| getListingOpenHouses | GET /v1/listings/{listing_id}/open-houses | beta |  |
| getSimilarListings | GET /v1/listings/{listing_id}/similar | beta |  |
| resolveProperty | POST /v1/properties/resolve | beta |  |
| getProperty | GET /v1/properties/{property_id} | beta |  |
| getPropertyListings | GET /v1/properties/{property_id}/listings | beta |  |
| getPropertyRecords | GET /v1/properties/{property_id}/records | beta |  |
| getPropertyTransactions | GET /v1/properties/{property_id}/transactions | beta |  |
| getPropertyTaxAssessments | GET /v1/properties/{property_id}/tax-assessments | beta |  |
| getPropertyValuations | GET /v1/properties/{property_id}/valuations | beta |  |
| getPropertyComparables | GET /v1/properties/{property_id}/comparables | beta |  |
| getBuilding | GET /v1/buildings/{building_id} | beta |  |
| getBuildingUnits | GET /v1/buildings/{building_id}/units | beta |  |
| searchDevelopments | POST /v1/developments/search | beta |  |
| getDevelopment | GET /v1/developments/{development_id} | beta |  |
| searchAgents | POST /v1/agents/search | beta |  |
| getAgent | GET /v1/agents/{agent_id} | beta |  |
| getAgentListings | GET /v1/agents/{agent_id}/listings | beta |  |
| searchAgencies | POST /v1/agencies/search | beta |  |
| getAgency | GET /v1/agencies/{agency_id} | beta |  |
| getAgencyListings | GET /v1/agencies/{agency_id}/listings | beta |  |
| searchAuctions | POST /v1/auctions/search | beta |  |
| getAuction | GET /v1/auctions/{auction_id} | beta |  |
| searchMarkets | POST /v1/markets/search | beta |  |
| searchStays | POST /v1/stays/search | beta |  |
| getStay | GET /v1/stays/{stay_id} | beta |  |
| getStayQuote | POST /v1/stays/{stay_id}/quote | beta |  |
| getStayAvailability | GET /v1/stays/{stay_id}/availability | beta |  |
| getStayReviews | GET /v1/stays/{stay_id}/reviews | beta |  |
| getMarketSeries | GET /v1/markets/{market_id}/series | beta |  |
| searchLocations | POST /v1/locations/search | beta |  |
| createReadJob | POST /v1/jobs | beta |  |
| getReadJob | GET /v1/jobs/{job_id} | beta |  |
| getReadJobResults | GET /v1/jobs/{job_id}/results | beta |  |
| getListingFacts | GET /v1/listings/{listing_id}/facts | beta | stored_observation_read |
| getListingTaxHistory | GET /v1/listings/{listing_id}/tax-history | beta | stored_observation_read |
| getListingSchools | GET /v1/listings/{listing_id}/schools | beta | stored_observation_read |
| getListingNearby | GET /v1/listings/{listing_id}/nearby | beta | stored_observation_read |
| getListingProfessional | GET /v1/listings/{listing_id}/agent | beta | stored_observation_read |
| batchZillowListings | POST /v1/zillow/listings/batch | beta | successful_source_detail |
| batchPlatformListings | POST /v1/{platform}/listings/batch | beta | successful_source_detail |
| batchReadObservations | POST /v1/observations/batch | beta | successful_stored_observation_read |
| getMarket | GET /v1/markets/{market_id} | beta | stored_observation_read |

Response-only `fields` and `format` controls apply to data operations. They do not change source input or billing. Metadata is free; stored reads cost 1 credit. Zillow listing searches cost 3 credits per returned result; fresh details cost 50 per successful item. Source-detail batches reserve 50 credits per requested item (1–5); saved-observation batches reserve 1 per requested read (1–25). Failed items refund their reservation. Check operation pricing in the live contract.
