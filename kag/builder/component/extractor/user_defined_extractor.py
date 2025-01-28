from typing import Dict, List

from knext.common.base.runnable import Input, Output
from kag.interface.builder import ExtractorABC


class UserDefinedExtractor(ExtractorABC):
    @property
    def input_types(self) -> Input:
        return Dict[str, str]

    @property
    def output_types(self) -> Output:
        return Dict[str, str]

    def invoke(self, input: Input, **kwargs) -> List[Output]:
        return input
