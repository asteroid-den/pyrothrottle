from typing import Optional
from time import time

from ..base import Base
from ..request_info import RequestInfo

class GlobalThrottle(Base):

    def __call__(self, *args) -> Optional['GlobalThrottle']:
        if self.callable:
            now = time()
            client, event = args
            interval = self.get_interval()

            passed_enough = now >= self.last_processed + interval

            self.last_processed = now if passed_enough else self.last_processed

            event.request_info = RequestInfo(now, self.last_processed,
                now if passed_enough else self.last_processed + interval, interval)

            if passed_enough:
                self.callable(client, event)

            else:
                if self.fallback:
                    self.fallback(client, event)

            self.last_received = now

        else:
            f = args[0]
            if callable(f):
                self.callable = args[0]
                return self
            else:
                raise TypeError('handler must be callable')
