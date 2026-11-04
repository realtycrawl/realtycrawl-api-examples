import {RealtyCrawlClient} from './client.mjs';
const nativeIds=process.argv.slice(2),idempotencyKey=process.env.REALTYCRAWL_IDEMPOTENCY_KEY;
if(nativeIds.length<1||nativeIds.length>5||new Set(nativeIds).size!==nativeIds.length||nativeIds.some(id=>!/^[1-9]\d{0,14}$/.test(id)))throw Error('Usage: node examples/node/05-zillow-batch.mjs ZPID [ZPID ...] (1–5 unique IDs)');
if(!idempotencyKey)throw Error('Set REALTYCRAWL_IDEMPOTENCY_KEY; reuse only for an identical retry.');
console.log(JSON.stringify(await new RealtyCrawlClient().callEndpoint({endpointId:'batchZillowListings',parameters:{native_ids:nativeIds},maxCredits:50*nativeIds.length,idempotencyKey}),null,2));
