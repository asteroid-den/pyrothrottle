# pyrothrottle
Throttle and debounce add-on for Pyrogram  

**⚠️ UNDER HEAVY MAINTENANCE ⚠️**  

## Quickstart
> implementation on decorators
```python3
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrothrottle.decorators import personal_throttle

client = Client('client')

@client.on_message(filters.incoming & filters.text)
@personal_throttle(3)
def handler(c: Client, m: Message):
    m.reply_text(f'Message processed. You can send next in {m.request_info.interval} seconds')

@handler.on_fallback
def fallback_handler(c: Client, m: Message):
    m.reply_text(f'Too fast. Write me after {m.request_info.cooldown} seconds')

client.run()
```

> implementation on filters
```python3
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrothrottle.filters import personal_throttle

client = Client('client')
throttle = personal_throttle(3)

@client.on_message(filters.incoming & filters.text & throttle.filter)
def handler(c: Client, m: Message):
    m.reply_text(f'Message processed. You can send next in {m.request_info.interval} seconds')

@throttle.on_fallback
def fallback_handler(c: Client, m: Message):
    m.reply_text(f'Too fast. Write me after {m.request_info.cooldown} seconds')
```  
## Docs
First of all, I have to mention that package has two implementations (each was shown in _Quickstart_ section), so, each type of antispam system would have two equal named classes, one in `.filters` subpackage, and one in `.decorators` subpackage.  
Also, for convinient usage, every class (when package is initialised) named in snake case (**_But in declaration they're named in camel case as it should be_**). So, in documentation they will be named as usual classes (for example, `PersonalDebounce`), but in code you have to use snake case names (for example, `personal_debounce`).  

> Meaningful part

In order to choice right system, you just need to undestand 5 terms.
- Global  
`Global` in class name means that chosen system would have common for all users counter.
- Personal  
`Personal` in class name means that chosen system would have separate counters for each user.  
- Throttle  
`Throttle` system counts interval between **now** and **last processed** (not **last received**) event. If this interval equals to or greater than given, event would be processed. Only `interval` is mandatory parameter.
- Debounce  
`Debounce` system counts interval between **now** and **last received** event. If this interval equals to or greater than given, event would be processed. Only `interval` is mandatory parameter.
- ReqrateController  
`ReqrateController` system counts, how many events were processed for last interval of time with length of provided **interval** (from some time point till **now**). If amount of processed events less than given allowed **amount**, event would be processed. Have 2 mandatory parameters: `interval` and `amount`.  

In every class name first goes scope (`Global` or `Personal`), and then technique name (for example, `PersonalDebounce`). 

> Full API explanation

### Classes
#### `class pyrothrottle.decorators.GlobalThrottle`
#### `class pyrothrottle.filters.GlobalThrottle`
**Parameters**:
- **interval**(`int`|`float`) — Interval between successfully processed events. Since it's `Throttle`, system would pass any event, if interval between **now** and **last processed** (not **last received**) event would equals to or be greater than given interval. Because it's `Global`, system wound have common for all users counter.
- **falback** (`callable`, _optional_) — Function that will be called if passed not enough time between events. Must accept two positional arguments _(client, event)_.

#### `class pyrothrottle.decorators.PersonalThrottle`
#### `class pyrothrottle.filters.PersonalThrottle`
**Parameters**:
- **interval**(`int`|`float`|`callable`) — Interval between successfully processed events. If `callable` passed, it must accept one positional argument _(user\_id)_  and return `int` or `float`. Since it's `Throttle`, system would pass an event, if interval between **now** and **last processed** (not **last received**) event would equals to or be greater than given interval. Because it's `Personal`, system wound have separate counters for each user.
- **falback** (`callable`, _optional_) — Function that will be called if passed not enough time between events. Must accept two positional arguments _(client, event)_.

#### `class pyrothrottle.decorators.GlobalDebounce`
#### `class pyrothrottle.filters.GlobalDebounce`
**Parameters**:
- **interval**(`int`|`float`) — Interval between successfully processed events. Since it's `Debounce`, system would pass an event, if interval between **now** and **last received** event would equals to or be greater than given interval. Because it's `Global`, system wound have common for all users counter.
- **falback** (`callable`, _optional_) — Function that will be called if passed not enough time between events. Must accept two positional arguments _(client, event)_.

#### `class pyrothrottle.decorators.PersonalDebounce`
#### `class pyrothrottle.filters.PersonalDebounce`
**Parameters**:
- **interval**(`int`|`float`|`callable`) — Interval between successfully processed events. If `callable` passed, it must accept one positional argument _(user\_id)_  and return `int` or `float`. Since it's `Debounce`, system would pass an event, if interval between **now** and **last received** event would equals to or be greater than given interval. Because it's `Personal`, system wound have separate counters for each user.
- **falback** (`callable`, _optional_) — Function that will be called if passed not enough time between events. Must accept two positional arguments _(client, event)_.

#### `class pyrothrottle.decorators.GlobalReqrateController`
#### `class pyrothrottle.filters.GlobalReqrateController`
**Parameters**:
- **interval**(`int`|`float`) — Interval between successfully processed events. Since it's `ReqrateController`, system would pass an event, if amount of processed for last interval of time with length of provided **interval** events less that given allowed **amount**. Because it's `Global`, system wound have common for all users counter.
- **amount**(`int`) — Allowed amount of processed requests during given **interval**.
- **falback** (`callable`, _optional_) — Function that will be called if passed not enough time between events. Must accept two positional arguments _(client, event)_.

#### `class pyrothrottle.decorators.PersonalReqrateController`
#### `class pyrothrottle.filters.PersonalReqrateController`
**Parameters**:
- **interval**(`int`|`float`|`callable`) — Interval between successfully processed events. If `callable` passed, it must accept one positional argument _(user\_id)_  and return `int` or `float`. Since it's `ReqrateController`, system would pass an event, if amount of processed for last interval of time with length of provided **interval** events less that given allowed **amount**. Because it's `Personal`, system wound have separate counters for each user.
- **amount**(`int`|`callable`) — Allowed amount of processed requests during given **interval**. If `callable` passed, it must accept one positional argument (_user\_id)_ and return `int`.
- **falback** (`callable`, _optional_) — Function that will be called if passed not enough time between events. Must accept two positional arguments _(client, event)_.  

### Decorators
Decorators intended to use in next way:
```python3
@client.on_event(...) # i.e. on_message, on_callback_query, etc.
@personal_throttle(3) # I'll use personal_throttle for examples
def handler(c: Client, e: Event):
    ...
```

If you want to add fallback handler to your system, you have to use `.on_fallback` (this method would contain in variable named as function that you registered as handler) as decorator. Fallback function must accept two positional arguments (same arguments as provided to main handler)
```python3
@handler.on_fallback
def fallback_handler(c: Client, e: Event):
    ...
```

**Please note**: `Event` objects (i.e. `Message`, `CallbackQuery` or `InlineQuery`) are patched, so they have have attribute `request_info` with usefull info (more on `RequestInfo` class later).  

### Filters
First of all, I have to mention that filter itself contained in `filter` attribute.
Filters have 2 major ways to use: normal and anonymous.
> Normal use
```python3
throttle = personal_throttle(3)

@client.on_event(different_filters & throttle.filter) # i.e. on_message, on_callback_query, etc.
def handler(c: Client, e: Event):
    ...

@throttle.on_fallback
def fallback_handler(c: Client, e: Event):
    ...
```

So, instead of decorators, when using filters (in normal way), `.on_fallback` must be called from antispam system instance

> Anonymous use
```python3
@client.on_event(different_filters & personal_throttle(3).filter) # i.e. on_message, on_callback_query, etc.
def handler(c: Client, e: Event):
    ...
```

So, comparing ways to use, the advantage of normal use is that you can add fallback using `.on_fallback`, while main advantage of anonymous usage is absence of necessity to create named instance what gives us less code. You still can specify fallback when creating anomyous instance

```python3
def fallback_handler(c: Client, e: Event):
    ...

@client.on_event(different_filters & personal_throttle(3, fallback_handler).filter)
def handler(c: Client, e: Event):
    ...
```

**Please note**: `Event` objects (i.e. `Message`, `CallbackQuery` or `InlineQuery`) are patched, so they have attribute `request_info` with usefull info (more on `RequestInfo` class later).  

### RequestInfo
So, as it was mentioned before, all incoming events are patched, so they have attribute `request_info` with `RequestInfo` instance.

#### `class pyrothrottle.RequestInfo`
**Attributes**:
- **time**(`float`) — timestamp of the moment when the event got into antispam system.
- **last_processed**(`float`|`list`) — timestamp (or list of timestamps) of last processed event(s).
- **next_successful**(`float`) — timestamp, when incoming event would be processed.
- **interval**(`int`|`float`) — user-defined interval for antispam system.
- **amount**(`int`, _optional_) — user-defined amount of events that should be processed during **interval** (only in `ReqrateController`)
- **cooldown**(`float`) — amount of time till **now** to **next successful** processed event.
