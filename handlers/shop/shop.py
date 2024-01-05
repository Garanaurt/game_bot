from aiogram import Router, Bot, F, types
from aiogram.filters import Command
from create_db import db
from keyboards.shop_kb import kb_set_lang, kb_ukr_all_games, kb_ukr_back, kb_rf_back, kb_rf_all_games
import re
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from main import MYGROUP



class SetLangStates(StatesGroup):
    LANG = State()


class SetGameStates(StatesGroup):
    GAME = State()


class GameState(StatesGroup):
    GAME = State()




router = Router()



async def delete_chat_mess(bot, chat):
    messages = db.db_get_messages_in_chat(chat)
    for msg in messages:
        chat_mess = int(msg[1])
        try:
            await bot.delete_message(chat_id=msg[0], message_id=chat_mess)
        except:
            pass
    db.db_delete_message_in_chat(chat)



async def save_message(message):
    chat_id = message.chat.id
    message_id = message.message_id
    db.db_add_message_in_messages(chat_id, message_id)


@router.callback_query(lambda c: re.match(r'^go_to_lang', c.data))
async def get_list(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await star(call, bot, state)



@router.message(SetGameStates.GAME, lambda c: re.match(r'^[\w-]+$', c.text))
async def echo(message: types.Message):
    msg = '<b>Oберіть гру із списку</b>'
    me = await message.answer(msg, parse_mode='HTML')
    await save_message(me)



@router.message(SetLangStates.LANG, lambda c: re.match(r'^[\w-]+$', c.text))
async def echo(message: types.Message):
    msg = '<b>Обери мову якою будеш проходити гру</b>'
    me = await message.answer(msg, parse_mode='HTML')
    await save_message(me)


@router.message(GameState.GAME, lambda c: re.match(r'^[\w-]+$', c.text))
async def echo(message: types.Message):
    msg = '<b>Завантажуй і встановлюй згідно з інструкцією</b>'
    me = await message.answer(msg, parse_mode='HTML')
    await save_message(me)


@router.message(Command('start'))
async def cmd_start(message: types.Message, bot: Bot, state: FSMContext):
    await star(message, bot, state) 
    

@router.callback_query(F.data == "star")
async def star(message: types.Message, bot: Bot, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    user_channel_status = await bot.get_chat_member(chat_id=MYGROUP, user_id=user_id)
    firstname = message.from_user.first_name
    await delete_chat_mess(bot, user_id)
    if user_channel_status.status == 'left':
        await bot.send_message(user_id, f'Ви не підписані на канал {MYGROUP}, підпишіться та спробуйте знову')
        return
    else:
        logo = types.FSInputFile('logolang.jpg')
        await state.set_state(SetLangStates.LANG)
        mess = await bot.send_photo(user_id,
                                    logo,
                                    caption=f'<b>Вітаю {firstname}! Я тут задля того, щоб тобі допомогти. Обери мову, якою будеш проходити гру!</b>',
                                    reply_markup=kb_set_lang(), parse_mode='HTML')
        await save_message(mess)


@router.callback_query(lambda c: c.data == "ukrainian")
async def set_lang_ukr(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await state.set_state(SetGameStates.GAME)
    chat_id = call.from_user.id
    games = db.db_get_all_games()
    await delete_chat_mess(bot, chat_id)
    username = call.from_user.first_name
    msg = f'<b>{username} на цій сторінці ти можеш обрати назву гри 🎮, яку будеш проходити!</b>'
    logo = types.FSInputFile('logogames.jpg')
    me = await bot.send_photo(chat_id, 
                              photo=logo, 
                              caption=msg, 
                              reply_markup=kb_ukr_all_games(games),
                              parse_mode='HTML')
    await save_message(me)


@router.callback_query(lambda c: re.match(r'^get_game_ukr_[\w-]+$', c.data))
async def get_ukr_game(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await state.set_state(GameState.GAME)
    game_id = call.data.split('_')[3]
    game_data = db.db_get_game_where_id(game_id)
    chat_id = call.from_user.id
    await delete_chat_mess(bot, chat_id)
    msg = '<b>Завантажити Українізатор 👇</b>\n'
    msg += f"{game_data[3]}\n\n"
    msg += "<b>Інструкція:📖</b>\n"
    msg += f"{game_data[4]}"
    logo = types.FSInputFile(game_data[2])
    mess = await call.message.answer_photo(photo=logo,
                                           caption=msg, 
                                           reply_markup=kb_ukr_back(), 
                                         parse_mode='HTML')
    await save_message(mess)


@router.callback_query(lambda c: c.data == "russian")
async def set_lang_rf(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await state.set_state(SetGameStates.GAME)
    chat_id = call.from_user.id
    username = call.from_user.first_name
    games = db.db_get_all_games()
    await delete_chat_mess(bot, chat_id)
    msg = f'<b>{username} на цій сторінці ти можеш обрати назву гри 🎮, яку будеш проходити!</b>'
    logo = types.FSInputFile('logogames.jpg')
    me = await bot.send_photo(chat_id, 
                              photo=logo, 
                              caption=msg, 
                              reply_markup=kb_rf_all_games(games), 
                              parse_mode='HTML')
    await save_message(me)


@router.callback_query(lambda c: re.match(r'^get_game_rf_[\w-]+$', c.data))
async def get_rf_game(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await state.set_state(GameState.GAME)
    game_id = call.data.split('_')[3]
    game_data = db.db_get_game_where_id(game_id)
    chat_id = call.from_user.id
    await delete_chat_mess(bot, chat_id)
    msg = '<b>Завантажити Русифікатор 👇</b>\n'
    msg += f"{game_data[5]}\n\n"
    msg += "<b>Інструкція:📖</b>\n"
    msg += f"{game_data[6]}"
    logo = types.FSInputFile(game_data[2])
    mess = await call.message.answer_photo(photo=logo,
                                           caption=msg, 
                                           reply_markup=kb_rf_back(), 
                                         parse_mode='HTML')
    await save_message(mess)