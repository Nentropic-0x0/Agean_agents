'''
Configuratio and other utilities

'''
import os
from typing import Dict, Optional, Tuple

import yaml
from dotenv import find_dotenv, load_dotenv


def get_api_keys(service):
    if os.path.exists('.env'):
        load_dotenv(find_dotenv())
        api_key = os.getenv(f"{service}_API_KEY")
        return api_key
    else:
        api_key = os.getenv(f"{service}_API_KEY")
        return api_key

def get_config() -> Dict:
    api_key = get_api_keys(service="OPENAI")
    
    with open("agent_config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
        #humanloop_settings = config['humanloop']