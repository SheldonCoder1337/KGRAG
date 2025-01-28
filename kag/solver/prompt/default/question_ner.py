

import json
from string import Template
from typing import List, Optional

from kag.common.base.prompt_op import PromptOp
from knext.reasoner.client import ReasonerClient


class QuestionNER(PromptOp):

    template_en = """
    {
        "instruction": "You are an expert in named entity recognition. Please extract entities and that match the schema definition from the input. Return an empty list if the entity type does not exist. Please respond in the format of a JSON string.You can refer to the example for extraction.",
        "schema": $schema,
        "example": [
            {
                "input": "Which magazine was started first, Arthur's Magazine or First for Women?",
                "output": [
                        {
                            "entity": "First for Women",
                            "category": "Works"
                        },
                        {
                            "entity": "Arthur's Magazine",
                            "category": "Works"
                        }
                    ]
            }
        ],
        "input": "$input"
    }    
        """

    template_zh = template_en

    def __init__(
            self, language: Optional[str] = "en", **kwargs
    ):
        super().__init__(language, **kwargs)
        self.schema = list(ReasonerClient(project_id=self.project_id).get_reason_schema().keys())
        self.template = Template(self.template).safe_substitute(schema=self.schema)

    @property
    def template_variables(self) -> List[str]:
        return ["input"]

    def parse_response(self, response: str, **kwargs):
        rsp = response
        if isinstance(rsp, str):
            rsp = json.loads(rsp)
        if isinstance(rsp, dict) and "output" in rsp:
            rsp = rsp["output"]
        if isinstance(rsp, dict) and "named_entities" in rsp:
            entities = rsp["named_entities"]
        else:
            entities = rsp

        return entities
