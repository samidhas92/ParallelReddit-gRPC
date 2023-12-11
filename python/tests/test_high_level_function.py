# test_high_level_function.py
import sys
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root) + "/client")
import unittest
from unittest.mock import MagicMock
from high_level_function import retrieve_expand_and_get_top_reply

class TestHighLevelFunction(unittest.TestCase):
    def setUp(self):
        # Mock the RedditClient
        self.mock_client = MagicMock()

        # Set up the mock data for retrieve_post
        self.mock_client.retrieve_post.return_value = MagicMock()

        # Set up the mock data for retrieve_comments
        self.mock_client.retrieve_comments.return_value = MagicMock(comments=[
            MagicMock(comment=MagicMock(id='1', score=10)),
            MagicMock(comment=MagicMock(id='2', score=20)),
            MagicMock(comment=MagicMock(id='3', score=5))
        ])

        # Set up the mock data for expand_comment_branch
        self.mock_client.expand_comment_branch.return_value = MagicMock(comments=[
            MagicMock(replies=[
                MagicMock(score=15),
                MagicMock(score=25)
            ])
        ])

    def test_retrieve_expand_and_get_top_reply(self):
        # Use the mock client to test the function
        top_reply = retrieve_expand_and_get_top_reply(self.mock_client, '1')

        # Assertions to check the expected behavior
        self.assertIsNotNone(top_reply, "Expected top reply to be not None")
        self.assertEqual(top_reply.score, 25, "Expected top reply score to be 25")

        # Verify the methods were called with correct arguments
        self.mock_client.retrieve_post.assert_called_once_with('1')
        self.mock_client.retrieve_comments.assert_called_once_with('1', limit=3)
        self.mock_client.expand_comment_branch.assert_called_once_with('2', limit=2)

if __name__ == '__main__':
    unittest.main()
