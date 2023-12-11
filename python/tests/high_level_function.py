# Import the RedditClient from the client folder
import sys
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root) + "/client")

from reddit_client import RedditClient

def retrieve_expand_and_get_top_reply(client, post_id):
    post = client.retrieve_post(post_id)
    comments_response = client.retrieve_comments(post_id, limit=3)
    top_comment = max(comments_response.comments, key=lambda c: c.comment.score)
    expanded_comment_response = client.expand_comment_branch(top_comment.comment.id, limit=2)
    top_reply = max(expanded_comment_response.comments[0].replies, key=lambda r: r.score, default=None)

    return top_reply










