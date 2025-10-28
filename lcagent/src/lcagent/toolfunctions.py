import os
import json

from pathlib import Path
from typing import Dict, Callable, Optional, Literal, List, Tuple
from lcagent.langfetch import initialize_logger


LOGGER = initialize_logger(__name__)

def fetch_project_file_structure_function(
    project_base_dir: str = '.',
    recursive: bool = True,
    return_form: List[Literal['dict', 'json', 'tree', 'flat']] = ['dict', 'json', 'tree', 'flat'],
    file_keep_rule: Optional[Callable[[str], bool]] = None,
    dir_keep_rule: Optional[Callable[[str], bool]] = None,
    category: Callable[[str], str] = lambda full_path : Path(full_path).suffix,
    visible_only: bool = True
) -> Dict[str, Dict[str, Dict | str] | List[str] | str]:
    json_output: Optional[str] = None
    flat_output: List[str] = []
    tree_output: str = ''
    
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
                        flat_output.append(entry_path)
                elif os.path.isdir(entry_path):
                    if dir_keep_rule is None or dir_keep_rule(entry):
                        if recursive:
                            recursive_dict = fetch_inner(os.path.join(curr_path, entry))
                            if len(recursive_dict) > 0:
                                curr_output_dict[entry] = recursive_dict
                        else:
                            curr_output_dict[entry] = 'directory'
                            flat_output.append(entry_path)
        except Exception:
            raise
        return curr_output_dict
    
    tree_stack: List[Literal['not_last', 'last_one']] = []
    def draw_tree(input_dict: Dict[str, Dict | str], target: str = '', layer: int = 0) -> None:
        nonlocal tree_output, tree_stack
        for i, flag in enumerate(tree_stack):
            if i != len(tree_stack) - 1:
                tree_output += '│   ' if flag == 'not_last' else '    '
            else:
                tree_output += '├── ' if flag == 'not_last' else '└── '
        tree_output = tree_output + target + '\n'
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

    output_dict: Dict[str, Dict[str, Dict | str] | List[str] | str] = {}
    for form in return_form:
        if form == 'dict' and 'dict' not in output_dict:
            output_dict['dict'] = result
        elif form == 'json' and 'json' not in output_dict:
            json_output = json.dumps(result)
            output_dict['json'] = json_output
        elif form == 'flat' and 'flat' not in output_dict:
            output_dict['flat'] = flat_output
        elif form == 'tree' and 'tree' not in output_dict:
            draw_tree(result)
            output_dict['tree'] = tree_output
    return output_dict

if __name__ == '__main__':
    result = fetch_project_file_structure_function(
        return_form=['tree', 'flat'],
        file_keep_rule=lambda name: name.endswith('.py')  # 只保留Python文件
    )

    print("树形结构：")
    print(result['tree'])

    print("\n扁平路径：")
    for path in result['flat']:
        print(path)
