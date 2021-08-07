from typing import Optional, Union, Callable
from time import monotonic
from itertools import dropwhile

from pyrogram import Client

from .filters_base import FiltersBase
from ..reqrate_base import ReqrateBase
from ..misc import Event
from ..request_info import RequestInfo

class GlobalReqrateController(FiltersBase, ReqrateBase):

    def __call__(self, client: Client, event: Event) -> bool:
        now = monotonic()
        interval = self.get_interval()
        amount = self.get_amount()

        requests = list(dropwhile(lambda x: x + interval < now, self.last_processed))

        available = len(requests) < amount

        event.request_info = RequestInfo(now, requests, now if available else requests[0] + interval,
            amount)

        if available:
            requests.append(now)
            self.last_processed = requests.copy()
        else:
            if self.fallback:
                self.fallback(client, event)

        return available
