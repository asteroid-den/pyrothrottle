from typing import Optional, Union, Callable
from time import time
from itertools import dropwhile

from pyrogram import Client

from .filters_base import FiltersBase
from ..reqrate_base import ReqrateBase
from ..misc import Event
from ..request_info import RequestInfo

class PersonalReqrateController(FiltersBase, ReqrateBase):

    def __call__(self, client: Client, event: Event) -> bool:
        now = time()
        uid = event.from_user.id
        interval = self.get_interval(uid)
        amount = self.get_amount(uid)
        last_processed = self.last_processed.setdefault(uid, [])

        requests = list(dropwhile(lambda x: x + interval < now, last_processed))

        available = len(requests) < amount

        event.request_info = RequestInfo(now, requests, now if available else requests[0] + interval,
            interval, amount)

        if available:
            requests.append(now)
            self.last_processed[uid] = requests.copy()
        else:
            if self.fallback:
                self.fallback(client, event)

        return result

