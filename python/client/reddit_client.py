import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from concurrent import futures
import grpc
import reddit_pb2 as r_pb2
import reddit_pb2_grpc as r_grpc

class RedditClient:
    def __init__(self, host="localhost", port=50051):
        server_addr = f"{host}:{port}"
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = r_grpc.RedditStub(self.channel)

    def create_post(self, title, text, image_url, author, subreddit, tags):
        post = r_pb2.Post(title=title, text=text, image_url=image_url, author=author, subreddit=subreddit, tags=tags)
        response = self.stub.CreatePost(post)
        return response
    
    def vote_post(self, post_id, upvote=True):
        vote_request = r_pb2.VoteRequest(id=post_id, upvote=upvote)
        response = self.stub.VotePost(vote_request)
        return response

    def retrieve_post(self, post_id):
        try:
            post_request = r_pb2.PostRequest(id=post_id)
            response = self.stub.RetrievePost(post_request)
            return response
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                print("Post not found") 
            else:
                print(f"RPC failed: {e}")
            return None

    def create_comment(self, text, author, post_id=None, comment_id=None):
        try:
           if post_id:
               # Creating a comment directly under a post
               comment = r_pb2.Comment(text=text, author=author, post_id=post_id)
           elif comment_id:
               # Creating a comment as a reply to another comment
               comment = r_pb2.Comment(text=text, author=author, comment_id=comment_id)
           else:
               raise ValueError("Either post_id or parent_comment_id must be provided")
           response = self.stub.CreateComment(comment)
           return response
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                print("Parent not found") 
            else:
                print(f"RPC failed: {e}")
            return None

    def vote_comment(self, comment_id, upvote=True):
        vote_request = r_pb2.VoteRequest(id=comment_id, upvote=upvote)
        return self.stub.VoteComment(vote_request)
    
    def retrieve_comments(self, post_id, limit):
        comments_request = r_pb2.CommentsRequest(post_id=post_id, limit=limit)
        return self.stub.RetrieveComments(comments_request)

    def expand_comment_branch(self, parent_comment_id, limit):
        expand_request = r_pb2.ExpandRequest(comment_id=parent_comment_id, limit=limit)
        return self.stub.ExpandCommentBranch(expand_request)

    def monitor_updates(self, post_id, comment_ids):
        monitor_request = r_pb2.MonitorRequest(post_id=post_id, comment_ids=comment_ids)
        try:
            for update in self.stub.MonitorUpdates(monitor_request):
                print(f"Update received for ID={update.id}: New Score={update.newScore}")
        except Exception as e:
            print(f"Error during monitoring: {e}")


# Example usage
if __name__ == "__main__":
    client = RedditClient()
    title = "My trip to Italy"
    text = "I loved italy "
    author = "Samidha"  # Define the author
    subreddit = "SampleSubreddit"
    tags = ["tag1", "tag2"]
    image_url = 'https://www.google.com/search?sca_esv=589677336&q=photos&tbm=isch&source=lnms&sa=X&ved=2ahUKEwjk1oLIxIaDAxU8j4kEHQFbC2EQ0pQJegQIDRAB&biw=1440&bih=720&dpr=2#imgrc=LHC8R68-jkuwQM'

    # Create a post
    response = client.create_post(title, text, image_url, author, subreddit, tags)
    print(f"Post created with title: {response.title} \n text: {response.text} \n image_url: {response.image_url} \n author: {response.author} \n tags: {response.tags}")

    downvote_response = client.vote_post("1", False)
    print(f"New score after downvote: {downvote_response.newScore}")

    upvote_response = client.vote_post("1", True)
    print(f"New score after upvote: {upvote_response.newScore}")

    upvote_response_2 = client.vote_post("1", True)
    print(f"New score after downvote: {upvote_response_2.newScore}")

    retrieved_post = client.retrieve_post("1")
    if retrieved_post: 
        print(f"Retrieved post title: {retrieved_post.title}")

    retrieved_post = client.retrieve_post("1")
    if retrieved_post: 
        print(f"Retrieved post title: {retrieved_post.title} \n image_url: {response.image_url} \n text: {retrieved_post.text} \n author: {retrieved_post.author} \n  subreddit: {retrieved_post.subreddit} \n tags: {retrieved_post.tags}")


    response_comment_to_a_post = client.create_comment(
        text="Wow you look so the first time good",
        author="SampleAuthor",
        post_id="1"
    )

    response_comment_to_a_post = client.create_comment(
        text="Wow you look so the second time good",
        author="SampleAuthor",
        post_id="1"
    )

    response_comment_to_a_post = client.create_comment(
        text="Wow you look so the third time ",
        author="SampleAuthor",
        post_id="1"
    )

    response_comment_to_a_comment = client.create_comment(
        text="This is a comment - reply to first comment",
        author="ReplyAuthor",
        comment_id="1"  # ID of the comment you are replying to
    )
    

    response_comment_to_a_comment = client.create_comment(
        text="This is a third comment - reply to a comment 1",
        author="ReplyAuthorxx",
        comment_id="1"  # ID of the comment you are replying to
    )
    
    
    response_comment_to_a_post = client.create_comment(
        text="Wow you look so the first time good0 comment 4 but to post 1 ",
        author="SampleAuthor",
        post_id="1"
    )

    response_comment_to_a_comment = client.create_comment(
        text="This is a comment 5 - reply to a comment 2 ",
        author="ReplyAuthorxx",
        comment_id="2"  # ID of the comment you are replying to
    )

    response_comment_to_a_comment = client.create_comment(
        text="This is a comment 6 - reply to a comment 2 ",
        author="ReplyAuthorxx",
        comment_id="2"  # ID of the comment you are replying to
    )

    response_comment_to_a_comment = client.create_comment(
        text="This is a comment 7 reply to a comment 3 ",
        author="ReplyAuthorxx",
        comment_id="3"  # ID of the comment you are replying to
    )
        # Upvote a comment
    upvote_response = client.vote_comment("1", True)
    print(f"New score after upvote: {upvote_response.newScore}")

    # Downvote the same comment
    downvote_response = client.vote_comment("2", False)
    print(f"New score after downvote: {downvote_response.newScore}")


    # Downvote the same comment
    downvote_response = client.vote_comment("3", False)
    print(f"New score after downvote: {downvote_response.newScore}")

    response = client.retrieve_comments("1", 3)
    for comment_with_replies in response.comments:
        print(f"Comment: {comment_with_replies.comment.text}, Score: {comment_with_replies.comment.score}, Has replies: {'Yes' if comment_with_replies.has_more_replies else 'No'} \n")

    response = client.expand_comment_branch("1", 2)  # Example comment ID and limit
    for comment_with_replies in response.comments:
        print(f"Comment: {comment_with_replies.comment.text}, Score: {comment_with_replies.comment.score}")
        for reply in comment_with_replies.replies:
            print(f"  Reply: {reply.text}, Score: {reply.score}")

    client.monitor_updates("1", ["1", "2", "3"])  # Example post and comment IDs