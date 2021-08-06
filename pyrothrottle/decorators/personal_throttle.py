from typing import Optional
from time import time

from ..base import Base
from ..request_info import RequestInfo

class PersonalThrottle(Base):

    def __call__(self, *args) -> Optional['PersonalThrottle']:
        if self.callable:
            now = time()
            client, event = args
            uid = event.from_user.id
            interval = self.get_interval(uid)
            last_processed = self.last_processed.setdefault(uid, 0)
            last_received = self.last_received.setdefault(uid, 0)

            passed_enough = now >= last_processed + interval

            self.last_processed[uid] = now if passed_enough else last_processed
            last_processed = self.last_processed[uid]

            event.request_info = RequestInfo(now, last_processed,
                now if now >= last_processed + interval else last_processed + interval,
                interval)

            if passed_enough:
                self.callable(client, event)
                self.last_processed[uid] = now

            else:
                if self.fallback:
                    self.fallback(client, event)

            self.last_received[uid] = now

        else:
            f = args[0]
            if callable(f):
                self.callable = args[0]
                return self
            else:
                raise TypeError('handler must be callable')
