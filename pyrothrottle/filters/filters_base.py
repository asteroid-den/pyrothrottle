from pyrogram import filters

from ..base import Base
from ..misc import get_modulename, Event


class FiltersBase(Base):

    @property
    def filter(self) -> filters.Filter:

        modulename = get_modulename(__name__)

        if not hasattr(self, '_filter'):
            self._filter = filters.create(self, modulename)

        return self._filter
