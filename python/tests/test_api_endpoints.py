import unittest
from unittest.mock import MagicMock, patch
# test_high_level_function.py
import sys
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root) + "/client")
import unittest
from unittest.mock import MagicMock
from reddit_client import RedditClient
# Mock data for testing
mock_posts = {
    "1": {"title": "My trip to Italy", "text": "I loved italy", "score": 0},
    "2": {"title": "Daily Discussion", "text": "Open topic", "score": 0}
}

mock_comments = {
    "1": {"text": "Great post!", "score": 0, "post_id": "1"},
    "2": {"text": "Thanks for sharing", "score": 0, "post_id": "1"},
    "3": {"text": "Interesting point", "score": 0, "post_id": "2"}
}

class TestRedditAPI(unittest.TestCase):
    @patch('reddit_client.RedditClient')
    def setUp(self, MockRedditClient):
        self.client = MockRedditClient()

        # Setup the mock methods with return values
        self.client.create_post.side_effect = self.mock_create_post
        self.client.vote_post.side_effect = self.mock_vote_post
        self.client.retrieve_post.side_effect = self.mock_retrieve_post
        self.client.create_comment.side_effect = self.mock_create_comment
        self.client.vote_comment.side_effect = self.mock_vote_comment
        self.client.retrieve_comments.side_effect = self.mock_retrieve_comments
        self.client.expand_comment_branch.side_effect = self.mock_expand_comment_branch

    def mock_create_post(self, title, text, image_url, author, subreddit, tags):
        # Assuming you have a global or class-level dictionary to store posts for mocking
        post_id = str(len(mock_posts) + 1)  # Generate a unique post ID
        new_post = {
            "title": title,
            "text": text,
            "image_url": image_url,
            "author": author,
            "subreddit": subreddit,
            "tags": tags,
            "score": 0,  # Initial score is set to 0
            "id": post_id  # Assign the unique ID to the post
        }
        
        # Add the new post to the mock posts dictionary
        mock_posts[post_id] = new_post
        
        # Return the new post data as the response
        return new_post

    def mock_vote_post(self, post_id, upvote):
        if post_id in mock_posts:
            mock_posts[post_id]["score"] += 1 if upvote else -1
            return mock_posts[post_id]["score"]
        else:
            raise ValueError("Post not found")
    
    def mock_retrieve_post(self, post_id):
        if post_id in mock_posts:
            return mock_posts[post_id]
        else:
            raise ValueError("Post not found")
    
    def mock_create_comment(self, text, author, post_id=None, comment_id=None):
        comment_id = str(len(mock_comments) + 1)
        new_comment = {"text": text, "score": 0, "id": comment_id, "post_id": post_id or None}
        mock_comments[comment_id] = new_comment
        return new_comment
    
    def mock_vote_comment(self, comment_id, upvote):
        if comment_id in mock_comments:
            mock_comments[comment_id]["score"] += 1 if upvote else -1
            return mock_comments[comment_id]["score"]
        else:
            raise ValueError("Comment not found")
    
    def mock_retrieve_comments(self, post_id, limit):
        comments = [comment for comment in mock_comments.values() if comment["post_id"] == post_id]
        sorted_comments = sorted(comments, key=lambda c: c["score"], reverse=True)[:limit]
        return sorted_comments
    
    def mock_expand_comment_branch(self, comment_id, limit):
        # Assuming that 'replies' is a list of comment IDs replying to this comment
        replies = [comment for id, comment in mock_comments.items() if comment.get("reply_to") == comment_id]
        sorted_replies = sorted(replies, key=lambda c: c["score"], reverse=True)[:limit]
        return {"comment": mock_comments[comment_id], "replies": sorted_replies}
    
    # Test cases for the API endpoints
    def test_create_post(self):
        title = "Test Post"
        text = "This is a test post."
        response = self.client.create_post(title, text, None, "testuser", "testsubreddit", [])
        self.assertEqual(response["title"], title)
        self.assertEqual(response["text"], text)
    
    def test_vote_post(self):
        response = self.client.vote_post("1", True)
        self.assertEqual(response, 1)
    
    def test_retrieve_post(self):
        response = self.client.retrieve_post("1")
        self.assertEqual(response["title"], "My trip to Italy")
    
    def test_create_comment(self):
        response = self.client.create_comment("Nice post", "testuser", post_id="1")
        self.assertEqual(response["text"], "Nice post")
    
    def test_vote_comment(self):
        response = self.client.vote_comment("1", True)
        self.assertEqual(response, 1)
    
    def test_retrieve_comments(self):
        response = self.client.retrieve_comments("1", 2)
        self.assertTrue(len(response) <= 2)
    
    def test_expand_comment_branch(self):
        response = self.client.expand_comment_branch("1", 2)
        self.assertEqual(response["comment"]["text"], "Great post!")
        self.assertTrue(len(response["replies"]) <= 2)
    