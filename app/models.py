from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

# 사용자 모델
class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: str = Field(index=True, unique=True, sa_column_kwargs={"unique": True})
    password: str # 실제 앱에서는 해싱된 비밀번호를 저장

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship: User와 Post는 1:N 관계 (한 유저가 여러 게시글을 작성)
    posts: List["Post"] = Relationship(back_populates="owner")
    comments: List["Comment"] = Relationship(back_populates="owner")

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

# 게시글 모델
class PostBase(SQLModel):
    title: str = Field(index=True, min_length=1, max_length=200)
    content: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")

class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship: Post와 User는 N:1 관계 (여러 게시글이 한 유저에 속함)
    owner: Optional[User] = Relationship(back_populates="posts")
    comments: List["Comment"] = Relationship(back_populates="post")

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    owner: Optional[UserRead] = None # 게시글 조회 시 작성자 정보 포함

class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.now)

# 댓글 모델
class CommentBase(SQLModel):
    content: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    post_id: int = Field(foreign_key="post.id")
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")

class Comment(CommentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    post: Optional[Post] = Relationship(back_populates="comments")
    owner: Optional[User] = Relationship(back_populates="comments")

class CommentCreate(CommentBase):
    pass

class CommentRead(CommentBase):
    id: int
    owner: Optional[UserRead] = None # 댓글 조회 시 작성자 정보 포함

class CommentUpdate(SQLModel):
    content: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.now)