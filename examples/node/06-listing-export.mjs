import {RealtyCrawlClient} from './client.mjs';
const listingId=process.argv[2];
if(!/^[A-Za-z0-9_.:~-]{1,256}$/.test(listingId??''))throw Error('Usage: node examples/node/06-listing-export.mjs LISTING_ID');
console.log(JSON.stringify(await new RealtyCrawlClient().callEndpoint({endpointId:'getListingFacts',parameters:{listing_id:listingId,fields:'year_built,description',format:'csv'},maxCredits:1}),null,2));
