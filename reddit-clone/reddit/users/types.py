from __future__ import annotations

from typing import List, Optional

from strawberry import type, field
from strawberry.types import Info
from sqlalchemy import select

from reddit.users.models import User
from reddit.base.types import NodeType
from reddit.posts.types import PostType
from reddit.subreddits.types import SubredditType
from reddit.comments.types import CommentType
from reddit.database import get_session


@type(name="User")
class UserType(NodeType):
    username: str = field(
        description="""
        The username of the user.
        """
    )

    avatar: str = field(
        description="""
        The avatar URL of the user.
        """
    )

    posts: List[PostType] = field(
        description="""
        The posts for the user.
        """
    )

    subreddits: List[SubredditType] = field(
        description="""
        The subreddits the user is in.
        """
    )

    comments: List[CommentType] = field(
        description="""
        The comments for the user.
        """
    )

    @classmethod
    async def get_node(cls, info: Info, user_id: str) -> Optional[UserType]:
        """
        Gets an user with the given ID.
        """
        query = select(User).filter_by(id=user_id).first()
        async with get_session() as session:
            user = await session.execute(query)
        if user is not None:
            return cls.from_instance(user)

    @classmethod
    def from_instance(cls, instance: User) -> UserType:
        return UserType(
            id=instance.id,
            username=instance.username,
            avatar=instance.avatar,
            posts=instance.posts,
            subreddits=instance.subreddits,
            comments=instance.comments,
        )
