from typing import Union

from pyrogram.types import Message, CallbackQuery, InlineQuery

Event = Union[Message, CallbackQuery, InlineQuery]

get_modulename = lambda n: n.split('.')[-1]
