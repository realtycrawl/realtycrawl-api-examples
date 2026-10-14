import {RealtyCrawlClient} from './client.mjs';
const idempotencyKey=process.env.REALTYCRAWL_IDEMPOTENCY_KEY;
if(!idempotencyKey)throw Error('Set REALTYCRAWL_IDEMPOTENCY_KEY; reuse it only for an identical retry.');
const body={"location": {"kind": "bbox", "bbox": [-97.82, 30.2, -97.65, 30.35]}, "transaction": "sale", "limit": 1};
console.log(JSON.stringify(await new RealtyCrawlClient().request('POST','/v1/zillow/listings/search',body,{maxCredits:50,idempotencyKey}),null,2));
