import app
import unittest

class ProtocolTests(unittest.TestCase):
    def test_is_http(self):
        ''' Returns true that the given URI is http '''
        result = app.getProtocolBool('http://www.google.com/')
        self.assertEqual(True, result)

    def test_is_https(self):
        ''' Returns true that the given URI is https '''
        result = app.getProtocolBool('https://www.google.com/')
        self.assertEqual(True, result)

    def test_is_other(self):
        ''' Returns False to stop the process of generating a short link '''
        result = app.getProtocolBool('ftp://127.0.0.1/')
        self.assertEqual(False, result)

    def test_is_unknown(self):
        ''' Returns 'unknown' and we'll append http and continue '''
        result = app.getProtocolBool('www.google.com/')
        self.assertEqual('unknown', result)

class StatusCodeBoolTests(unittest.TestCase):
    def test_is_not_error(self):
        ''' Status code is < 400 '''
        result = app.getStatusCodeBool('http://httpstat.us/200')
        self.assertEqual(True, result)

    def test_is_error(self):
        ''' Given address returns some sort of error '''
        result = app.getStatusCodeBool('http://httpstat.us/418')
        self.assertEqual(False, result)

class GoogleSafetyTests(unittest.TestCase):
    def test_is_safe(self):
        ''' Given address returns "ok" if it is NOT in G's list '''
        result = app.getGglSafeBrowsingStatus('http://www.google.com/')
        self.assertEqual('ok', result)

    def test_is_not_safe(self):
        ''' Given address returns 200 in [0] if IT IS in G's list '''
        result = app.getGglSafeBrowsingStatus('http://malware.testing.google.test/testing/malware/')
        self.assertEqual(200, result[0])

if __name__ == '__main__':
    unittest.main()