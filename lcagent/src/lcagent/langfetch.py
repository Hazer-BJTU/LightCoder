import os
import sys
import toml
import logging
import logging.config

from typing import Dict, Any


MODULE_DIR: str = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH: str = os.path.join(MODULE_DIR, 'configs', 'langfetch.toml')

def initialize_logger(logger_name: str, config_file_path: str = CONFIG_FILE_PATH) -> logging.Logger:
    if not hasattr(initialize_logger, 'executed'):
        try:
            with open(config_file_path, 'r', encoding='utf-8') as config_file:
                configs: Dict[str, Any] = toml.loads(config_file.read())
                logging_configs = configs['logging_configs']
            logging.config.dictConfig(logging_configs)
        except Exception as e:
            print(f"(Warning): Failed to load logging configurations: {e}.")
        initialize_logger.executed = True #type: ignore
    return logging.getLogger(logger_name)

LOGGER: logging.Logger = initialize_logger(__name__)

class LangFetcher:
    DEFAULT_ERROR_MESSAGE: str = "DEFAULT_ERROR_MESSAGE"

    def __init__(self, config_file_path: str):
        try:
            with open(config_file_path, 'r', encoding='utf-8') as config_file:
                configs: Dict[str, Any] = toml.loads(config_file.read())
            self.raw_configs: Dict[str, Any] = configs
            self.supported: Dict[str, Any] = configs['supported']
            self.groups: Dict[str, Any] = configs['groups']
            self.lang: str = next(iter(self.supported.values()))
            assert self.lang is not None, 'No language supported.'
        except Exception as e:
            print(f"(Critical): An exception has occurred when reading from the config file: {e}.")
            sys.exit(1)

    def __call__(self, key: str, lang: str | None = None) -> str:
        try:
            if lang is None:
                lang = self.lang
            elif lang in self.supported:
                lang = self.supported[lang]
            return self.groups[key][lang]
        except Exception as e:
            LOGGER.error(f"An exception has occurred when fetching the text: {e}.")
            return LangFetcher.DEFAULT_ERROR_MESSAGE
        
    def set_lang(self, lang: str) -> None:
        if lang in self.supported:
            self.lang = self.supported[lang]
        elif lang in self.supported.values():
            self.lang = lang
        else:
            LOGGER.warning(f"Unsupported language: {lang}.")

    def get_supported(self) -> Dict[str, str]:
        return self.supported

langfetcher = LangFetcher(CONFIG_FILE_PATH)

if __name__ == '__main__':
    # _ = langfetcher
    # _.set_lang('simplified_chinese')
    # print(_('test0'))
    # print(_.get_supported())
    pass
