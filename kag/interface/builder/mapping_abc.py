
from abc import ABC, abstractmethod
from typing import List, Dict

from kag.builder.component.base import BuilderComponent
from kag.builder.model.sub_graph import SubGraph
from knext.common.base.runnable import Input, Output


class MappingABC(BuilderComponent, ABC):
    """
    Interface for mapping structured dicts to a list SubGraph, which can be written into KG storage.
    """

    @property
    def input_types(self):
        return Dict

    @property
    def output_types(self):
        return SubGraph

    @abstractmethod
    def invoke(self, input: Input, **kwargs) -> List[Output]:
        raise NotImplementedError(
            f"`invoke` is not currently supported for {self.__class__.__name__}."
        )
