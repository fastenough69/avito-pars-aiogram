from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Keyboard:
    main = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Получать уведомления о новых объявлениях', callback_data='get_not')],
        [InlineKeyboardButton(text='Получить первую страницу объявлений', callback_data='get_pars')],
        [InlineKeyboardButton(text='Задать параметры цены', callback_data='set_params')]])