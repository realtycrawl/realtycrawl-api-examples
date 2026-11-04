import {RealtyCrawlClient} from './client.mjs';
const nativeId=process.argv[2];
if(!/^[1-9]\d{0,14}$/.test(nativeId??''))throw Error('Usage: node examples/node/04-zillow-detail.mjs ZPID');
console.log(JSON.stringify(await new RealtyCrawlClient().callEndpoint({endpointId:'getPlatformListing',parameters:{platform:'zillow',native_id:nativeId},maxCredits:50}),null,2));
