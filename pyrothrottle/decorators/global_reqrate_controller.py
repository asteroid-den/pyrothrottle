from typing import Optional, Union, Callable
from time import time
from itertools import dropwhile

from pyrogram import Client

from ..reqrate_base import ReqrateBase
from ..misc import Event
from ..request_info import RequestInfo

class GlobalReqrateController(ReqrateBase):

    def __call__(self, *args) -> Optional['GlobalReqrateController']:
        if self.callable:
            now = time()
            client, event = args
            interval = self.get_interval()
            amount = self.get_amount()

            requests = list(dropwhile(lambda x: x + interval < now, self.last_processed))

            available = len(requests) < amount

            event.request_info = RequestInfo(now, requests, now if available else requests[0] + interval,
                amount)

            if available:
                requests.append(now)
                self.callable(client, event)
                self.last_processed = requests.copy()

            else:
                if self.fallback:
                    self.fallback(client, event)

        else:
            f = args[0]
            if callable(f):
                self.callable = args[0]
                return self
            else:
                raise TypeError('handler must be callable')
