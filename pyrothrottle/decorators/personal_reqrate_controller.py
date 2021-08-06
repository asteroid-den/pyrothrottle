from typing import Optional, Union, Callable
from time import time
from itertools import dropwhile

from pyrogram import Client

from ..reqrate_base import ReqrateBase
from ..request_info import RequestInfo


class PersonalReqrateController(ReqrateBase):

    def __call__(self, *args) -> Optional['PersonalReqrateController']:
        if self.callable:
            now = time()
            client, event = args
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
                self.callable(client, event)
                self.last_processed[uid] = requests.copy()

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
