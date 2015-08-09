import airtable
import mock
import requests
import unittest

FAKE_TABLE_NAME = 'TableName'
FAKE_BASE_ID = 'app12345'
FAKE_API_KEY = 'fake_api_key'


class TestAirtable(unittest.TestCase):
    def setUp(self):
        self.base_id = FAKE_BASE_ID
        self.api_key = FAKE_API_KEY
        self.airtable = airtable.Airtable(self.base_id, self.api_key)

    def test_build_base_url(self):
        self.assertEqual(self.airtable.base_url,
                         'https://api.airtable.com/v0/app12345')

    def test_build_headers(self):
        self.assertEqual(self.airtable.headers['Authorization'],
                         'Bearer fake_api_key')

    @mock.patch.object(requests, 'request')
    def test_get_all(self, mock_request):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'records': [
                {
                    'id': 'reccA6yaHKzw5Zlp0',
                    'fields': {
                        'Name': 'John',
                        'Number': '(987) 654-3210'
                    }
                },
                {
                    'id': 'reccg3Kke0QvTDW0H',
                    'fields': {
                        'Name': 'Nico',
                        'Number': '(123) 222-1131'
                    }
                }
            ],
            'offset': 'reccg3Kke0QvTDW0H'
        }
        mock_request.return_value = mock_response
        r = self.airtable.get(FAKE_TABLE_NAME)
        self.assertEqual(len(r['records']), 2)
        self.assertEqual(r['offset'], 'reccg3Kke0QvTDW0H')

    @mock.patch.object(requests, 'request')
    def test_get_by_id(self, mock_request):
        fake_id = 'reccA6yaHKzw5Zlp0'
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 'reccA6yaHKzw5Zlp0',
            'fields': {
                'Name': 'John',
                'Number': '(987) 654-3210'
            }
        }
        mock_request.return_value = mock_response
        r = self.airtable.get(FAKE_TABLE_NAME, fake_id)
        self.assertEqual(r['id'], fake_id)

    @mock.patch.object(requests, 'request')
    def test_get_not_found(self, mock_request):
        mock_response = mock.MagicMock()
        mock_response.status_code = 404
        mock_request.return_value = mock_response
        r = self.airtable.get(FAKE_TABLE_NAME, '123')
        self.assertEqual(r['error']['code'], 404)
    
    def test_invalid_get(self):
        with self.assertRaises(airtable.IsNotString):
            self.airtable.get(FAKE_TABLE_NAME, 123)
            self.airtable.get(FAKE_TABLE_NAME, offset=123)
        with self.assertRaises(airtable.IsNotInteger):
            self.airtable.get(FAKE_TABLE_NAME, limit='1')

    @mock.patch.object(requests, 'request')
    def test_delete(self, mock_request):
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'deleted': True,
            'id': '1234'
        }
        mock_request.return_value = mock_response
        r = self.airtable.delete(FAKE_TABLE_NAME, '1234')
        self.assertTrue(r['deleted'])
        self.assertEqual(r['id'], '1234')

    def test_invalid_delete(self):
        with self.assertRaises(airtable.IsNotString):
            self.airtable.delete(FAKE_TABLE_NAME, 123)

if __name__ == '__main__':
    unittest.main()