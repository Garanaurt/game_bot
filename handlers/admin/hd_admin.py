from aiogram import Router, Bot, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from create_db import db
import re
import uuid
from keyboards.admin_kb import kb_get_main_menu, kb_go_to_main_menu, kb_delete_game, kb_cancel_but, kb_edit_game
from keyboards.admin_kb import kb_edit_game_proc


router = Router()


class AddProductStates(StatesGroup):
    NAME = State()
    DESCRIPTION = State()
    DESCRIPTIONRF = State()
    INSTRUCTION = State()
    IMAGE = State()


class ChangeNameStates(StatesGroup):
    NAME = State()


class ChangeDescriptionStates(StatesGroup):
    DESCRIPTION = State()


class ChangeDescriptionrfStates(StatesGroup):
    DESCRIPTIONRF = State()


class ChangeInstructionStates(StatesGroup):
    INSTRUCTION = State()


class ChangeImageStates(StatesGroup):
    IMAGE = State()



async def delete_chat_mess(bot, chat):
    messages = db.db_get_messages_in_chat_admin(chat)
    for msg in messages:
        chat_mess = int(msg[1])
        try:
            await bot.delete_message(chat_id=msg[0], message_id=chat_mess)
        except Exception:
            continue            
    db.db_delete_message_in_chat_admin(chat)



async def save_message(message):
    chat_id = message.chat.id
    message_id = message.message_id
    db.db_add_message_in_messages_admin(chat_id, message_id)




@router.callback_query(lambda c: c.data == "cancel_adding")
async def cancel_adding(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    username = call.from_user.username
    chat_id = call.from_user.id
    await delete_chat_mess(bot, chat_id)
    text = f'Привіт, {username}\n'
    me = await bot.send_message(chat_id, text, reply_markup=kb_get_main_menu())
    await save_message(me)
    
#Старт
@router.message(Command('start'))
async def cmd_start(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    if chat_id > 0:
        await cmd_star(message, bot)


@router.callback_query(F.data == "star")
async def cmd_star(call: types.CallbackQuery, bot: Bot):
    username = call.from_user.username
    chat_id = call.from_user.id
    await delete_chat_mess(bot, chat_id)
    text = f'Привіт, {username}\n'
    me = await bot.send_message(chat_id, text, reply_markup=kb_get_main_menu())
    await save_message(me)


@router.callback_query(lambda c: c.data == "product_list_main")
async def products_list(call: types.CallbackQuery, bot: Bot):
    chat = call.message.chat.id
    await delete_chat_mess(bot, chat)
    msg = 'Усі ігри в базі:\n'
    games = db.db_get_all_games()
    if games:
        for game in games:
            msg += f'{game[1]} \n'
    else:
        msg += f'Пусто'
    me = await bot.send_message(chat, msg, reply_markup=kb_go_to_main_menu())
    await save_message(me)




@router.callback_query(lambda c: c.data == "add_product_main")
async def add_product(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(AddProductStates.NAME)
    me = await call.message.edit_text(f"Напиши мені назву нової гри", reply_markup=kb_cancel_but(), parse_mode='HTML')
    await save_message(me)

    
@router.message(AddProductStates.NAME)
async def add_product_proc_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(AddProductStates.DESCRIPTION)
    me = await message.answer(f"Прийшли укр опис гри", reply_markup=kb_cancel_but(), parse_mode='HTML')
    await save_message(me)


@router.message(AddProductStates.DESCRIPTION)
async def add_product_proc_description(message: types.Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await state.set_state(AddProductStates.DESCRIPTIONRF)
    me = await message.answer(f"Прийшли рф опис гри", reply_markup=kb_cancel_but(), parse_mode='HTML')
    await save_message(me)


@router.message(AddProductStates.DESCRIPTIONRF)
async def add_product_proc_description(message: types.Message, state: FSMContext):
    descriptionrf = message.text
    await state.update_data(descriptionrf=descriptionrf)
    await state.set_state(AddProductStates.INSTRUCTION)
    me = await message.answer(f"Прийшли інстукцію для гри", reply_markup=kb_cancel_but(), parse_mode='HTML')
    await save_message(me)


@router.message(AddProductStates.INSTRUCTION)
async def add_product_proc_instruction(message: types.Message, state: FSMContext):
    instruction = message.text
    await state.update_data(instruction=instruction)
    await state.set_state(AddProductStates.IMAGE)
    me = await message.answer(f"Прийшли картинку", reply_markup=kb_cancel_but(), parse_mode='HTML')
    await save_message(me)


@router.message(AddProductStates.IMAGE, F.photo)
async def process_product_photo(message: types.Message, state: FSMContext, bot: Bot):
    photo = ''
    if message.photo:
        file_path = f'images/{uuid.uuid4()}.jpg'
        photo = message.photo[-1].file_id
    game_data = await state.get_data()
    await bot.download(photo, destination=file_path)
    game_data['image_path'] = file_path
    db.db_add_game_to_db(game_data)
    await state.clear()
    me = await message.answer(f"Гра у базі", reply_markup=kb_go_to_main_menu())
    await save_message(me)



@router.callback_query(lambda c: c.data == "del_product_main")
async def delete_product(call: types.CallbackQuery, bot: Bot):
    chat = call.message.chat.id
    games = db.db_get_all_games()
    await delete_chat_mess(bot, chat)
    me = await call.message.answer(f"Вибери гру яку треба видалити", reply_markup=kb_delete_game(games))
    await save_message(me)


@router.callback_query(lambda c: re.match(r'^delete_game_\d+$', c.data))
async def delete_game_proc(call: types.CallbackQuery, bot: Bot):
    game_id = call.data.split('_')[2]
    db.db_delete_game(game_id)
    me = await call.message.answer(f"Гра видалена з бази", reply_markup=kb_go_to_main_menu())
    await save_message(me)


@router.callback_query(lambda c: c.data == "edit_product_main")
async def delete_product(call: types.CallbackQuery, bot: Bot):
    chat = call.message.chat.id
    games = db.db_get_all_games()
    await delete_chat_mess(bot, chat)
    me = await call.message.answer(f"Вибери гру яку треба редагувати", reply_markup=kb_edit_game(games))
    await save_message(me)



@router.callback_query(lambda c: re.match(r'^edit_game_\d+$', c.data))
async def delete_game_proc(call: types.CallbackQuery, bot: Bot):
    game_id = call.data.split('_')[2]
    game = db.db_get_game_where_id(game_id)
    msg = ''
    msg += f'Назва - {game[1]}\n'
    msg += f'Опис укр - {game[3]}\n'
    msg += f'Опис рф - {game[5]}\n'
    msg += f'Інструкція - {game[4]}\n\n'
    msg += 'Вибери що хочеш змінити в цій грі'
    me = await call.message.answer(msg, reply_markup=kb_edit_game_proc(game_id))
    await save_message(me)



@router.callback_query(lambda c: re.match(r'^change_name_\d+$', c.data))
async def edit_game(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    game_id = call.data.split('_')[2]
    chat = call.message.chat.id
    await delete_chat_mess(bot, chat)
    await state.set_state(ChangeNameStates.NAME)
    await state.update_data(game_id=game_id)
    me = await call.message.answer(f"Прийшли нову назву", reply_markup=kb_cancel_but())
    await save_message(me)


   
@router.message(ChangeNameStates.NAME)
async def edit_product_proc_name(message: types.Message, state: FSMContext):
    name = message.text
    data = await state.get_data()
    game_id = data['game_id']
    db.db_set_game_name_where_id(game_id, name)
    await state.clear()
    me = await message.answer(f"Назву гри змінено", reply_markup=kb_go_to_main_menu())
    await save_message(me)





@router.callback_query(lambda c: re.match(r'^change_description_\d+$', c.data))
async def edit_game_descr(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    game_id = call.data.split('_')[2]
    chat = call.message.chat.id
    await delete_chat_mess(bot, chat)
    await state.set_state(ChangeDescriptionStates.DESCRIPTION)
    await state.update_data(game_id=game_id)
    me = await call.message.answer(f"Прийшли новий укр опис гри", reply_markup=kb_cancel_but())
    await save_message(me)


   
@router.message(ChangeDescriptionStates.DESCRIPTION)
async def edit_product_proc_descr(message: types.Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    game_id = data['game_id']
    db.db_set_game_description_where_id(game_id, description)
    await state.clear()
    me = await message.answer(f"Опис гри укр змінено", reply_markup=kb_go_to_main_menu())
    await save_message(me)




@router.callback_query(lambda c: re.match(r'^change_descriptionrf_\d+$', c.data))
async def edit_game_descrrf(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    game_id = call.data.split('_')[2]
    chat = call.message.chat.id
    await delete_chat_mess(bot, chat)
    await state.set_state(ChangeDescriptionrfStates.DESCRIPTIONRF)
    await state.update_data(game_id=game_id)
    me = await call.message.answer(f"Прийшли новий рф опис гри", reply_markup=kb_cancel_but())
    await save_message(me)


   
@router.message(ChangeDescriptionrfStates.DESCRIPTIONRF)
async def edit_product_proc_descrrf(message: types.Message, state: FSMContext):
    descriptionrf = message.text
    data = await state.get_data()
    game_id = data['game_id']
    db.db_set_game_description_rf_where_id(game_id, descriptionrf)
    await state.clear()
    me = await message.answer(f"Опис гри рф змінено", reply_markup=kb_go_to_main_menu())
    await save_message(me)



@router.callback_query(lambda c: re.match(r'^change_instruction_\d+$', c.data))
async def edit_game_instr(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    game_id = call.data.split('_')[2]
    chat = call.message.chat.id
    await delete_chat_mess(bot, chat)
    await state.set_state(ChangeInstructionStates.INSTRUCTION)
    await state.update_data(game_id=game_id)
    me = await call.message.answer(f"Прийшли нову інструкцію для гри", reply_markup=kb_cancel_but())
    await save_message(me)


   
@router.message(ChangeInstructionStates.INSTRUCTION)
async def edit_product_proc_instr(message: types.Message, state: FSMContext):
    instruction = message.text
    data = await state.get_data()
    game_id = data['game_id']
    db.db_set_game_instruction_where_id(game_id, instruction)
    await state.clear()
    me = await message.answer(f"Інструкція для гри змінена", reply_markup=kb_go_to_main_menu())
    await save_message(me)




@router.callback_query(lambda c: re.match(r'^change_image_\d+$', c.data))
async def edit_game_image(call: types.CallbackQuery, bot: Bot, state: FSMContext):
    game_id = call.data.split('_')[2]
    chat = call.message.chat.id
    await delete_chat_mess(bot, chat)
    await state.set_state(ChangeImageStates.IMAGE)
    await state.update_data(game_id=game_id)
    me = await call.message.answer(f"Прийшли нову картинку для гри", reply_markup=kb_cancel_but())
    await save_message(me)


   
@router.message(ChangeImageStates.IMAGE, F.photo)
async def edit_product_proc_image(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    game_id = data['game_id']
    photo = ''
    if message.photo:
        file_path = f'images/{uuid.uuid4()}.jpg'
        photo = message.photo[-1].file_id
    await bot.download(photo, destination=file_path)
    db.db_set_game_image_where_id(game_id, file_path)
    await state.clear()
    me = await message.answer(f"Картинка для гри змінена", reply_markup=kb_go_to_main_menu())
    await save_message(me)
