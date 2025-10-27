import os
import json

from pathlib import Path
from typing import Dict, Callable, Optional
from lcagent.langfetch import initialize_logger


LOGGER = initialize_logger(__file__)

def fetch_project_file_structure_function(
    project_base_dir: str = '.',
    recursive: bool = True,
    plain_text: bool = False,
    file_keep_rule: Optional[Callable[[str], bool]] = None,
    dir_keep_rule: Optional[Callable[[str], bool]] = None,
    category: Callable[[str], str] = lambda full_path : Path(full_path).suffix,
    visible_only: bool = True
) -> Dict[str, Dict | str] | str:
    def fetch_inner(curr_path: str) -> Dict[str, Dict | str]:
        try:
            curr_output_dict = {}
            targets = os.listdir(curr_path)
            for entry in targets:
                if visible_only and entry.startswith('.'):
                    continue
                entry_path = os.path.join(curr_path, entry)
                if os.path.isfile(entry_path):
                    if file_keep_rule is None or file_keep_rule(entry):
                        curr_output_dict[entry] = category(entry_path)
                elif os.path.isdir(entry_path):
                    if dir_keep_rule is None or dir_keep_rule(entry):
                        if recursive:
                            curr_output_dict[entry] = fetch_inner(os.path.join(curr_path, entry))
                        else:
                            curr_output_dict[entry] = 'directory'
        except Exception:
            raise
        return curr_output_dict
    try:
        result = fetch_inner(project_base_dir)
        return result if not plain_text else json.dumps(result, indent=2)
    except Exception as e:
        LOGGER.warning(f'An error has occurred when traversing the project: {e}.')
        result = {}
        return result if not plain_text else json.dumps(result, indent=2)
    

if __name__ == '__main__':
    print(
        fetch_project_file_structure_function(
            plain_text=True,
            dir_keep_rule=lambda dir: dir not in ['log', '__pycache__']
        )
    )
