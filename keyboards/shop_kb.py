from aiogram import types
import random
from collections import defaultdict




def kb_set_lang():
    keys = [
        [types.InlineKeyboardButton(text='Українська', callback_data="ukrainian")],
        [types.InlineKeyboardButton(text='Російська', callback_data="russian")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_ukr_all_games(games):
    sorted_games = sorted(games, key=lambda game: game[1].lower())
    keys = []
    for game in sorted_games:
        if game[3] == 'немає':
            pass
        else:
            keys.append([types.InlineKeyboardButton(text=f'{game[1]}', callback_data=f"get_game_ukr_{game[0]}")])
    keys.append([types.InlineKeyboardButton(text='Назад до вибору мови', callback_data="go_to_lang")])
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_ukr_back():
    keys = [
        [types.InlineKeyboardButton(text='Назад', callback_data="ukrainian")],
        [types.InlineKeyboardButton(text='На головну', callback_data="go_to_lang")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb




def kb_rf_all_games(games):
    sorted_games = sorted(games, key=lambda game: game[1].lower())
    keys = []
    for game in sorted_games:
        if game[5] == 'немає':
            pass
        else:
            keys.append([types.InlineKeyboardButton(text=f'{game[1]}', callback_data=f"get_game_rf_{game[0]}")])
    keys.append([types.InlineKeyboardButton(text='Назад до вибору мови', callback_data="go_to_lang")])
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_rf_back():
    keys = [
        [types.InlineKeyboardButton(text='Назад', callback_data="russian")],
        [types.InlineKeyboardButton(text='На головну', callback_data="go_to_lang")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb



