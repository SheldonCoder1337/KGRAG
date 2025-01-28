import json
from string import Template
from typing import List, Optional

from kag.common.base.prompt_op import PromptOp
from knext.schema.client import SchemaClient


class QuestionNER(PromptOp):

    template_zh = """
{
    "instruction": "你是命名实体识别的专家。请从输入中提取与模式定义匹配的实体。如果不存在该类型的实体，请返回一个空列表。请以JSON字符串格式回应。你可以参照example进行抽取。",
    "schema": $schema,
    "example": [
        {
            "input": "患者男，40岁，工作。2月8日初诊。主诉：鼻塞，流涕4天，发热、恶寒、头痛2天。病史：2月4日上班时因天气突变而衣着单薄感寒，自感恶寒，鼻塞流清涕，稍咳，喷嚏，头痛，因工作繁忙未介意。昨起发热汗出，微恶寒，头胀痛，鼻塞流浊涕，口渴喜饮，咽喉疼痛，咳嗽咯黄稠痰，小便黄。辅助检查：体温39.8°C。咽部充血，扁桃体Ⅱ度肿大，无脓点。舌苔薄黄，脉浮数。中医辩证应该是：\nA.感冒,风热证,疏风解表，清热解毒,银翘散 \nB.感冒,风寒证,辛温解表，宣肺散寒,桂枝汤",
            "output": [
                    {"entity": "鼻塞", "category": "Symptom"},
                    {"entity": "流涕", "category": "Symptom"},
                    {"entity": "发热", "category": "Symptom"},
                    {"entity": "恶寒", "category": "Symptom"},
                    {"entity": "头痛", "category": "Symptom"},
                    {"entity": "鼻塞流清涕", "category": "Symptom"},
                    {"entity": "稍咳", "category": "Symptom"},
                    {"entity": "喷嚏", "category": "Symptom"},
                    {"entity": "发热汗出", "category": "Symptom"},
                    {"entity": "微恶寒", "category": "Symptom"},
                    {"entity": "头胀痛", "category": "Symptom"},
                    {"entity": "鼻塞流浊涕", "category": "Symptom"},
                    {"entity": "口渴喜饮", "category": "Symptom"},
                    {"entity": "咽喉疼痛", "category": "Symptom"},
                    {"entity": "咳嗽咯黄稠痰", "category": "Symptom"},
                    {"entity": "小便黄", "category": "Symptom"},
                    {"entity": "体温39.8°C", "category": "ExaminationTest"},
                    {"entity": "咽部充血", "category": "ExaminationTest"},
                    {"entity": "扁桃体Ⅱ度肿大", "category": "ExaminationTest"},
                    {"entity": "舌苔薄黄", "category": "ExaminationTest"},
                    {"entity": "脉浮数", "category": "ExaminationTest"},
                    {"entity": "感冒", "category": "Disease"},
                    {"entity": "风热证", "category": "Syndrome"},
                    {"entity": "风寒证", "category": "Syndrome"}
                    {"entity": "辛温解表", "category": "Treatment"},
                    {"entity": "宣肺散寒", "category": "Treatment"},
                    {"entity": "疏风解表", "category": "Treatment"},
                    {"entity": "清热解毒", "category": "Treatment"},
                    {"entity": "银翘散", "category": "Prescription"},
                    {"entity": "桂枝汤", "category": "Prescription"}
                ]
        }
    ],
    "input": "$input"
}    
    """

    template_en = template_zh

    def __init__(
            self, language: Optional[str] = "en", **kwargs
    ):
        super().__init__(language, **kwargs)
        self.schema = SchemaClient(project_id=self.project_id).extract_types()
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
