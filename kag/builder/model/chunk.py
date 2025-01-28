
import hashlib
from enum import Enum
from typing import Dict, Any


class ChunkTypeEnum(str, Enum):
    Table = "TABLE"
    Text = "TEXT"


class Chunk:
    def __init__(
        self,
        id: str,
        name: str,
        content: str,
        type: ChunkTypeEnum = ChunkTypeEnum.Text,
        **kwargs
    ):
        self.id = id
        self.name = name
        self.type = type
        self.content = content
        self.kwargs = kwargs

    @staticmethod
    def generate_hash_id(value):
        if isinstance(value, str):
            value = value.encode("utf-8")
        hasher = hashlib.sha256()
        hasher.update(value)
        return hasher.hexdigest()

    def __str__(self):
        tmp = {
            "id": self.id,
            "name": self.name,
            "content": self.content
            if len(self.content) <= 64
            else self.content[:64] + " ...",
        }
        return f"<Chunk>: {tmp}"

    __repr__ = __str__

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "type": self.type.value if isinstance(self.type, ChunkTypeEnum) else self.type,
            "properties": self.kwargs,
        }

    @classmethod
    def from_dict(cls, input_: Dict[str, Any]):
        return cls(
            id=input_.get("id"),
            name=input_.get("name"),
            content=input_.get("content"),
            type=input_.get("type"),
            **input_.get("properties", {}),
        )
