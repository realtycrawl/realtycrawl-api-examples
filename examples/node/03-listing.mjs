import {RealtyCrawlClient} from './client.mjs';
const id=process.argv[2];
if(!id||! /^[A-Za-z0-9_.:~-]{1,256}$/.test(id))throw Error('Usage: node examples/node/03-listing.mjs LISTING_ID');
console.log(JSON.stringify(await new RealtyCrawlClient().get('/v1/listings/'+encodeURIComponent(id),{},{maxCredits:1}),null,2));
