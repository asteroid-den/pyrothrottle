from time import monotonic

from pyrogram import Client

from .filters_base import FiltersBase
from ..misc import Event
from ..request_info import RequestInfo


class GlobalDebounce(FiltersBase):
    def __call__(self, client: Client, event: Event) -> bool:
        now = monotonic()
        interval = self.get_interval()

        passed_enough = now >= self.last_received + interval

        self.last_processed = now if passed_enough else self.last_processed

        event.request_info = RequestInfo(now, self.last_processed,
            now + interval, interval)

        if not passed_enough:
            if self.fallback:
                self.fallback(client, event)

        self.last_received = now

        return passed_enough
