import re
from aiogram.types import Message
from aiogram.filters import BaseFilter


class FilterLink(BaseFilter):

    def __init__(self, mask: str):
        self.mask: str = mask

    async def __call__(self, message: Message):
        try:

            if re.search(self.mask, message.text):
                return message
            return False
        except: 
            return False


