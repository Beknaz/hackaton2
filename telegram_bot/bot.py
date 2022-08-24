from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os


bot = Bot(token='5611827190:AAF5B0iUzk0a3MdycObr_ptdbLzPDVf58Ho')
dp = Dispatcher(bot)

async def on_startup(_):
    print('Бот вышел в онлайн')

#==================Клиентская часть================

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):

    await bot.send_message(message.from_user.id, 'Здравствуйте, вас приветствует клиника MakersClinic')
     


@dp.message_handler(commands=['Режим работы '])
async def clinic_open_comand(message: types.Message):

    await bot.send_message(message.from_user.id, 'Пн-Сб  с  08:00 до 21:00')




@dp.message_handler(commands=['Расположение'])
async def clinic_place_command(message: types.Message):

    await bot.send_message(message.from_user.id, 'ул. Табышалиева 29')






#==================Админская часть===============


#==================Общая часть===================






@dp.message_handler()
async def send(message: types.Message):
    if message.text == 'Здравствуйте':

        await message.answer('Добрый день! ')

      

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
