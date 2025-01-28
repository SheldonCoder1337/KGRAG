

import json


class LLMConfigChecker(object):
    """
    Check whether the llm config is valid.
    """

    def check(self, config: str) -> str:
        """
        Check the llm config.

        * If the config is valid, return the generated text.

        * If the config is invalid, raise a RuntimeError exception.

        :param config: llm config
        :type config: str
        :return: the generated text
        :rtype: str
        :raises RuntimeError: if the config is invalid
        """
        from kag.common.llm.client import LLMClient
        config = json.loads(config)
        llm_client = LLMClient.from_config(config)
        try:
            res = llm_client("who are you?")
            return res
        except Exception as ex:
            raise RuntimeError(f"invalid llm config: {config}, for details: {ex}")
        
if __name__ == "__main__":
    config = '''
        {"client_type" :"ollama",
        "base_url" : "http://localhost:11434/",
        "model" : "llama3.1" }
    '''
    config_checker = LLMConfigChecker()
    res = config_checker.check(config)
