from aiogram.filters import CommandStart, Command
from aiogram import Router, types, F
from app.keyboards import Keyboard as K
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.module import *
import asyncio


router = Router()

data_user = {}
flag_user = {}
active_tasks = {}

class Params(StatesGroup):
    min_price = State()
    max_price = State()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    data_user[message.from_user.id] = {'first_name': message.from_user.first_name, 'min_price': None, 'max_price': None}
    await message.answer(f'Привет {data_user[message.from_user.id]['first_name']}', reply_markup=K.main)

@router.callback_query(F.data == 'set_params')
async def set_params(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Params.min_price)
    await call.answer(f'Задайте минимальную цену, {data_user[call.from_user.id]['first_name']}')
    await call.message.answer('Введите минимальную цену')

@router.message(Params.min_price)
async def get_max_price(message: types.Message, state: FSMContext):
    try:
        await state.update_data(min_price = int(message.text))
        await state.set_state(Params.max_price)
        await message.answer('Введите максимальную цену')
        
    except ValueError:
        await message.answer('Вы ввели не число, попробуйте снова')

@router.message(Params.max_price)
async def save_data(message: types.Message, state: FSMContext):
    try:
        await state.update_data(max_price=int(message.text))
        data = await state.get_data()
        if data['min_price'] > data['max_price']:
            await message.answer('Минимальная цена не может быть больше максимальной.\nПопробуйте снова задать максимальную цену')
            return

        data_user[message.from_user.id]['min_price'] = data["min_price"]
        data_user[message.from_user.id]['max_price'] = data["max_price"]
        await state.clear()

        await message.answer(f'Вы задали параметры цены от {data_user[message.from_user.id]['min_price']} до {data_user[message.from_user.id]['max_price']}', reply_markup=K.main)
    except ValueError:
        await message.answer('Вы ввели не число попробуйте снова')

@router.callback_query(F.data == 'get_pars')
async def get_pars(call: types.CallbackQuery):
    await call.answer('Запрос обрабатывается')
    await call.message.answer('Нужно немного подождать...')
    min_p = data_user[call.from_user.id]['min_price']
    max_p = data_user[call.from_user.id]['max_price']
    data = await data_collection(min_p, max_p)
    for url in data:
        await call.message.answer(f'{url}')
    
    await call.message.answer(f'Что делаем дальше {data_user[call.from_user.id]['first_name']}', reply_markup=K.main)
    
@router.callback_query(F.data == 'get_not')
async def get_not(call: types.CallbackQuery):
    flag_user[call.from_user.id] = True
    await call.answer('Вы подключили получение уведомлений')
    await call.message.answer('Вы подключили получение уведомлений. Уведомления могут приходить с задержкой от 30 секунд до 2 минут')
    await call.message.answer('Чтобы выключить получение уведомлений пропишите команду "/offnot"')

    async def getnot_loop(user_id: int):
        print(f'notifictions status: ON, date: {datetime.now()}')
        data = await data_collection(data_user[user_id]['min_price'], data_user[user_id]['max_price'])
        
        if data:
            last = data
        else:
            print(f'ERROR "In func module", date: {datetime.now()} decription: Произошла ошибка при запросе к серверу, программа продолжит работать через 2 минуты')
            sleep(120)
        
        while flag_user.get(user_id, False):
            try:
                    await asyncio.sleep(15)
                    current = await data_collection(data_user[call.from_user.id]["min_price"], data_user[call.from_user.id]["max_price"])
                    for i in range(len(current[:10])):
                        if current[i] not in last:
                            await call.message.answer(current[i])
                            print(f'{i + 1}: {current[i]}')
                        
                    last = current
            except Exception as error:
                print(f'ERROR "In func module": {error}, date: {datetime.now()} decription: Произошла ошибка при запросе к серверу, программа продолжит работать через 2 минуты')
                await asyncio.sleep(120)
    
    task = asyncio.create_task(getnot_loop(call.from_user.id))
    active_tasks[call.from_user.id] = task


@router.message(Command('offnot'))
async def off_not(message: types.Message):
    flag_user[message.from_user.id] = False

    if task := active_tasks.pop(message.from_user.id, None):
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    await message.answer('Вы отключили получение уведомлений')
    await message.answer('Что делаем дальше?', reply_markup=K.main)