# server/server.py
import sys
import time
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
from concurrent import futures
import grpc
import reddit_pb2 as r_pb2
import reddit_pb2_grpc as r_grpc
import argparse
from datetime import datetime

class RedditService(r_grpc.RedditServicer):
    def __init__(self):
        self.posts = {}  # In-memory storage for posts
        self.comments = {}
        self.comment_replies = {}

    def CreatePost(self, request, context):
        post_id = str(len(self.posts) + 1)  # Simple way to generate a unique ID
        new_post = r_pb2.Post(
            title=request.title,
            text=request.text,
            image_url = request.image_url,
            author=request.author,
            score=0,
            state=r_pb2.PostState.POST_NORMAL,
            publication_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            subreddit=request.subreddit,
            tags=request.tags,
            id= post_id
        )
        self.posts[post_id] = new_post
        # print(f"Post created with ID: {post_id} and title: {request.title}")
        return new_post
    
    def VotePost(self, request, context):
        post_id = request.id
        if post_id in self.posts:
            if request.upvote:
                self.posts[post_id].score += 1
            else:
                self.posts[post_id].score -= 1
            return r_pb2.VoteResponse(newScore=self.posts[post_id].score, id=request.id)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Post not found')
            return r_pb2.VoteResponse()
        
    def RetrievePost(self, request, context):
        post_id = request.id
        if post_id in self.posts:
            return self.posts[post_id]
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Post not found')
            return r_pb2.Post()
        
    def CreateComment(self, request, context):
       comment_id = str(len(self.comments) + 1)
       # Determine whether the comment is under a post or a reply to another comment
       if request.WhichOneof('parent') == 'post_id':
           # Check if the referenced post exists
           if request.post_id not in self.posts:
               context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
           new_comment = r_pb2.Comment(
               author=request.author,
               text=request.text,
               score=0,
               state=r_pb2.CommentState.COMMENT_NORMAL,
               publication_date=datetime.now().isoformat(),
               post_id=request.post_id,
               id= comment_id
           )
           print(new_comment)
       elif request.WhichOneof('parent') == 'comment_id':
           # Check if the referenced comment exists
           if request.comment_id not in self.comments:
               context.abort(grpc.StatusCode.NOT_FOUND, "Parent comment not found")
           # Fetch the post_id from the parent comment to maintain the link to the original post
           new_comment = r_pb2.Comment(
               author=request.author,
               text=request.text,
               score=0,
               state=r_pb2.CommentState.COMMENT_NORMAL,
               publication_date=datetime.now().isoformat(),
               comment_id=request.comment_id,
               id=comment_id
           )
           parent_comment_id = request.comment_id #this itself is eindex of comments comments array
           if parent_comment_id not in self.comment_replies:
               self.comment_replies[parent_comment_id] = []
           self.comment_replies[parent_comment_id].append(comment_id)
       else:
           context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid parent identifier")
       self.comments[comment_id] = new_comment
       return new_comment
    
    def VoteComment(self, request, context):
        comment_id = request.id
        if comment_id in self.comments:
            # Update the score of the comment based on the upvote/downvote
            if request.upvote:
                self.comments[comment_id].score += 1
            else:
                self.comments[comment_id].score -= 1
            return r_pb2.VoteResponse(newScore=self.comments[comment_id].score, id=request.id)
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, "Comment not found")

    def RetrieveComments(self, request, context):
        post_id = request.post_id
        limit = request.limit
    
        if post_id not in self.posts:
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found")
    

        post_comments = [comment for comment in self.comments.values() if comment.post_id == post_id]

        top_comments = sorted(post_comments, key=lambda c: c.score, reverse=True)[:limit]
    
        print("Comment Replies Mapping:", self.comment_replies)  # Debug print
        
        response = r_pb2.CommentsResponse()
                 
        for comment in top_comments:
                 comment_with_replies = r_pb2.CommentWithReplies(
                    comment=comment, 
                    has_more_replies=len(self.comment_replies.get(comment.id, [])) > 0
                 )
                 response.comments.append(comment_with_replies)   
     
        return response

    def ExpandCommentBranch(self, request, context):
        parent_comment_id = request.comment_id
        limit = request.limit

        if parent_comment_id not in self.comments:
            context.abort(grpc.StatusCode.NOT_FOUND, "Parent comment not found")
        # Retrieve the top N replies to the parent comment
        first_level_replies = [(reply_id, self.comments[reply_id]) for reply_id in self.comment_replies.get(parent_comment_id, [])]
        top_first_level = sorted(first_level_replies, key=lambda item: item[1].score, reverse=True)[:limit]
        
        response = r_pb2.CommentsResponse()
        for reply_id, reply in top_first_level:
            # For each top reply, retrieve its top N replies
            second_level_replies = [(sub_reply_id, self.comments[sub_reply_id]) for sub_reply_id in self.comment_replies.get(reply_id, [])]
            top_second_level = sorted(second_level_replies, key=lambda item: item[1].score, reverse=True)[:limit]

            comment_with_replies = r_pb2.CommentWithReplies(
                comment=reply,
                replies=[sub_reply[1] for sub_reply in top_second_level],
                has_more_replies=len(self.comment_replies.get(reply_id, [])) > limit
            )
            response.comments.append(comment_with_replies)

        return response

    def MonitorUpdates(self, request, context):
        post_id = request.post_id
        comment_ids = set(request.comment_ids)

        try:
            while context.is_active():  # Keep the stream open
                # Send updates for the post
                if post_id in self.posts:
                    yield r_pb2.UpdateResponse(id=post_id, newScore=self.posts[post_id].score)
                    print(f"Sent update for post {post_id}")

                # Send updates for comments
                for comment_id in comment_ids:
                    if comment_id in self.comments:
                        yield r_pb2.UpdateResponse(id=comment_id, newScore=self.comments[comment_id].score)
                        print(f"Sent update for comment {comment_id}")

                # Simulate delay for next round of updates
                time.sleep(5)
        except Exception as e:
            print(f"Exception in MonitorUpdates: {e}")    
    
def serve(host, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    r_grpc.add_RedditServicer_to_server(RedditService(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    print(f"Server started listening on {host}:{port}")
    server.wait_for_termination()


if __name__ == "__main__":
    # Parse command-line arguments for host and port
    parser = argparse.ArgumentParser(description="gRPC Server")
    parser.add_argument("--host", type=str, default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=50051, help="Server port")
    args = parser.parse_args()

    # Start the gRPC server
    serve(args.host, args.port)
