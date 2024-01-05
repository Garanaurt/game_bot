from aiogram import types




def kb_cancel_but():
    keys = [
        [types.InlineKeyboardButton(text='Скасувати', callback_data="cancel_adding")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb



def kb_edit_game_proc(game_id):
    keys = [
        [types.InlineKeyboardButton(text='Змінити назву гри', callback_data=f"change_name_{game_id}")],
        [types.InlineKeyboardButton(text='Змінити посилання UA', callback_data=f"change_description_{game_id}")],
        [types.InlineKeyboardButton(text='Змінити посилання RU', callback_data=f"change_descriptionrf_{game_id}")],
        [types.InlineKeyboardButton(text='Змінити інструкцію UA', callback_data=f"change_instruction_{game_id}")],
        [types.InlineKeyboardButton(text='Змінити інструкцію RU', callback_data=f"change_instructionrf_{game_id}")],
        [types.InlineKeyboardButton(text='Змінити світлину з гри', callback_data=f"change_image_{game_id}")]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb



def kb_edit_game(games):
    sorted_games = sorted(games, key=lambda game: game[1].lower())
    keys = []
    for game in sorted_games:
        keys.append([types.InlineKeyboardButton(text=f'{game[1]}', callback_data=f"edit_game_{game[0]}")])
    keys.append([types.InlineKeyboardButton(text='Скасувати', callback_data="star")])
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb



def kb_go_to_main_menu():
    keys = [
        [types.InlineKeyboardButton(text='Назад', callback_data="star")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb




def kb_delete_game(games):
    sorted_games = sorted(games, key=lambda game: game[1].lower())
    keys = []
    for game in sorted_games:
        keys.append([types.InlineKeyboardButton(text=f'{game[1]}', callback_data=f"delete_game_{game[0]}")])
    keys.append([types.InlineKeyboardButton(text='Скасувати', callback_data="star")])
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_get_main_menu():
    keys = [
        [types.InlineKeyboardButton(text='Список ігр', callback_data="product_list_main")],
        [types.InlineKeyboardButton(text='Додати гру', callback_data="add_product_main")],
        [types.InlineKeyboardButton(text='Видалити гру', callback_data="del_product_main")],
        [types.InlineKeyboardButton(text='Редагувати гру', callback_data='edit_product_main')],
        ]  
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb






