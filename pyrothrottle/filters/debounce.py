from abc import ABC, abstractmethod
from typing import Callable, NoReturn, Any
from time import monotonic

from ..types import Client, Event, Number, filters
from ..request_info import RequestInfo

class AbstractDebounce(ABC):
    __name__ = __qualname__

    async def __call__(self, client: Client, event: Event):
        now = monotonic()

        interval = self._get_interval(client, event)
        last_received = self._get_last_received(client, event)
        last_processed = self._get_last_processed(client, event)

        available = now >= last_received + interval

        self._set_last_received(client, event, now)

        if available:
            self._set_last_processed(client, event, now)
            last_processed = now

        event.request_info = RequestInfo(now, last_processed, now + interval,
            interval)

        if not available:
            if self._fallback:
                await self._fallback(client, event)

        return available

    @property
    def filter(self) -> filters.Filter:
        return filters.create(self.__call__)

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
    def _get_last_received(self, client: Client, event: Event) -> float:
        pass

    @abstractmethod
    def _set_last_received(self, client: Client, event: Event) -> NoReturn:
        pass

    @abstractmethod
    def _get_last_processed(self, client: Client, event: Event) -> float:
        pass

    @abstractmethod
    def _set_last_processed(self, client: Client, event: Event, time: float) -> NoReturn:
        pass



class Debounce(AbstractDebounce):
    def __init__(self, interval: Number, fallback: Callable = None):
        self._interval = interval
        self._fallback = fallback
        self._last_processed = {}
        self._last_received = {}

    def _get_interval(self, _, __) -> Number:
        return self._interval

    def _get_last_processed(self, _, event: Event) -> Number:
        return self._last_processed.setdefault(event.from_user.id, 0)

    def _set_last_processed(self, _, event: Event, time: float) -> NoReturn:
        self._last_processed[event.from_user.id] = time

    def _get_last_received(self, _, event: Event) -> Number:
        return self._last_received.setdefault(event.from_user.id, 0)

    def _set_last_received(self, _, event: Event, time: float) -> NoReturn:
        self._last_received[event.from_user.id] = time

