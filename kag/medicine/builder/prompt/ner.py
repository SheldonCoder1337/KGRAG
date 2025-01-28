import json
from string import Template
from typing import List, Optional

from kag.common.base.prompt_op import PromptOp
from knext.schema.client import SchemaClient

class OpenIENERPrompt(PromptOp):
    """
    Name Entity Recognition Prompt Task
    """
    template_zh = """
    {
        "instruction": "你是命名实体识别的专家。请从输入中提取与模式定义匹配的实体。如果不存在该类型的实体，请返回一个空列表。请以JSON字符串格式回应。你可以参照example进行抽取。",
        "schema": $schema,
        "example": [
            {
                "input": "外风证是指感受外界风邪（其中可能包含着某些生物性致病因素，如风毒等）为病，以汗出、恶风、脉浮缓，或咳嗽、咽痒、鼻塞、喷嚏，或皮肤瘙痒、丘疹、麻木不仁、口眼歪斜、肢体抽搐为常见症的证候。常见于感冒、咳嗽、瘾疹、中风等疾病。典型症状：恶风发热、汗出、脉浮缓；咳嗽、咽痒、鼻塞或喷嚏；皮肤瘙痒、突起风团，麻木不仁、口眼歪斜、颈项拘急、口噤不开、肢体抽搐；肢体关节游走疼痛、面睑浮肿。常见疾病：感冒、咳嗽\n\n多由风邪与当令之时气相挟而伤人，以风寒、风热、风燥多见，而致卫表不和，肺失宣肃。风燥证，症见干咳，连声作呛，喉痒咽干鼻燥，无痰或痰少而粘连成丝，不易咯出，初起或伴鼻塞，头痛，发热，恶寒，汗出或无汗等，舌苔薄白或薄黄，干而少津，脉浮数或浮缓，治宜硫凤清肺，润燥止咳，方用桑杏汤（《温病条辨》）加麦冬、玉竹，或用杏苏散（《温病条辨》）加紫菀、款冬、百部荆芥、防风。",
                "output": [
                        {"entity": "外风证", "category": "Syndrome"},
                        {"entity": "汗出", "category": "Symptom"},
                        {"entity": "恶风", "category": "Symptom"},
                        {"entity": "脉浮缓", "category": "Symptom"},
                        {"entity": "咳嗽", "category": "Symptom"},
                        {"entity": "咽痒", "category": "Symptom"},
                        {"entity": "鼻塞", "category": "Symptom"},
                        {"entity": "喷嚏", "category": "Symptom"},
                        {"entity": "皮肤瘙痒", "category": "Symptom"},
                        {"entity": "丘疹", "category": "Symptom"},
                        {"entity": "麻木不仁", "category": "Symptom"},
                        {"entity": "口眼歪斜", "category": "Symptom"},
                        {"entity": "肢体抽搐", "category": "Symptom"},
                        {"entity": "感冒", "category": "Disease"},
                        {"entity": "咳嗽", "category": "Disease"},
                        {"entity": "瘾疹", "category": "Disease"},
                        {"entity": "中风", "category": "Disease"},
                        {"entity": "恶风发热", "category": "Symptom"},
                        {"entity": "突起风团", "category": "Symptom"},
                        {"entity": "颈项拘急", "category": "Symptom"},
                        {"entity": "口噤不开", "category": "Symptom"},
                        {"entity": "肢体关节游走疼痛", "category": "Symptom"},
                        {"entity": "面睑浮肿", "category": "Symptom"},
                        {"entity": "卫表不和", "category": "pathogenesis"},
                        {"entity": "肺失宣肃", "category": "pathogenesis"},
                        {"entity": "风燥证", "category": "Syndrome"},
                        {"entity": "干咳", "category": "Symptom"},
                        {"entity": "连声作呛", "category": "Symptom"},
                        {"entity": "喉痒咽干鼻燥", "category": "Symptom"},
                        {"entity": "无痰或痰少而粘连成丝", "category": "Symptom"},
                        {"entity": "不易咯出", "category": "Symptom"},
                        {"entity": "舌苔薄白或薄黄", "category": "Symptom"},
                        {"entity": "干而少津", "category": "Symptom"},
                        {"entity": "脉浮数或浮缓", "category": "Symptom"},
                        {"entity": "疏风清肺", "category": "Treatment"},
                        {"entity": "润燥止咳", "category": "Treatment"},
                        {"entity": "桑杏汤", "category": "Prescription"},
                        {"entity": "《温病条辨》", "category": "Literature"},
                        {"entity": "麦冬", "category": "Herbs"},
                        {"entity": "玉竹", "category": "Herbs"},
                        {"entity": "杏苏散", "category": "Prescription"},
                        {"entity": "紫菀", "category": "Herbs"},
                        {"entity": "款冬", "category": "Herbs"},
                        {"entity": "百部", "category": "Herbs"},
                        {"entity": "荆芥", "category": "Herbs"},
                        {"entity": "防风", "category": "Herbs"}
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
