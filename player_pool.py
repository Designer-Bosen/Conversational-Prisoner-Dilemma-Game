#####################
## === Imports === ##
from openai import OpenAI
from anthropic import Anthropic




#################################
## === LLM agents API keys === ##
## (highly private if filled in,  beware!)

# Those keys are filled, just to make it secret
key0 = ""
key1 = ""
key2 = ""

############################
## === LLM Agent Pool === ##
## Agent ID start with 0
agent_pool = {
    "000": {"provider": "openai", "model": "gpt-5.4", "client": OpenAI(api_key=key0), "history": []},
    "001": {"provider": "openai", "model": "gpt-5.4", "client": OpenAI(api_key=key1), "history": []},
    "002": {"provider": "openai", "model": "gpt-5.4", "client": OpenAI(api_key=key2), "history": []},
}


###############################
## === Human Player Pool === ##
## Human ID start with 1
human_pool = {
    "100": {"id": "0000", "history": []},
    "101": {"id": "0001", "history": []},
    "102": {"id": "0001", "history": []}
}
