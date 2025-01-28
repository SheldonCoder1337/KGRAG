

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
from ollama import Client

import requests
import traceback
from Crypto.Cipher import AES
from requests import RequestException

from kag.common import arks_pb2
from kag.common.base.prompt_op import PromptOp
from kag.common.llm.config import OllamaConfig

from kag.common.llm.client.llm_client import LLMClient


# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OllamaClient(LLMClient):
    def __init__(self, llm_config: OllamaConfig):
        self.model = llm_config.model
        self.base_url = llm_config.base_url
        self.param = {}
        self.client = Client(host=self.base_url)

    def sync_request(self, prompt,image=None):
        # import pdb; pdb.set_trace()
        response = self.client.generate(model=self.model, prompt=prompt, stream=False)
        content = response["response"]
        content = content.replace("&rdquo;", "”").replace("&ldquo;", "“")
        content = content.replace("&middot;", "")

        return content

    def __call__(self, prompt,image=None):
        return self.sync_request(prompt,image)

    def call_with_json_parse(self, prompt):
        rsp = self.sync_request(prompt)
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
