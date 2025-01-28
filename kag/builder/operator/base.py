

from abc import ABC, abstractmethod
from typing import List

from knext.builder.operator.base import BaseOp

from kag.builder.model.sub_graph import Node, SubGraph


class FuseOpABC(BaseOp, ABC):
    """
    Interface for fusing mapped sub graphs with data in storage.

    It is usually used in mapping component for SPG builder.
    """

    @abstractmethod
    def link(self, source: SubGraph) -> List[SubGraph]:
        raise NotImplementedError(
            f"{self.__class__.__name__} need to implement `link` method."
        )

    @abstractmethod
    def merge(self, source: SubGraph, target: List[SubGraph]) -> List[SubGraph]:
        raise NotImplementedError(
            f"{self.__class__.__name__} need to implement `merge` method."
        )

    def invoke(self, source: SubGraph) -> List[SubGraph]:
        target = self.link(source)
        return self.merge(source, target)


class LinkOpABC(BaseOp, ABC):
    """
    Interface for recall nodes in storage by mapped properties.

    It is usually used in mapping component for SPG builder.
    """

    @abstractmethod
    def invoke(self, source: Node, prop_value: str, target_type: str) -> List[Node]:
        raise NotImplementedError(
            f"{self.__class__.__name__} need to implement `invoke` method."
        )
