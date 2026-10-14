import io, json, sys, unittest, urllib.error
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'examples/python'))
from client import request, RealtyCrawlError, NoRedirect
class Response(io.BytesIO):
    pass
class Transport:
    def __init__(self, error=None): self.calls=[]; self.error=error
    def open(self,req,timeout):
        self.calls.append((req,timeout))
        if self.error: raise self.error
        return Response(json.dumps({'data':[],'meta':{'request_id':'fixture'}}).encode())
class ClientTests(unittest.TestCase):
    def test_headers_and_body(self):
        transport=Transport()
        result=request('POST','/v1/zillow/listings/search',{'limit':1},max_credits=50,idempotency_key='request-one',api_key='test-only-key',opener=transport)
        req,timeout=transport.calls[0]
        self.assertEqual(req.full_url,'https://realtycrawl.dev/v1/zillow/listings/search')
        self.assertEqual(req.get_header('X-max-credits'),'50')
        self.assertEqual(req.get_header('Idempotency-key'),'request-one')
        self.assertEqual(timeout,60)
        self.assertEqual(json.loads(req.data),{'limit':1})
        self.assertEqual(result['meta']['request_id'],'fixture')
    def test_metadata_has_no_credentials(self):
        transport=Transport();request('GET','/v1/meta/capabilities',{'country':'US'},api_key='never-send',opener=transport)
        req,_=transport.calls[0]
        self.assertFalse(req.has_header('Authorization'))
        self.assertTrue(req.full_url.endswith('?country=US'))
    def test_preflight_guards(self):
        transport=Transport()
        for path in ['https://other.invalid/v1/a','/v1/../key','/v1//key']:
            with self.assertRaises(RealtyCrawlError):request('GET',path,opener=transport)
        for cap in [None,0,-1,True]:
            with self.assertRaises(RealtyCrawlError):request('GET','/v1/listings/one',api_key='test',max_credits=cap,opener=transport)
        with self.assertRaises(RealtyCrawlError):request('POST','/v1/listings/search',api_key='test',max_credits=50,opener=transport)
        self.assertEqual(transport.calls,[])
    def test_no_retry_or_secret_in_network_error(self):
        transport=Transport(urllib.error.URLError('secret-value'))
        with self.assertRaises(RealtyCrawlError) as caught:request('GET','/v1/meta/platforms',opener=transport)
        self.assertNotIn('secret-value',str(caught.exception));self.assertEqual(len(transport.calls),1)
    def test_no_redirect(self):
        self.assertIsNone(NoRedirect().redirect_request(None,None,302,'',{},'https://other.invalid'))
if __name__=='__main__':unittest.main()
