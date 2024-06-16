############################################## ИМПОРТ ##############################################
import asyncio
import os
import segno
import cv2

from aiogram import Dispatcher, Bot, F, html
from aiogram.types import FSInputFile, Message, CallbackQuery
from aiogram.filters import Command

from app import keyboard as kb
from app.keyboard import Keyboard
from app.linkfil import FilterLink

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv

############################################## OБЬЯВЛЕНИЕ ВЕДУЩИХ КЛАССОВ ##############################################

load_dotenv()

storage=MemoryStorage()

bot = Bot(os.getenv('TOKEN_API'))
dp = Dispatcher(bot=bot, storage=storage)

kb_code_decode=Keyboard(text=['Создать QR код🔐', 'Декодировать QR код🔑'], callback=['code','decode'])

class FSMQR(StatesGroup):
    code=State()
    decode=State()



############################################## КОМАНДА СТАРТ ##############################################
@dp.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):

    # ЕСЛИ ПОЛЬЗОВАТЕЛЬ НОВЫЙ СОЗДАЕМ ПОД НЕГО ФАЙЛ С QR КОДОМ #

    await state.update_data(color='black')

    await (message.answer(f'Привет {message.from_user.full_name}'
                          f'Данный бот кодирует и декодирует QR коды',
                         reply_markup=kb_code_decode.make_inline()))










############################################## РЕЖИМ КОДИРОВАНИЯ ##############################################
@dp.callback_query(F.data=='code')
async def color(callback: CallbackQuery, state: FSMContext):

    if not os.path.isdir(f'users/qr{callback.from_user.id}'):
        os.makedirs(f'users/qr{callback.from_user.id}')

    await state.update_data(color='black')

    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer('Выбирите цвет:', reply_markup=kb.Keyb())
    await state.set_state(FSMQR.code)


#--------------------------------------------- ВЫБОР ЦВЕТА
@dp.callback_query(FSMQR.code, F.data=='color_y')
async def color(callback: CallbackQuery,state: FSMContext):

    await callback.message.answer('Отлично теперь отправь ссылку',reply_markup=kb.Keyba())
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await state.update_data(color='yellow')


@dp.callback_query(FSMQR.code, F.data=='color_g')
async def color(callback: CallbackQuery,state: FSMContext):

    await callback.message.answer('Отлично теперь отправь ссылку',reply_markup=kb.Keyba())
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await state.update_data(color='green')


@dp.callback_query(FSMQR.code, F.data=='color_r')
async def color(callback: CallbackQuery,state: FSMContext):

    await callback.message.answer('Отлично теперь отправь ссылку', reply_markup=kb.Keyba())
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await state.update_data(color='red')


@dp.callback_query(FSMQR.code, F.data=='color_b')
async def color(callback: CallbackQuery,state: FSMContext):

    await callback.message.answer(f'Отлично теперь отправь ссылку',reply_markup=kb.Keyba())
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await state.update_data(color='blue')



@dp.callback_query(FSMQR.code,F.data=='color_bl')
async def color(callback: CallbackQuery,state: FSMContext):

    await callback.message.answer(f'Отлично теперь отправь ссылку',reply_markup=kb.Keyba())
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await state.update_data(color='black')


#--------------------------------------------- КНОПКА НАЗАД
@dp.callback_query(F.data=='back')
async def back(callback: CallbackQuery):

    await callback.message.answer('Выбери категорию', reply_markup=kb_code_decode.make_inline())
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


#--------------------------------------------- ОТПРАВКА QR КОДА
@dp.message(FSMQR.code, FilterLink(mask='http[s]'))
async def code(message: Message, state: FSMContext):
    try:
        # ВЫБОРКА ССЫЛКИ ИЗ СООБЩЕНИЯ #
        current_state = await state.get_data()

        data = {"url": "None"}
        entities = message.entities or []
        for item in entities:
            if item.type in data.keys():
                data[item.type] = item.extract_from(message.text)

        # ПРЕОБРАЗОВАНИЕ И СОХРАНЕНИЕ QR КОДА В СОЗДАННУЮ ДИРЕКТОРИЮ #
        qr = segno.make(f'{html.quote(data["url"])}')
        qr.save(out=f'users/qr{message.from_user.id}/qr.png' ,dark=current_state.get('color'), scale=5)

        # ДАЛЬНЕЙШАЯ ОТПРАВКА СООБЩЕНИЯ #
        await message.answer_photo(FSInputFile(f'users\qr{message.from_user.id}/qr.png'))
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)

    except:
        pass

    finally:
        await message.delete()
        await state.clear()

        os.remove(f"users/qr{message.from_user.id}/qr.png")
        os.rmdir(f"users/qr{message.from_user.id}")

    

#----------------------------------Фильтрация сообщений
@dp.message(FSMQR.code)
async def all_msg(message: Message):


    await message.reply('Это не ссылка')
    await message.delete()
  
    await asyncio.sleep(1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)







############################################## РЕЖИМ ДЕКОДИРОВАНИЯ ##############################################
@dp.callback_query(F.data=='decode')
async def qr_msg(callback: CallbackQuery, state: FSMContext):

    if not os.path.isdir(f'users/qr{callback.from_user.id}'):
        os.makedirs(f'users/qr{callback.from_user.id}')

    await state.update_data(color='black')
    await callback.message.answer('Отправь QR код:', reply_markup=kb.Keyba())
    await state.set_state(FSMQR.decode)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)



@dp.message(FSMQR.decode, F.photo)
async def decode(message: Message, state: FSMContext):

    await bot.download(message.photo[-1], destination=f'users/qr{message.from_user.id}/qr.png')

    linc=cv2.imread(f'users/qr{message.from_user.id}/qr.png', flags=cv2.IMREAD_GRAYSCALE)
    detector=cv2.QRCodeDetector()
    data,bbox,qr = detector.detectAndDecode(linc)

    try:

        if bbox is None:
            await message.answer('Это не QR код')
            return
        await message.answer(html.quote(data))

    finally:

        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await state.clear()

        os.remove(f"users/qr{message.from_user.id}/qr.png")
        os.rmdir(f"users/qr{message.from_user.id}")


@dp.message(FSMQR.decode)
async def all_msg(message: Message):

    await message.answer("Это не QR код")
    await message.delete()
    await asyncio.sleep(1)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id+1)




############################################## { } ##############################################
@dp.message()
async def all(message: Message):

    await message.delete()
    await message.answer("Выбери режим", reply_markup=kb_code_decode.make_inline())


async def main():

    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
