import test from 'node:test';
import assert from 'node:assert/strict';
import {RealtyCrawlClient} from '../examples/node/client.mjs';

const spec={components:{schemas:{}},paths:{'/v1/zillow/listings/batch':{post:{operationId:'batchZillowListings',tags:['platform-listings'],'x-runtime-status':'beta','x-credit-cost':50,'x-credit-unit':'successful_source_detail'}},'/v1/listings/{listing_id}/facts':{get:{operationId:'getListingFacts',tags:['listings'],'x-credit-cost':1,'x-credit-unit':'stored_observation_read'}}}};

for(const format of ['csv','ndjson'])test(format+' preserves export controls, text and credit metadata for a bounded batch',async()=>{
  let captured;
  const content=format==='csv'?'native_id,status\r\n123,success\r\n':'{"native_id":"123","status":"success"}\n';
  const client=new RealtyCrawlClient({apiKey:'fixture',fetchImpl:async(url,init)=>{
    if(url.pathname==='/v1/openapi.json')return Response.json(spec);
    captured={url,init};
    return new Response(content,{headers:{'content-type':format==='csv'?'text/csv':'application/x-ndjson','x-request-id':'batch-export','x-credits-used':'50','x-row-count':'1','x-idempotent-replay':'true'}});
  }});
  const result=await client.callEndpoint({endpointId:'batchZillowListings',parameters:{native_ids:['123'],fields:'native_id,status',format},maxCredits:50,idempotencyKey:'batch-one'});
  assert.deepEqual(JSON.parse(captured.init.body),{native_ids:['123']});
  assert.equal(captured.url.searchParams.get('fields'),'native_id,status');
  assert.equal(captured.url.searchParams.get('format'),format);
  assert.equal(result.format,format);assert.equal(result.content,content);
  assert.equal(result.meta.request_id,'batch-export');assert.equal(result.meta.credits_used,50);assert.equal(result.meta.row_count,1);assert.equal(result.meta.idempotent_replay,true);
});

test('retained facts discovery and GET projection use their source operation and one-credit budget',async()=>{
  let captured;
  const payload={data:{year_built:1979},meta:{request_id:'facts-one'}};
  const client=new RealtyCrawlClient({apiKey:'fixture',fetchImpl:async(url,init)=>{
    if(url.pathname==='/v1/openapi.json'){assert.equal(init.headers.Authorization,undefined);return Response.json(spec);}
    captured={url,init};return Response.json(payload);
  }});
  assert.equal((await client.endpoint('getListingFacts')).creditCost,1);
  assert.deepEqual(await client.callEndpoint({endpointId:'getListingFacts',parameters:{listing_id:'lst_example',fields:'year_built'},maxCredits:1}),payload);
  assert.equal(captured.url.pathname,'/v1/listings/lst_example/facts');
  assert.equal(captured.url.searchParams.get('fields'),'year_built');
  assert.equal(captured.init.headers['X-Max-Credits'],'1');
  assert.equal(captured.init.body,undefined);
});
