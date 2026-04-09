from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # relações
    achievements: List["Achievement"] = Relationship(back_populates="user")
    comments: List["Comment"] = Relationship(back_populates="user")
    reactions: List["Reaction"] = Relationship(back_populates="user")

    # follow (self-reference)
    following: List["Follow"] = Relationship(
        back_populates="follower",
        sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"}
    )
    followers: List["Follow"] = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "[Follow.following_id]"}
    )


class Achievement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # relações
    user: Optional[User] = Relationship(back_populates="achievements")
    comments: List["Comment"] = Relationship(back_populates="achievement")
    reactions: List["Reaction"] = Relationship(back_populates="achievement")


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    achievement_id: int = Field(foreign_key="achievement.id")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # relações
    user: Optional[User] = Relationship(back_populates="comments")
    achievement: Optional[Achievement] = Relationship(back_populates="comments")


class ReactionType(str, Enum):
    # sei lá, peguei em um lugar aleatório, do qual não lembro mais :D
    # como já dizia o Michel Temer... se eu soubesse, apresentá-lo-ia
    WOW = "Eita"
    RELATABLE = "Papo Reto"
    INSIGHTFUL = "Chave Demais"
    SUPPORT = "Brabo demais"
    NEUTRAL = "Paia"
    MEH = "Chapou"


class Reaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    achievement_id: int = Field(foreign_key="achievement.id")
    type: ReactionType

    # relações
    user: Optional[User] = Relationship(back_populates="reactions")
    achievement: Optional[Achievement] = Relationship(back_populates="reactions")


class Follow(SQLModel, table=True):
    follower_id: int = Field(foreign_key="user.id", primary_key=True)
    following_id: int = Field(foreign_key="user.id", primary_key=True)

    # relações (self join)
    follower: Optional[User] = Relationship(
        back_populates="following",
        sa_relationship_kwargs={"foreign_keys": "[Follow.follower_id]"}
    )
    following: Optional[User] = Relationship(
        back_populates="followers",
        sa_relationship_kwargs={"foreign_keys": "[Follow.following_id]"}
    )
