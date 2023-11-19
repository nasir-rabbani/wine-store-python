import unittest
from unittest.mock import patch
import main


class RecommendationStreamConsumerTestCase(unittest.TestCase):
    @patch("main.boto3.client")
    def test_poll_kinesis_stream(self, mock_kinesis_client):
        # Mock the Kinesis client and its methods to test polling behavior
        main.poll_kinesis_stream()
        # Assert that Kinesis client methods were called as expected
        mock_kinesis_client.assert_called_with("kinesis", region_name="us-east-1")


if __name__ == "__main__":
    unittest.main()
