import io, json, sys, unittest, urllib.error, urllib.parse
from pathlib import Path

root = Path(__file__).resolve().parents[1]
scripts = root / 'skills/realtycrawl/scripts' if (root / 'skills').exists() else root / 'examples/python'
sys.path.insert(0, str(scripts))
from client import request, RealtyCrawlError

class Response(io.BytesIO):
    def __init__(self, content, headers):
        super().__init__(content)
        self.headers = headers

class Transport:
    def __init__(self, content, headers):
        self.content, self.headers, self.calls = content, headers, []
    def open(self, req, timeout):
        self.calls.append(req)
        return Response(self.content, self.headers)

class ExportTests(unittest.TestCase):
    def test_post_export_options_stay_out_of_canonical_body(self):
        for output, content_type, content in [('csv', 'text/csv', b'native_id\r\n123\r\n'), ('ndjson', 'application/x-ndjson', b'{"native_id":"123"}\n')]:
            transport = Transport(content, {'content-type': content_type + '; charset=utf-8', 'x-request-id': 'export-one', 'x-credits-used': '50', 'x-row-count': '1', 'x-idempotent-replay': 'true'})
            result = request('POST', '/v1/zillow/listings/batch', {'native_ids': ['123'], 'fields': 'native_id,status', 'format': output}, api_key='fixture', max_credits=50, idempotency_key='batch-one', opener=transport)
            req = transport.calls[0]
            self.assertEqual(json.loads(req.data), {'native_ids': ['123']})
            self.assertEqual(urllib.parse.parse_qs(urllib.parse.urlsplit(req.full_url).query), {'fields': ['native_id,status'], 'format': [output]})
            self.assertEqual(req.get_header('Accept'), content_type)
            self.assertEqual(result['format'], output)
            self.assertEqual(result['content'], content.decode())
            self.assertEqual(result['meta'], {'request_id': 'export-one', 'credits_used': 50, 'credits_remaining': None, 'row_count': 1, 'idempotent_replay': True})

    def test_get_projection_retains_json_envelope(self):
        payload = {'data': {'year_built': 1979}, 'meta': {'request_id': 'facts-one'}}
        transport = Transport(json.dumps(payload).encode(), {'content-type': 'application/json'})
        self.assertEqual(request('GET', '/v1/listings/lst_example/facts', {'fields': 'year_built'}, api_key='fixture', max_credits=1, opener=transport), payload)
        self.assertTrue(transport.calls[0].full_url.endswith('?fields=year_built'))

    def test_export_errors_keep_json_failure_and_request_id(self):
        class FailedTransport:
            def open(self, req, timeout):
                raise urllib.error.HTTPError(req.full_url, 503, 'Unavailable', {'x-request-id': 'fallback'}, io.BytesIO(b'{"error":{"code":"SOURCE_UNAVAILABLE"},"request_id":"failure-one"}'))
        with self.assertRaisesRegex(RealtyCrawlError, 'SOURCE_UNAVAILABLE.*failure-one'):
            request('GET', '/v1/listings/lst_example/facts', {'format': 'csv'}, api_key='fixture', max_credits=1, opener=FailedTransport())

    def test_invalid_controls_never_dispatch(self):
        transport = Transport(b'', {})
        for params in [{'format': 'html'}, {'fields': ['id']}, ['not-an-object']]:
            with self.assertRaises(RealtyCrawlError):
                request('GET', '/v1/listings/one', params, api_key='fixture', max_credits=1, opener=transport)
        with self.assertRaises(RealtyCrawlError):
            request('GET', '/v1/meta/platforms', {'format': 'csv'}, opener=transport)
        self.assertEqual(transport.calls, [])

if __name__ == '__main__':
    unittest.main()
