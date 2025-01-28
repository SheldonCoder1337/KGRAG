import json
from typing import Optional, List

from kag.common.base.prompt_op import PromptOp

class OpenIEEntitystandardizationdPrompt(PromptOp):

    """
    Entity standardization Prompt Task
    """

    template_zh = """
{
    "instruction": "input字段包含用户提供的上下文。命名实体字段包含从上下文中提取的命名实体，这些可能是含义不明的缩写、别名或俚语。为了消除歧义，请尝试根据上下文和您自己的知识提供这些实体的官方名称。请注意，具有相同含义的实体只能有一个官方名称。请按照提供的示例中的输出字段格式，以单个JSONArray字符串形式回复，无需任何解释。",
    "example": {
        "input": "外风证是指感受外界风邪（其中可能包含着某些生物性致病因素，如风毒等）为病，以汗出、恶风、脉浮缓，或咳嗽、咽痒、鼻塞、喷嚏，或皮肤瘙痒、丘疹、麻木不仁、口眼歪斜、肢体抽搐为常见症的证候。常见于感冒、咳嗽、瘾疹、中风等疾病。典型症状：恶风发热、汗出、脉浮缓；咳嗽、咽痒、鼻塞或喷嚏；皮肤瘙痒、突起风团，麻木不仁、口眼歪斜、颈项拘急、口噤不开、肢体抽搐；肢体关节游走疼痛、面睑浮肿。常见疾病：感冒、咳嗽\n\n多由风邪与当令之时气相挟而伤人，以风寒、风热、风燥多见，而致卫表不和，肺失宣肃。风燥证，症见干咳，连声作呛，喉痒咽干鼻燥，无痰或痰少而粘连成丝，不易咯出，初起或伴鼻塞，头痛，发热，恶寒，汗出或无汗等，舌苔薄白或薄黄，干而少津，脉浮数或浮缓，治宜硫凤清肺，润燥止咳，方用桑杏汤（《温病条辨》）加麦冬、玉竹，或用杏苏散（《温病条辨》）加紫菀、款冬、百部荆芥、防风。",
        "named_entities": [
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
        ],
        "output": [
            {"entity": "外风证", "category": "Syndrome", "official_name": "外风证"},
            {"entity": "汗出", "category": "Symptom", "official_name": "汗出"},
            {"entity": "恶风", "category": "Symptom", "official_name": "恶风"},
            {"entity": "脉浮缓", "category": "Symptom", "official_name": "脉浮缓"},
            {"entity": "咳嗽", "category": "Symptom", "official_name": "咳嗽"},
            {"entity": "咽痒", "category": "Symptom", "official_name": "咽痒"},
            {"entity": "鼻塞", "category": "Symptom", "official_name": "鼻塞"},
            {"entity": "喷嚏", "category": "Symptom", "official_name": "喷嚏"},
            {"entity": "皮肤瘙痒", "category": "Symptom", "official_name": "皮肤瘙痒"},
            {"entity": "丘疹", "category": "Symptom", "official_name": "丘疹"},
            {"entity": "麻木不仁", "category": "Symptom", "official_name": "麻木不仁"},
            {"entity": "口眼歪斜", "category": "Symptom", "official_name": "口眼歪斜"},
            {"entity": "肢体抽搐", "category": "Symptom", "official_name": "肢体抽搐"},
            {"entity": "感冒", "category": "Disease", "official_name": "感冒"},
            {"entity": "咳嗽", "category": "Disease", "official_name": "咳嗽病"},
            {"entity": "瘾疹", "category": "Disease", "official_name": "瘾疹"},
            {"entity": "中风", "category": "Disease", "official_name": "中风"},
            {"entity": "恶风发热", "category": "Symptom", "official_name": "恶风发热"},
            {"entity": "突起风团", "category": "Symptom", "official_name": "突起风团"},
            {"entity": "颈项拘急", "category": "Symptom", "official_name": "颈项拘急"},
            {"entity": "口噤不开", "category": "Symptom", "official_name": "口噤不开"},
            {"entity": "肢体关节游走疼痛", "category": "Symptom", "official_name": "肢体关节游走疼痛"},
            {"entity": "面睑浮肿", "category": "Symptom", "official_name": "面睑浮肿"},
            {"entity": "卫表不和", "category": "pathogenesis", "official_name": "卫表不和"},
            {"entity": "肺失宣肃", "category": "pathogenesis", "official_name": "肺失宣肃"},
            {"entity": "风燥证", "category": "Syndrome", "official_name": "风燥证"},
            {"entity": "干咳", "category": "Symptom", "official_name": "干咳"},
            {"entity": "连声作呛", "category": "Symptom", "official_name": "连声作呛"},
            {"entity": "喉痒咽干鼻燥", "category": "Symptom", "official_name": "喉痒咽干鼻燥"},
            {"entity": "无痰或痰少而粘连成丝", "category": "Symptom", "official_name": "无痰或痰少而粘连成丝"},
            {"entity": "不易咯出", "category": "Symptom", "official_name": "不易咯出"},
            {"entity": "舌苔薄白或薄黄", "category": "Symptom", "official_name": "舌苔薄白或薄黄"},
            {"entity": "干而少津", "category": "Symptom", "official_name": "干而少津"},
            {"entity": "脉浮数或浮缓", "category": "Symptom", "official_name": "脉浮数或浮缓"},
            {"entity": "疏风清肺", "category": "Treatment", "official_name": "疏风清肺"},
            {"entity": "润燥止咳", "category": "Treatment", "official_name": "润燥止咳"},
            {"entity": "桑杏汤", "category": "Prescription", "official_name": "桑杏汤"},
            {"entity": "《温病条辨》", "category": "Literature", "official_name": "《温病条辨》"},
            {"entity": "麦冬", "category": "Herbs", "official_name": "麦冬"},
            {"entity": "玉竹", "category": "Herbs", "official_name": "玉竹"},
            {"entity": "杏苏散", "category": "Prescription", "official_name": "杏苏散"},
            {"entity": "紫菀", "category": "Herbs", "official_name": "紫菀"},
            {"entity": "款冬", "category": "Herbs", "official_name": "款冬"},
            {"entity": "百部", "category": "Herbs", "official_name": "百部"},
            {"entity": "荆芥", "category": "Herbs", "official_name": "荆芥"},
            {"entity": "防风", "category": "Herbs", "official_name": "防风"}
        ]
    },
    "input": $input,
    "named_entities": $named_entities,
}    
    """

    template_en = template_zh

    def __init__(self, language: Optional[str] = "en"):
        super().__init__(language)

    @property
    def template_variables(self) -> List[str]:
        return ["input", "named_entities"]

    def parse_response(self, response: str, **kwargs):

        rsp = response
        if isinstance(rsp, str):
            rsp = json.loads(rsp)
        if isinstance(rsp, dict) and "output" in rsp:
            rsp = rsp["output"]
        if isinstance(rsp, dict) and "named_entities" in rsp:
            standardized_entity = rsp["named_entities"]
        else:
            standardized_entity = rsp
        entities_with_offical_name = set()
        merged = []
        entities = kwargs.get("named_entities", [])
        for entity in standardized_entity:
            merged.append(entity)
            entities_with_offical_name.add(entity["entity"])
        # in case llm ignores some entities
        for entity in entities:
            if entity["entity"] not in entities_with_offical_name:
                entity["official_name"] = entity["entity"]
                merged.append(entity)
        return merged
