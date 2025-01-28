
from abc import ABC, abstractmethod
from typing import List, Dict, Union

from kag.builder.component.base import BuilderComponent
from kag.builder.model.chunk import Chunk
from knext.common.base.runnable import Input, Output


class SourceReaderABC(BuilderComponent, ABC):
    """
    Interface for reading files into a list of unstructured chunks or structured dicts.
    """

    @property
    def input_types(self) -> Input:
        return str

    @property
    def output_types(self) -> Output:
        return Union[Chunk, Dict]

    @abstractmethod
    def invoke(self, input: Input, **kwargs) -> List[Output]:
        raise NotImplementedError(
            f"`invoke` is not currently supported for {self.__class__.__name__}."
        )
