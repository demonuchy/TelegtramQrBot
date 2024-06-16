
from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import  InlineKeyboardBuilder, ReplyKeyboardBuilder

button_select = InlineKeyboardBuilder()
(button_select.add(InlineKeyboardButton(text='Выбрать цвет', callback_data='select')))

def Keyb():

    items=[['🟥','color_r'],['🟨','color_y'],['🟩','color_g'],['🟦','color_b'],['⬛️','color_bl'],['🔙','back']]
    button_color = InlineKeyboardBuilder()
    [button_color.add(InlineKeyboardButton(text=item[0], callback_data=item[1])) for item in items]
    button_color.adjust(3)
    return button_color.as_markup()

def Keyba():
    button_back=InlineKeyboardBuilder()
    button_back.add(InlineKeyboardButton(text='🔙', callback_data='back'))
    return button_back.as_markup()

class Keyboard():

    def __init__(self, callback: list = (), text: list = (), web=None):

        self.text=text
        self.callback=callback
        self.web=web



    def make_inline(self):

        button=InlineKeyboardBuilder()
        calltxt=list(zip(self.text,self.callback))
        [button.add(InlineKeyboardButton(text=text, callback_data=callback, web_app=self.web)) for text, callback in calltxt]
        button.adjust(1)
        return button.as_markup()

    def make_reply(self):

        button=ReplyKeyboardBuilder()
        [button.add(KeyboardButton(text=text, )) for text in self.text]
        return button.as_markup(resize_keyboard=True)
