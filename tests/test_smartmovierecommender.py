
import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from smartmovierecommender.main import main

class TestMovieRecommendations(unittest.TestCase):


    @patch('sys.stdout', new_callable=StringIO)
    def test_output(self, mock_stdout):
        """Test the printed output when calling the main function"""
        sys.argv = ["main", "-t", "The Other Woman"]

        main("The Other Woman")

        output = mock_stdout.getvalue()

        self.assertIn("Top Recommendations:", output)
        self.assertIn("Think Like a Man (Similarity: 1.00)", output)
        self.assertIn("What Happens in Vegas (Similarity: 1.00)", output)
        self.assertIn("Good Luck Chuck (Similarity: 0.99)", output)
        self.assertIn("He's Just Not That Into You (Similarity: 0.99)", output)
        self.assertIn("Intolerable Cruelty (Similarity: 0.99)", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_fuzzy_match(self, mock_stdout):
        """Testing that fuzzy matching works regardless of entry"""

        sys.argv = ["main", "-t", "ajdnfajnsdfnaisuhe"]

        main("ajdnfajnsdfnaisuhe")

        output = mock_stdout.getvalue()

        self.assertIn("Top Recommendations:", output)
        self.assertIn("Call Me by Your Name (Similarity: 0.99)", output)
        self.assertIn("Brokeback Mountain (Similarity: 0.98)", output)
        self.assertIn("Malcolm & Marie (Similarity: 0.98)", output)
        self.assertIn("Carol (Similarity: 0.98)", output)
        self.assertIn("Breaking the Waves (Similarity: 0.98)", output)

if __name__ == '__main__':
    unittest.main()
