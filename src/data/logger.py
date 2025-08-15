from datetime import datetime
from string import Template
from typing import Literal, Optional
from rich.console import Console

console = Console()
pprint = console.print

COLORED_LEVELS = {
    "info": "[purple]INFO[/purple]",
    "debug": "[blue]DEBG[/blue]",
    "warn": "[yellow]WARN[/yellow]",
    "error": "[red]EROR[/red]",
    "start": "[magenta]STRT[/magenta]",
    "close": "[red]CLSE[/red]",
}

class Logger:
    def __init__(self, process_name: str, log_format: Template, time_format: str, log_file: str, debug_disabled: bool = False) -> None:
        self.console = Console()
        self.name = process_name
        self.format = log_format
        self.time_format = time_format
        self.log_file = log_file
        self.debug_disabled = debug_disabled
        
    def get_time(self) -> str:
        return datetime.now().strftime(self.time_format)

    def write_to_file(self, log_message: str) -> None:
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')

    def log(self, level: Literal["info", "debug", "warn", "error", "start", "close"] = "info", text: Optional[str] = None) -> None:
        if self.debug_disabled:
            if level == "debug":
                return
            else:
                formatted_text = self.format.substitute(
                    time=self.get_time(),
                    process=self.name,
                    level=COLORED_LEVELS[level],
                    message=f"[white]{text}[/white]",
                )
        else:
            formatted_text = self.format.substitute(
                    time=self.get_time(),
                    process=self.name,
                    level=COLORED_LEVELS[level],
                    message=f"[white]{text}[/white]",
                )
            
        pprint(f"[gray]{formatted_text}[/gray]")
        self.write_to_file(formatted_text)

    def info(self, message: Optional[str] = None, exception: Optional[str] = None, extra: Optional[str] = None) -> None:
        self.log("info", message)
        if exception:
            self.log("info", exception)
        if extra:
            self.log("info", extra)

    def debug(self, message: str) -> None: self.log("debug", message)

    def warn(self, message: str) -> None: self.log("warn", message)

    def error(self, message: str) -> None: self.log("error", message)

    def start(self, message: str) -> None: self.log("start", message)

    def close(self, message: str) -> None: self.log("close", message)

def space(list_max_length: int, word: str, add_space: int = 0) -> str:
    spaces = (list_max_length - len(str(word)) + add_space)
    return " " * spaces

def set_logger(
    process_name: str = __name__,
    process_tabs: int = 6,
    log_format: Optional[Template] = None,
    time_format: str = "%d.%m.%Y %H:%M:%S",
    log_path: str = "logs.log",
    debug_disabled: bool = False
) -> Logger:
    if log_format is None:
        log_format = Template(f"$time | {space(list_max_length=process_tabs, word=process_name)}$process | $level | $message")
    return Logger(process_name, log_format, time_format, log_path, debug_disabled)
