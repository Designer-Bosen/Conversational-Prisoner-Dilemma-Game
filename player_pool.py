#####################
## === Imports === ##
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import os


load_dotenv()
## Load Key from Environment
def get_key(API_key):
    key = os.getenv(API_key)
    if key is None:
        raise ValueError(f"KEY FAILED: {API_key}")
    return key

############################
## === LLM Agent Pool === ##
## Agent ID start with 0
agent_pool = {
    "000": {"provider": "openai", "model": "gpt-5.4", "client": OpenAI(api_key=get_key("OPENAI_API_KEY_0"))},
    "001": {"provider": "openai", "model": "gpt-5.4", "client": OpenAI(api_key=get_key("OPENAI_API_KEY_1"))},
    "002": {"provider": "openai", "model": "gpt-5.4", "client": OpenAI(api_key=get_key("OPENAI_API_KEY_2"))},
    "003": {"provider": "openai", "model": "gpt-5.4", "client": OpenAI(api_key=get_key("OPENAI_API_KEY_3"))},
}


###############################
## === Human Player Pool === ##
## Human ID start with 1
human_pool = {
    "100": {},
    "101": {},
    "102": {}
}
