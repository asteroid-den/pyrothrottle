from typing import Union, List, Optional
from dataclasses import dataclass, field
from time import time
from datetime import datetime

@dataclass
class RequestInfo:
    time: float
    last_processed: Union[float, List[float]]
    next_successful: float
    interval: Union[float, int] = field(repr=False)
    amount: Optional[int] = field(default=None, repr=False)

    @property
    def cooldown(self) -> float:
        return self.next_successful - self.time
