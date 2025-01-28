#


import json
import logging

from kag.common.base.prompt_op import PromptOp

logger = logging.getLogger(__name__)




class AnalyzeTablePrompt(PromptOp):
    template_zh: str = """你是一个分析表格的专家, 从table中提取信息并分析，最后返回表格有效信息"""
    template_en: str = """You are an expert in knowledge graph extraction. Based on the schema defined by the constraint, extract all entities and their attributes from the input. Return NAN for attributes not explicitly mentioned in the input. Output the results in standard JSON format, as a list."""

    def __init__(
        self,
        language: str = "zh",
    ):
        super().__init__(
            language=language,
        )

    def build_prompt(self, variables) -> str:
        return json.dumps(
            {
                "instruction": self.template,
                "table": variables.get("table",""),
            },
            ensure_ascii=False,
        )

    def parse_response(self, response: str, **kwargs):
        return response

