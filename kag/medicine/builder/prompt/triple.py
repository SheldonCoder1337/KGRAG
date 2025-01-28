

import json
from typing import Optional, List

from kag.common.base.prompt_op import PromptOp


class OpenIETriplePrompt(PromptOp):

    template_zh = """
{
    "instruction": "您是一位专门从事开放信息提取（OpenIE）的专家。请从input字段的文本中提取任何可能的关系（包括主语、谓语、宾语），并按照JSON格式列出它们，须遵循example字段的示例格式。请注意以下要求：1. 每个三元组应至少包含entity_list实体列表中的一个，但最好是两个命名实体。2. 明确地将代词解析为特定名称，以保持清晰度。",
    "entity_list": $entity_list,
    "input": "$input",
    "example": {
        "input": "外风证是指感受外界风邪（其中可能包含着某些生物性致病因素，如风毒等）为病，以汗出、恶风、脉浮缓，或咳嗽、咽痒、鼻塞、喷嚏，或皮肤瘙痒、丘疹、麻木不仁、口眼歪斜、肢体抽搐为常见症的证候。常见于感冒、咳嗽、瘾疹、中风等疾病。典型症状：恶风发热、汗出、脉浮缓；咳嗽、咽痒、鼻塞或喷嚏；皮肤瘙痒、突起风团，麻木不仁、口眼歪斜、颈项拘急、口噤不开、肢体抽搐；肢体关节游走疼痛、面睑浮肿。常见疾病：感冒、咳嗽\n\n多由风邪与当令之时气相挟而伤人，以风寒、风热、风燥多见，而致卫表不和，肺失宣肃。风燥证，症见干咳，连声作呛，喉痒咽干鼻燥，无痰或痰少而粘连成丝，不易咯出，初起或伴鼻塞，头痛，发热，恶寒，汗出或无汗等，舌苔薄白或薄黄，干而少津，脉浮数或浮缓，治宜硫凤清肺，润燥止咳，方用桑杏汤（《温病条辨》）加麦冬、玉竹，或用杏苏散（《温病条辨》）加紫菀、款冬、百部荆芥、防风。",
        "entity_list": [
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
            {"entity": "咳嗽病", "category": "Disease"},
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
        "output":[
            ["外风证", "常见症状", "汗出"],
            ["外风证", "常见症状", "恶风"],
            ["外风证", "常见症状", "脉浮缓"],
            ["外风证", "常见症状", "咳嗽"],
            ["外风证", "常见症状", "咽痒"],
            ["外风证", "常见症状", "鼻塞"],
            ["外风证", "常见症状", "喷嚏"],
            ["外风证", "常见症状", "皮肤瘙痒"],
            ["外风证", "常见症状", "丘疹"],
            ["外风证", "常见症状", "麻木不仁"],
            ["外风证", "常见症状", "口眼歪斜"],
            ["外风证", "常见症状", "肢体抽搐"],
            ["外风证", "常见疾病", "感冒"],
            ["外风证", "常见疾病", "咳嗽病"],
            ["外风证", "常见疾病", "瘾疹"],
            ["外风证", "常见疾病", "中风"],
            ["外风证", "典型症状", "恶风发热"],
            ["外风证", "典型症状", "汗出"],
            ["外风证", "典型症状", "脉浮缓"],
            ["外风证", "典型症状", "咳嗽"],
            ["外风证", "典型症状", "咽痒"],
            ["外风证", "典型症状", "鼻塞或喷嚏"],
            ["外风证", "典型症状", "皮肤瘙痒"],
            ["外风证", "典型症状", "突起风团"],
            ["外风证", "典型症状", "麻木不仁"],
            ["外风证", "典型症状", "口眼歪斜"],
            ["外风证", "典型症状", "颈项拘急"],
            ["外风证", "典型症状", "口噤不开"],
            ["外风证", "典型症状", "肢体抽搐"],
            ["外风证", "典型症状", "肢体关节游走疼痛"],
            ["外风证", "典型症状", "面睑浮肿"],
            ["外风证", "致病因素", "风邪与当令之时气相挟"],
            ["外风证", "病理机制", "卫表不和"],
            ["外风证", "病理机制", "肺失宣肃"],
            ["感冒", "常见证候", "风寒证"],
            ["感冒", "常见证候", "风热证"],
            ["感冒", "常见证候", "风燥证"],
            ["风燥证", "常见症状", "干咳"],
            ["风燥证", "常见症状", "连声作呛"],
            ["风燥证", "常见症状", "喉痒咽干鼻燥"],
            ["风燥证", "常见症状", "无痰或痰少而粘连成丝"],
            ["风燥证", "常见症状", "不易咯出"],
            ["风燥证", "常见症状", "舌苔薄白或薄黄"],
            ["风燥证", "常见症状", "干而少津"],
            ["风燥证", "常见症状", "脉浮数或浮缓"],
            ["风燥证", "治疗方法", "疏风清肺"],
            ["风燥证", "治疗方法", "润燥止咳"],
            ["桑杏汤", "出自", "《温病条辨》"],
            ["桑杏汤", "加药", "麦冬"],
            ["桑杏汤", "加药", "玉竹"],
            ["杏苏散", "出自", "《温病条辨》"],
            ["杏苏散", "加药", "紫菀"],
            ["杏苏散", "加药", "款冬"],
            ["杏苏散", "加药", "百部"],
            ["杏苏散", "加药", "荆芥"],
            ["杏苏散", "加药", "防风"]
        ]
    }
}    
    """

    template_en = template_zh

    def __init__(self, language: Optional[str] = "en"):
        super().__init__(language)

    @property
    def template_variables(self) -> List[str]:
        return ["entity_list", "input"]

    def parse_response(self, response: str, **kwargs):
        rsp = response
        if isinstance(rsp, str):
            rsp = json.loads(rsp)
        if isinstance(rsp, dict) and "output" in rsp:
            rsp = rsp["output"]
        if isinstance(rsp, dict) and "triples" in rsp:
            triples = rsp["triples"]
        else:
            triples = rsp

        standardized_triples = []
        for triple in triples:
            if isinstance(triple, list):
                standardized_triples.append(triple)
            elif isinstance(triple, dict):
                s = triple.get("subject")
                p = triple.get("predicate")
                o = triple.get("object")
                if s and p and o:
                    standardized_triples.append([s, p, o])

        return standardized_triples
