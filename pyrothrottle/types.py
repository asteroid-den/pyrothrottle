from typing import Union

from pyrogram.types import Message, CallbackQuery, InlineQuery
from pyrogram import Client, filters

Event = Union[Message, CallbackQuery, InlineQuery]

Number = Union[int, float]
