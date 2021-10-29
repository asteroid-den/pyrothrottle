from abc import ABC, abstractmethod
from typing import Callable, NoReturn, Any, List
from time import monotonic
from inspect import iscoroutinefunction
from itertools import dropwhile

from ..types import Client, Event, Number
from ..request_info import RequestInfo

class AbstractReqrateController(ABC):
    def __call__(self, client: Client, event: Event):
        now = monotonic()

        interval = self._get_interval(client, event)
        amount = self._get_amount(client, event)
        last_processed = self._get_last_processed(client, event)

        requests = list(dropwhile(lambda x: x + interval < now, last_processed))

        available = len(requests) < amount

        if available:
            requests.append(now)
            self._set_last_processed(client, event, requests.copy())

        event.request_info = RequestInfo(now, requests, now if available else requests[0] + interval,
            interval, amount)

        if available:
            return self._handler(client, event)

        else:
            if self._fallback:
                return self._fallback(client, event)

    def wraps(self, f: Callable[[Client, Event], Any]) -> Callable[[Client, Event], Any]:
        if callable(f):
            self._handler = f

            if iscoroutinefunction(f):
                async def async_caller(c: Client, e: Event):
                    await self(c, e)

                return async_caller

            else:
                return self

        else:
            raise TypeError('handler must be callable')

    def on_fallback(self, f: Callable[[Client, Event], Any]) -> Callable[[Client, Event], Any]:
        if callable(f):
            self._fallback = f
            return f
        else:
            raise TypeError('handler must be callable')

    @abstractmethod
    def _get_interval(self, client: Client, event: Event) -> Number:
        pass

    @abstractmethod
    def _get_amount(self, client: Client, event: Event) -> int:
        pass

    @abstractmethod
    def _get_last_processed(self, client: Client, event: Event) -> List[float]:
        pass

    @abstractmethod
    def _set_last_processed(self, client: Client, event: Event, requests: List[float]) -> NoReturn:
        pass



class ReqrateController(AbstractReqrateController):
    def __init__(self, interval: Number, amount: int, fallback: Callable = None):
        self._interval = interval
        self._amount = amount
        self._handler = None
        self._fallback = fallback
        self._last_processed = {}

    def _get_interval(self, _, __) -> Number:
        return self._interval

    def _get_amount(self, _, __) -> int:
        return self._amount

    def _get_last_processed(self, _, event: Event) -> List[float]:
        return self._last_processed.setdefault(event.from_user.id, [])

    def _set_last_processed(self, _, event: Event, requests: List[float]) -> NoReturn:
        self._last_processed[event.from_user.id] = requests
