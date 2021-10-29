# pyrothrottle
Throttle and debounce add-on for Pyrogram  

## Quickstart
> implementation on decorators
```python3
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrothrottle.decorators import Throttle

client = Client('client')
throttle = Throttle(3)

@client.on_message(filters.incoming & filters.text)
@throttle.wraps
async def handler(c: Client, m: Message):
    await m.reply_text(f'Message processed. You can send next in {m.request_info.interval} seconds')

@throttle.on_fallback
async def fallback_handler(c: Client, m: Message):
    await m.reply_text(f'Too fast. Write me after {m.request_info.cooldown} seconds')

client.run()
```

> implementation on filters
```python3
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrothrottle.filters import Throttle

client = Client('client')
throttle = Throttle(3)

@client.on_message(filters.incoming & filters.text & throttle.filter)
async def handler(c: Client, m: Message):
    await m.reply_text(f'Message processed. You can send next in {m.request_info.interval} seconds')

@throttle.on_fallback
async def fallback_handler(c: Client, m: Message):
    await m.reply_text(f'Too fast. Write me after {m.request_info.cooldown} seconds')
```  
## Docs
First of all, I have to mention that package has two implementations (each was shown in _Quickstart_ section), so, each type of antispam system would have two equal named classes, one in `.filters` subpackage, and one in `.decorators` subpackage.  

> Meaningful part

In order to choice right system, you just need to undestand 3 terms.
- Throttle  
`Throttle` system counts interval between **now** and **last processed** (not **last received**) event. If this interval equals to or greater than given, event would be processed. Only `interval` is mandatory parameter.
- Debounce  
`Debounce` system counts interval between **now** and **last received** event. If this interval equals to or greater than given, event would be processed. Only `interval` is mandatory parameter.
- ReqrateController  
`ReqrateController` system counts, how many events were processed for last interval of time with length of provided **interval** (from some time point till **now**). If amount of processed events less than given allowed **amount**, event would be processed. Have 2 mandatory parameters: `interval` and `amount`.  

> Full API explanation

### Classes
#### `class pyrothrottle.decorators.Throttle`
#### `class pyrothrottle.filters.Throttle`
**Parameters**:
- **interval**(`int`|`float`) — Interval between successfully processed events. Since it's `Throttle`, system would pass any event, if interval between **now** and **last processed** (not **last received**) event would equals to or be greater than given interval.
- **fallback** (`callable`, _optional_) — Function that will be called if passed not enough time between events. Must accept two positional arguments _(client, event)_. It can be both `sync` or `async` if you're using decorator, and must be `async`, if you're using filter.

#### `class pyrothrottle.decorators.Debounce`
#### `class pyrothrottle.filters.Debounce`
**Parameters**:
- **interval**(`int`|`float`) — Interval between successfully processed events. Since it's `Debounce`, system would pass an event, if interval between **now** and **last received** event would equals to or be greater than given interval.
- **fallback** (`callable`, _optional_) — Function that will be called if passed not enough time between events. Must accept two positional arguments _(client, event)_. It can be both `sync` or `async` if you're using decorator, and must be `async`, if you're using filter.

#### `class pyrothrottle.decorators.ReqrateController`
#### `class pyrothrottle.filters.ReqrateController`
**Parameters**:
- **interval**(`int`|`float`) — Interval between successfully processed events. Since it's `ReqrateController`, system would pass an event, if amount of processed for last interval of time with length of provided **interval** events less that given allowed **amount**.
- **amount**(`int`) — Allowed amount of processed requests during given **interval**.
- **fallback** (`callable`, _optional_) — Function that will be called if passed not enough time between events. Must accept two positional arguments _(client, event)_. It can be both `sync` or `async` if you're using decorator, and must be `async`, if you're using filter.

### Decorators
Decorators intended to use in next way:
```python3
@client.on_event(...) # i.e. on_message, on_callback_query, etc.
@throttler.wraps # Wrapped handler can be both sync or async
async def handler(c: Client, e: Event):
    ...
```

If you want to add fallback handler to your system, you have to use `.on_fallback` method of your controller object (better to use as decorator). Fallback function must accept two positional arguments (same arguments as provided to main handler) and can be both `sync` or `async`.
```python3
@throttler.on_fallback
async def fallback_handler(c: Client, e: Event):
    ...
```

**Please note**: `Event` objects (i.e. `Message`, `CallbackQuery` or `InlineQuery`) are patched, so they have attribute `request_info` with usefull info (more on `RequestInfo` class later).  

### Filters
First of all, I have to mention that filter itself contained in `filter` attribute (to be honest, it's `property`). Use example:
```python3
throttle = Throttle(3)

@client.on_event(different_filters & throttle.filter) # i.e. on_message, on_callback_query, etc.
async def handler(c: Client, e: Event):
    ...

@throttle.on_fallback
async def fallback_handler(c: Client, e: Event):
    ...
```

**Be aware**: when using filters implementation and setting fallback, fallback handler **must** be `async`.  


**Please note**: `Event` objects (i.e. `Message`, `CallbackQuery` or `InlineQuery`) are patched, so they have attribute `request_info` with usefull info (more on `RequestInfo` class later).  

### RequestInfo
So, as it was mentioned before, all incoming events are patched, so they have attribute `request_info` with `RequestInfo` instance.

#### `class pyrothrottle.RequestInfo`
**Attributes**:
- **time**(`float`) — timestamp of the moment when the event got into antispam system.
- **last_processed**(`float`|`list`) — timestamp (or list of timestamps) of last processed event(s).
- **next_successful**(`float`) — timestamp, when incoming event would be processed.
- **interval**(`int`|`float`) — user-defined interval for antispam system.
- **amount**(`int`, _optional_) — user-defined amount of events that should be processed during **interval** (only for `ReqrateController`)
- **cooldown**(`float`) — amount of time till **now** to **next successful** processed event.  

### Advanced
If simple implementations of antispam systems, which was described before, doesn't suit to your specific use case, you can create your own implementation based on one of given abstract classes.

#### `class pyrothrottle.decorators.AbstractThrottle`
#### `class pyrothrottle.filters.AbstractThrottle`
You have to implement next methods:
- `def _get_interval(self, client: Client, event: Event) -> Number` — method that returns system interval for given event.
- `def _get_last_processed(self, client: Client, event: Event) -> float` — method that returns time of last processed event (as timestamp).
- `def _set_last_processed(self, client: Client, event: Event, time: float) -> NoReturn` — method that sets time of last processed event.

#### `class pyrothrottle.decorators.AbstractDebounce`
#### `class pyrothrottle.filters.AbstractDebounce`
You have to implement next methods:
- `def _get_interval(self, client: Client, event: Event) -> Number` — method that returns system interval for given event.
- `def _get_last_received(self, client: Client, event: Event) -> float` — method that returns time of last received event (as timestamp).
- `def _set_last_received(self, client: Client, event: Event, time: float) -> NoReturn` — method that sets time of last received event.
- `def _get_last_processed(self, client: Client, event: Event) -> float` — method that returns time of last processed event (as timestamp).
- `def _set_last_processed(self, client: Client, event: Event, time: float) -> NoReturn` — method that sets time of last processed event.

#### `class pyrothrottle.decorators.AbstractReqrateController`
#### `class pyrothrottle.filters.AbstractReqrateController`
You have to implement next methods:
- `def _get_interval(self, client: Client, event: Event) -> Number` — method that returns system interval for given event.
- `def _get_amount(self, client: Client, event: Event) -> int` — method that returns system requests quota per interval for given event.
- `def _get_last_processed(self, client: Client, event: Event) -> List[float]` — method that returns list of timestamps of last processed events.
- `def _set_last_processed(self, client: Client, event: Event, time: List[float]) -> NoReturn` — method that sets list of timestamps of last processed events.
