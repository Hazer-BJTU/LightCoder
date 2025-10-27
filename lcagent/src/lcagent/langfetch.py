import os
import sys
import toml
import logging
import logging.config

from typing import Dict, Any


LOGGER: Any = None
MODULE_DIR: str = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH: str = os.path.join(MODULE_DIR, 'configs', 'langfetch.toml')

def initialize_logger(log_configs: Dict[str, Any]) -> None:
    global LOGGER
    if LOGGER is None:
        try:
            logging.config.dictConfig(log_configs)
            config_succeeded = True
        except Exception as e:
            config_succeeded = False
        LOGGER = logging.getLogger(__name__)
        if not config_succeeded:
            LOGGER.warning(f"Invalid logging configurations: {e}.") #type: ignore
        try:
            with open(log_configs['handlers']['fileHandler']['filename'], 'w', encoding='utf-8') as clean_file:
                pass
        except Exception:
            pass

class LangFetcher:
    DEFAULT_ERROR_MESSAGE: str = "DEFAULT_ERROR_MESSAGE"

    def __init__(self, config_file_path: str):
        try:
            with open(config_file_path, 'r', encoding='utf-8') as config_file:
                configs: Dict[str, Any] = toml.loads(config_file.read())
            self.raw_configs: Dict[str, Any] = configs
            self.logging_configs: Dict[str, Any] = configs['logging_configs']
            self.supported: Dict[str, Any] = configs['supported']
            self.groups: Dict[str, Any] = configs['groups']
            self.lang: str = next(iter(self.supported.values()))
            assert self.lang is not None, 'No language supported.'
            initialize_logger(self.logging_configs)
        except Exception as e:
            print(f"An exception has occurred when reading from the config file: {e}.") #type: ignore
            sys.exit(1)

    def __call__(self, key: str, lang: str | None = None) -> str:
        try:
            if lang is None:
                lang = self.lang
            elif lang in self.supported:
                lang = self.supported[lang]
            return self.groups[key][lang]
        except Exception as e:
            LOGGER.error(f"An exception has occurred when fetching the text: {e}.") #type: ignore
            return LangFetcher.DEFAULT_ERROR_MESSAGE
        
    def set_lang(self, lang: str) -> None:
        if lang in self.supported:
            self.lang = self.supported[lang]
        elif lang in self.supported.values():
            self.lang = lang
        else:
            LOGGER.warning(f"Unsupported language: {lang}.") #type: ignore

    def get_supported(self) -> Dict[str, str]:
        return self.supported

langfetcher = LangFetcher(CONFIG_FILE_PATH)

if __name__ == '__main__':
    # _ = langfetcher
    # _.set_lang('simplified_chinese')
    # print(_('test0'))
    # print(_.get_supported())
    pass
