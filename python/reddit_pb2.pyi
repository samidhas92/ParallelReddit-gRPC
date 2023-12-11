from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PostState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    POST_NORMAL: _ClassVar[PostState]
    POST_LOCKED: _ClassVar[PostState]
    POST_HIDDEN: _ClassVar[PostState]

class CommentState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    COMMENT_NORMAL: _ClassVar[CommentState]
    COMMENT_HIDDEN: _ClassVar[CommentState]

class SubredditVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    SUBREDDIT_PUBLIC: _ClassVar[SubredditVisibility]
    SUBREDDIT_PRIVATE: _ClassVar[SubredditVisibility]
    SUBREDDIT_HIDDEN: _ClassVar[SubredditVisibility]
POST_NORMAL: PostState
POST_LOCKED: PostState
POST_HIDDEN: PostState
COMMENT_NORMAL: CommentState
COMMENT_HIDDEN: CommentState
SUBREDDIT_PUBLIC: SubredditVisibility
SUBREDDIT_PRIVATE: SubredditVisibility
SUBREDDIT_HIDDEN: SubredditVisibility

class User(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class Subreddit(_message.Message):
    __slots__ = ["name", "visibility", "tags"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    name: str
    visibility: SubredditVisibility
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., visibility: _Optional[_Union[SubredditVisibility, str]] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class Post(_message.Message):
    __slots__ = ["title", "text", "video_url", "image_url", "author", "score", "state", "publication_date", "subreddit", "tags", "id"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VIDEO_URL_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    SUBREDDIT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    title: str
    text: str
    video_url: str
    image_url: str
    author: str
    score: int
    state: PostState
    publication_date: str
    subreddit: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    id: str
    def __init__(self, title: _Optional[str] = ..., text: _Optional[str] = ..., video_url: _Optional[str] = ..., image_url: _Optional[str] = ..., author: _Optional[str] = ..., score: _Optional[int] = ..., state: _Optional[_Union[PostState, str]] = ..., publication_date: _Optional[str] = ..., subreddit: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., id: _Optional[str] = ...) -> None: ...

class Comment(_message.Message):
    __slots__ = ["author", "text", "score", "state", "publication_date", "post_id", "comment_id", "id"]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLICATION_DATE_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    author: str
    text: str
    score: int
    state: CommentState
    publication_date: str
    post_id: str
    comment_id: str
    id: str
    def __init__(self, author: _Optional[str] = ..., text: _Optional[str] = ..., score: _Optional[int] = ..., state: _Optional[_Union[CommentState, str]] = ..., publication_date: _Optional[str] = ..., post_id: _Optional[str] = ..., comment_id: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class VoteRequest(_message.Message):
    __slots__ = ["id", "upvote"]
    ID_FIELD_NUMBER: _ClassVar[int]
    UPVOTE_FIELD_NUMBER: _ClassVar[int]
    id: str
    upvote: bool
    def __init__(self, id: _Optional[str] = ..., upvote: bool = ...) -> None: ...

class VoteResponse(_message.Message):
    __slots__ = ["newScore", "id"]
    NEWSCORE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    newScore: int
    id: str
    def __init__(self, newScore: _Optional[int] = ..., id: _Optional[str] = ...) -> None: ...

class PostRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CommentsRequest(_message.Message):
    __slots__ = ["post_id", "limit"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    post_id: str
    limit: int
    def __init__(self, post_id: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class CommentWithReplies(_message.Message):
    __slots__ = ["comment", "replies", "has_more_replies"]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    REPLIES_FIELD_NUMBER: _ClassVar[int]
    HAS_MORE_REPLIES_FIELD_NUMBER: _ClassVar[int]
    comment: Comment
    replies: _containers.RepeatedCompositeFieldContainer[Comment]
    has_more_replies: bool
    def __init__(self, comment: _Optional[_Union[Comment, _Mapping]] = ..., replies: _Optional[_Iterable[_Union[Comment, _Mapping]]] = ..., has_more_replies: bool = ...) -> None: ...

class CommentsResponse(_message.Message):
    __slots__ = ["comments"]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    comments: _containers.RepeatedCompositeFieldContainer[CommentWithReplies]
    def __init__(self, comments: _Optional[_Iterable[_Union[CommentWithReplies, _Mapping]]] = ...) -> None: ...

class ExpandRequest(_message.Message):
    __slots__ = ["comment_id", "limit"]
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    comment_id: str
    limit: int
    def __init__(self, comment_id: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class MonitorRequest(_message.Message):
    __slots__ = ["post_id", "comment_ids"]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    post_id: str
    comment_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, post_id: _Optional[str] = ..., comment_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ["id", "newScore"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NEWSCORE_FIELD_NUMBER: _ClassVar[int]
    id: str
    newScore: int
    def __init__(self, id: _Optional[str] = ..., newScore: _Optional[int] = ...) -> None: ...
