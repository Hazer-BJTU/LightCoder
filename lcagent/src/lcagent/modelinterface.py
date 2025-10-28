import os
import toml
import copy

from openai import OpenAI
from typing import Dict, Optional, Tuple
from lcagent.langfetch import initialize_logger


MODULE_DIR: str = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH: str = os.path.join(MODULE_DIR, 'configs', 'modelinterface.toml')
LOGGER = initialize_logger(__name__)

API_POOL: Dict[str, Tuple[OpenAI, Dict]] = {}

with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config_file:
    SUPPORTED_MODELS = toml.loads(config_file.read())

def get_client(name: str) -> Tuple[Optional[OpenAI], Dict]:
    get_client.DEFAULT_ERROR_MESSAGE = (None, {'MODEL_NOT_SUPPORTED': True}) #type: ignore
    if name in API_POOL:
        return API_POOL[name]
    else:
        if name in SUPPORTED_MODELS:
            try:
                model_configs: Dict = copy.deepcopy(SUPPORTED_MODELS[name])
                api_default_configs = model_configs.pop('api_default_configs')
                base_url = api_default_configs['base-url']
                if 'api-key' not in api_default_configs or api_default_configs['api-key'] == '<your api here>':
                    api_key = os.getenv(api_default_configs['api-key-env'])
                else:
                    api_key = api_default_configs['api-key']
                API_POOL[name] = OpenAI(base_url=base_url, api_key=api_key), model_configs
                return API_POOL[name]
            except Exception as e:
                LOGGER.warning(f'Unsupported model specified: {name} or an error has occurred: {e}.')
                return get_client.DEFAULT_ERROR_MESSAGE #type: ignore
        else:
            LOGGER.warning(f'Unsupported model specified: {name}.')
            return get_client.DEFAULT_ERROR_MESSAGE #type: ignore
        

if __name__ == '__main__':
    """
    test_messages = [{'role': 'user', 'content': '请简要介绍一下你自己。'}]
    client, extra_configs = get_model_api('deepseek-chat')
    input = extra_configs['completion_default_configs']
    input['messages'] = test_messages
    if client is not None:
        response = client.chat.completions.create(**input)
        response = response.choices[0].message
        print(response)
    """
    pass
