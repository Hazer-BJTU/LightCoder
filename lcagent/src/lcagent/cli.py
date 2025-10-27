import os
import time
import queue
import threading

from rich.console import Console
from .langfetch import initialize_logger


MODULE_DIR: str = os.path.dirname(os.path.abspath(__file__))
LOGGER = initialize_logger(__file__)

class CliManager:
    def __init__(self):
        self.quit: bool = False
        self.event_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self.run, args=())
        self.console = Console()
        self.worker_thread.start()

    def run(self) -> None:
        while not self.quit:
            pass

    def terminate(self) -> None:
        self.quit = True
        self.worker_thread.join()

if __name__ == '__main__':
    climanager = CliManager()
    time.sleep(5)
    climanager.terminate()
