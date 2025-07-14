import unittest
from unittest.mock import patch, Mock
from recontrack.extractor import TrackingCodeExtractor

class TestTrackingCodeExtractor(unittest.TestCase):

    @patch('recontrack.extractor.requests.get')
    def test_fetch_and_extract(self, mock_get):
        # Exemple simple de contenu HTML avec Google Analytics et Facebook Pixel
        example_html = '''
        <html>
        <head>
            <script>
                var _gaq = _gaq || [];
                _gaq.push(['_setAccount', 'UA-12345678-1']);
            </script>
            <script>
                !function(f,b,e,v,n,t,s)
                {n=f.fbq=function(){n.callMethod?
                n.callMethod.apply(n,arguments):n.queue.push(arguments)};
                fbq('init', '123456789012345');}
            </script>
        </head>
        <body>Test page</body>
        </html>
        '''

        # Mock de la réponse HTTP
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = 'https://final-url.com'
        mock_response.text = example_html
        mock_get.return_value = mock_response

        url = 'https://dummy-url.com'
        extractor = TrackingCodeExtractor(url)
        extractor.fetch()
        self.assertEqual(extractor.final_url, 'https://final-url.com')
        self.assertIn('UA-12345678-1', example_html)  # vérif simple du contenu mocké

        extractor.extract_codes()
        results = extractor.get_results()

        sources = [r.source for r in results]
        codes = [r.code for r in results]

        self.assertIn('Google Analytics (UA)', sources)
        self.assertIn('Facebook Pixel', sources)
        self.assertIn('UA-12345678-1', codes)
        self.assertIn('123456789012345', codes)

if __name__ == '__main__':
    unittest.main()
