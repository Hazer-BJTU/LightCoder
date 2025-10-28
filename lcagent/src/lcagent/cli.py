import os
import time
import queue
import threading

from rich.live import Live
from rich.console import Console
from rich.markdown import Markdown
from typing import Dict, Any, Callable
from lcagent.langfetch import initialize_logger


MODULE_DIR: str = os.path.dirname(os.path.abspath(__name__))
LOGGER = initialize_logger(__file__)
CONSOLE = Console()

def print_markdown(markdown_content: str) -> None:
    try:
        live_content: str = ''
        with Live(live_content, console=CONSOLE, refresh_per_second=10) as live:
            for character in markdown_content:
                live_content += character
                live.update(live_content)
                time.sleep(0.1)
            md = Markdown(live_content)
            live.update(md)
    except Exception as e:
        LOGGER.warning(f'An error has occurred when printing markdown content: {e}')

TEST_CONTENT = """
```markdown
# 测试文档

这是一段简单的文本内容，用于测试 Markdown 的基本功能。😊🎉

## 代码示例

下面是一个 Python 代码片段：

```python
def hello_world():
    print("Hello, World! 👋")
    return True
```

## 数学公式

这是一个行内公式：\\( E = mc^2 \\)

## 枚举列表

以下是几个常用的编程语言：

- Python 🐍
- JavaScript 💛
- Rust 🦀
- Go 💙

## 总结

这就是一个包含多种 Markdown 元素的测试文档！🌟
```

这个 Markdown 文档包含了：
- 标题（# 和 ##）
- 普通文本段落
- 代码块(Python)
- 数学公式（行内）
- 枚举列表
- Emoji 表情符号
"""

if __name__ == '__main__':
    print_markdown(TEST_CONTENT)
