import {RealtyCrawlClient} from './client.mjs';
console.log(JSON.stringify(await new RealtyCrawlClient().get('/v1/meta/capabilities',{platform:'zillow',country:'US'},{authenticated:false}),null,2));
