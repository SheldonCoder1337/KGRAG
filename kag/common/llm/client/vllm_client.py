

import os
import ast
import re
import json
import time
import uuid
import html
from binascii import b2a_hex
from datetime import datetime
from pathlib import Path
from typing import Union, Dict, List, Any
from urllib import request
from collections import defaultdict

from openai import OpenAI
import logging

import requests
import traceback
from Crypto.Cipher import AES
from requests import RequestException

from kag.common import arks_pb2
from kag.common.base.prompt_op import PromptOp
from kag.common.llm.config import VLLMConfig

from kag.common.llm.client.llm_client import LLMClient


# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VLLMClient(LLMClient):
    def __init__(self, llm_config: VLLMConfig):
        self.model = llm_config.model
        self.base_url = llm_config.base_url
        self.param = {}

    def sync_request(self, prompt):
        # import pdb; pdb.set_trace()
        self.param["messages"] = prompt
        self.param["model"] = self.model

        response = requests.post(
            self.base_url,
            data=json.dumps(self.param),
            headers={"Content-Type": "application/json"},
        )

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        content = content.replace("&rdquo;", "”").replace("&ldquo;", "“")
        content = content.replace("&middot;", "")
        return content

    def __call__(self, prompt):
        content = [
          {"role": "user", "content": prompt}
          ]
        return self.sync_request(content)

    def call_with_json_parse(self, prompt):
        content = [{"role": "user", "content": prompt}]
        rsp = self.sync_request(content)
        _end = rsp.rfind("```")
        _start = rsp.find("```json")
        if _end != -1 and _start != -1:
            json_str = rsp[_start + len("```json"): _end].strip()
        else:
            json_str = rsp
        try:
            json_result = json.loads(json_str)
        except:
            return rsp
        return json_result
