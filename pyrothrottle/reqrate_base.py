from typing import Optional, Union, Callable, Any, List

from pyrogram import Client

from .base import Base
from .misc import Event, get_modulename

class ReqrateBase(Base):

    def __init__(
        self,
        interval: Union[float, int, Callable[[int], Union[int, float]]],
        amount: Union[int, Callable[[int], int]],
        fallback: Optional[Callable[[Client, Event, List[float]], Any]] = None
    ):
        super().__init__(interval, fallback)
        self.amount = amount
        self.last_processed = [] if 'global' in get_modulename(__name__) else {}

    def get_amount(self, uid: Optional[int] = None) -> int:
        if uid and callable(self.amount):
            return self.amount(uid)

        return self.amount
