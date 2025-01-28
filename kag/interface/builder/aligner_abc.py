
from abc import ABC, abstractmethod
from typing import List

from kag.builder.component.base import BuilderComponent
from kag.builder.model.sub_graph import SubGraph
from knext.common.base.runnable import Input, Output


class AlignerABC(BuilderComponent, ABC):
    """
    Interface for aligning extractor results to semantic schema.
    """

    @property
    def input_types(self):
        return SubGraph

    @property
    def output_types(self):
        return SubGraph

    @abstractmethod
    def invoke(self, input: Input, **kwargs) -> List[Output]:
        raise NotImplementedError(
            f"`invoke` is not currently supported for {self.__class__.__name__}."
        )
