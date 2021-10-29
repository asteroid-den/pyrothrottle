from typing import Union, List, Optional
from dataclasses import dataclass, field

from .types import Number

@dataclass
class RequestInfo:
    time: float
    last_processed: Union[float, List[float]]
    next_successful: float
    interval: Number = field(repr=False)
    amount: Optional[int] = field(default=None, repr=False)

    @property
    def cooldown(self) -> float:
        return self.next_successful - self.time
