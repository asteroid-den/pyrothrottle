from time import monotonic

from pyrogram import Client

from .filters_base import FiltersBase
from ..misc import Event
from ..request_info import RequestInfo

class PersonalThrottle(FiltersBase):

    def __call__(self, client: Client, event: Event) -> bool:
        uid = event.from_user.id
        now = monotonic()
        interval = self.get_interval(uid)
        last_processed = self.last_processed.setdefault(uid, 0)

        passed_enough = now >= last_processed + interval

        self.last_processed[uid] = now if passed_enough else last_processed
        last_processed = self.last_processed[uid]

        event.request_info = RequestInfo(now, self.last_processed[uid],
            now if now >= last_processed + interval else last_processed + interval,
            interval)

        if not passed_enough:
            if self.fallback:
                self.fallback(client, event)

        return passed_enough
