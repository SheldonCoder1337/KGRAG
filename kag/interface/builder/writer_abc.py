
from abc import ABC, abstractmethod

from kag.builder.component.base import BuilderComponent
from kag.builder.model.sub_graph import SubGraph
from knext.common.base.runnable import Input, Output


class SinkWriterABC(BuilderComponent, ABC):
    """
    Interface for writing SubGraphs to storage.
    """

    @property
    def input_types(self):
        return SubGraph

    @property
    def output_types(self):
        return None

    @abstractmethod
    def invoke(self, input: Input, **kwargs) -> Output:
        raise NotImplementedError(
            f"`invoke` is not currently supported for {self.__class__.__name__}."
        )
