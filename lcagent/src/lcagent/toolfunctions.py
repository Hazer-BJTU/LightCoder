import os
import json

from pathlib import Path
from typing import Dict, Callable, Optional, Literal, List
from lcagent.langfetch import initialize_logger


LOGGER = initialize_logger(__file__)

def fetch_project_file_structure_function(
    project_base_dir: str = '.',
    recursive: bool = True,
    return_form: Literal['dict', 'json', 'tree'] = 'tree',
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
    
    tree_output: str = ''
    tree_stack: List[Literal['not_last', 'last_one']] = []
    def draw_tree(input_dict: Dict[str, Dict | str], target: str = '', layer: int = 0) -> None:
        nonlocal tree_output, tree_stack
        for i, flag in enumerate(tree_stack):
            if i != len(tree_stack) - 1:
                tree_output += '│   ' if flag == 'not_last' else '    '
            else:
                tree_output += '├── ' if flag == 'not_last' else '└── '
        tree_output = tree_output + target + os.linesep
        tree_stack.append('not_last')
        for i, (key, value) in enumerate(input_dict.items()):
            if i == len(input_dict.items()) - 1:
                tree_stack[layer] = 'last_one'
            draw_tree({} if isinstance(value, str) else value, key, layer + 1)
        tree_stack.pop()

    try:
        result = fetch_inner(project_base_dir)
    except Exception as e:
        LOGGER.warning(f'An error has occurred when traversing the project: {e}.')
        result = {}
    
    if return_form == 'dict':
        return result
    elif return_form == 'json':
        return json.dumps(result, indent=2)
    elif return_form == 'tree':
        draw_tree(result)
        return tree_output

if __name__ == '__main__':
    print(fetch_project_file_structure_function(return_form='tree'))
