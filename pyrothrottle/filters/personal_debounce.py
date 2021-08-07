from time import monotonic

from pyrogram import Client

from .filters_base import FiltersBase
from ..misc import Event
from ..request_info import RequestInfo

class PersonalDebounce(FiltersBase):

    def __call__(self, client: Client, event: Event) -> bool:
        uid = event.from_user.id
        now = monotonic()
        interval = self.get_interval(uid)
        last_processed = self.last_processed.setdefault(uid, 0)
        last_received = self.last_received.setdefault(uid, 0)

        passed_enough = now >= last_received + interval

        self.last_processed[uid] = now if passed_enough else last_processed

        event.request_info = RequestInfo(now, self.last_processed[uid],
            now + interval, interval)

        if not passed_enough:
            if self.fallback:
                self.fallback(client, event)

        self.last_received[uid] = now

        return passed_enough
