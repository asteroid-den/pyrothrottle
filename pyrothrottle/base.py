from typing import Union, Callable, Optional, Any

from pyrogram import Client

from .misc import Event, get_modulename

class Base:
    def __init__(
        self,
        interval: Union[float, int, Callable[[int], Union[int, float]]],
        fallback: Optional[Callable[[Client, Event], Any]] = None
    ):
        self.interval = interval
        self.callable = None
        self.fallback = fallback
        self.last_processed = 0 if 'global' in get_modulename(__name__) else {}
        self.last_received = 0 if 'global' in get_modulename(__name__) else {}

    def on_fallback(self, f: Callable[[Client, Event], Any]) -> Callable[[Client, Event], Any]:
        if callable(f):
            self.fallback = f
            return f
        else:
            raise TypeError('handler must be callable')

    def get_interval(self, uid: Optional[int] = None) -> Union[float, int]:
        if uid and callable(self.interval):
            return self.interval(uid)

        return self.interval
