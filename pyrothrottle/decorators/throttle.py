from abc import ABC, abstractmethod
from typing import Callable, NoReturn, Any
from time import monotonic
from inspect import iscoroutinefunction

from ..types import Client, Event, Number
from ..request_info import RequestInfo

class AbstractThrottle(ABC):
    def __call__(self, client: Client, event: Event):
        now = monotonic()

        interval = self._get_interval(client, event)
        last_processed = self._get_last_processed(client, event)

        available = now >= last_processed + interval

        if available:
            self._set_last_processed(client, event, now)
            last_processed = now

        event.request_info = RequestInfo(now, last_processed, last_processed + interval,
            interval)

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
    def _get_last_processed(self, client: Client, event: Event) -> float:
        pass

    @abstractmethod
    def _set_last_processed(self, client: Client, event: Event, time: float) -> NoReturn:
        pass



class Throttle(AbstractThrottle):
    def __init__(self, interval: Number, fallback: Callable = None):
        self._interval = interval
        self._handler = None
        self._fallback = fallback
        self._last_processed = {}

    def _get_interval(self, _, __) -> Number:
        return self._interval

    def _get_last_processed(self, _, event: Event) -> Number:
        return self._last_processed.setdefault(event.from_user.id, 0)

    def _set_last_processed(self, _, event: Event, time: float) -> NoReturn:
        self._last_processed[event.from_user.id] = time
