
from abc import ABC, abstractmethod
from typing import List

from kag.builder.component.base import BuilderComponent
from kag.builder.model.chunk import Chunk
from knext.common.base.runnable import Input, Output


class SplitterABC(BuilderComponent, ABC):
    """
    Interface for splitting chunk into a list of smaller chunks.
    """

    @property
    def input_types(self) -> Input:
        return Chunk

    @property
    def output_types(self) -> Output:
        return Chunk

    @abstractmethod
    def invoke(self, input: Input, **kwargs) -> List[Output]:
        raise NotImplementedError(
            f"`invoke` is not currently supported for {self.__class__.__name__}."
        )
