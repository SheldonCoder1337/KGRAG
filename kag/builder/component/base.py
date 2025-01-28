import os
from abc import ABC
from typing import List, Dict
import logging

from knext.common.base.component import Component
from knext.common.base.runnable import Input, Output
from knext.project.client import ProjectClient
from kag.common.llm.client import LLMClient


class BuilderComponent(Component, ABC):
    """
    Abstract base class for all builder component.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.project_id = kwargs.get("project_id",None) or os.getenv("KAG_PROJECT_ID")
        self.config = ProjectClient().get_config(self.project_id)


    def _init_llm(self) -> LLMClient:
        """
        Initializes the Large Language Model (LLM) client.

        This method retrieves the LLM configuration from environment variables and the project ID.
        It then fetches the project configuration using the project ID and updates the LLM configuration
        with any additional settings from the project. Finally, it creates and initializes the LLM client
        using the updated configuration.

        Args:
            None

        Returns:
            LLMClient
        """
        llm_config = eval(os.getenv("KAG_LLM", "{}"))
        project_id = self.project_id or os.getenv("KAG_PROJECT_ID")
        if project_id:
            try:
                config = ProjectClient().get_config(project_id)
                llm_config.update(config.get("llm", {}))
            except:
                logging.warning(
                    f"Failed to get project config for project id: {project_id}"
                )
        llm = LLMClient.from_config(llm_config)
        return llm

    @property
    def type(self):
        """
        Get the type label of the object.

        Returns:
            str: The type label of the object, fixed as "BUILDER".
        """
        return "BUILDER"

    def batch(self, inputs: List[Input], **kwargs) -> List[Output]:
        results = []
        for input in inputs:
            results.extend(self.invoke(input, **kwargs))
        return results

    def _handle(self, input: Dict) -> List[Dict]:
        _input = self.input_types.from_dict(input) if isinstance(input, dict) else input
        _output = self.invoke(_input)
        return [_o.to_dict() for _o in _output if _o]
