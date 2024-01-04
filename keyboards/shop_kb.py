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
    keys = []
    for game in games:
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
    keys = []
    for game in games:
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
















def kb_go_to_main_menu(cities):
    keys = []
    for city in cities:
        key = [types.InlineKeyboardButton(text=f'{city[1]}', callback_data=f"shop_main_add_{city[0]}")]
        keys.append(key)
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_go_to_main_back():
    keys = [
        [types.InlineKeyboardButton(text='Назад', callback_data="shop_main")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_pick_location(distr):
    keys = []
    #msg = ''
    for key, val in distr.items():
        #msg += f'{key[0]} - {val[0]} шт\n'
        keys.append([types.InlineKeyboardButton(text=f'{key[0]}', callback_data=f"go_to_loc_{key[0]}")])
    keys.append([types.InlineKeyboardButton(text='MDMA-300мг', callback_data='to_magri')])
    keys.append([types.InlineKeyboardButton(text=f'Сменить город', callback_data=f"change_city")])
        
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb




def kb_buy_prod(button_args: dict):
    keys = []
    group_prod = {}
    for k, v in button_args.items():
        name_sort = k
        weights_product = []
        for product in v:
            grouped_products = {}
            if product[2] in weights_product:
                continue
            else:
                weights_product.append(product[2])
        for weight in weights_product:
                    pr = []
                    for product in v:
                        if product[2] == weight and product[9] == False and product[10] == False:
                            pr.append(product)
                    grouped_products[weight] = pr
        group_prod[name_sort] = grouped_products
        
    for sort_name, grouped_product in group_prod.items():
        for weight, product_group in grouped_product.items():
            produc = product_group[0]
            keys.append([types.InlineKeyboardButton(text=f'{sort_name} {int(produc[2])} г за {produc[4]} грн',
                                                 callback_data=f"buy_product_{produc[0]}")])
    keys.append([types.InlineKeyboardButton(text='Назад', callback_data='shop_main')])
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_change_purch_descr(product_id):
    keys = [
    ]
    keys.append([types.InlineKeyboardButton(text=f'Изменить комментарий по покупке', callback_data=f"change_purch_descr_{product_id}")])
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb



def kb_confirm_buy(id):
    keys = [
        [types.InlineKeyboardButton(text='MonoBank', callback_data=f"mono_process_pay_{id}")],
        [types.InlineKeyboardButton(text='CryptoBot', callback_data=f"crypto_process_pay_{id}")],
        #[types.InlineKeyboardButton(text='GeoPay', callback_data=f"geopay_process_pay_{id}")],
    ]
    keys.append([types.InlineKeyboardButton(text=f'Назад', callback_data=f"cancel_pay_{id}")])
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_cancel_but(product_id):
    keys = [
        [types.InlineKeyboardButton(text='Отмена', callback_data=f"cancel_adding_{product_id}")],
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

def kb_monobank_paid(summ, time, prod_id, card_in_cards):
    keys = [
        [types.InlineKeyboardButton(text='Оплачено', callback_data=f'monopaid_{summ}_{time}_{prod_id}_{card_in_cards}')],
        [types.InlineKeyboardButton(text='В чеке другое время', callback_data=f"mono_retry_pay_{prod_id}_{summ}_{card_in_cards}")],
        [types.InlineKeyboardButton(text='Отмена', callback_data=f"cancel_adding_{prod_id}")]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_cryptopay_keyboard(inv_id, inv_sum, product_id):
    keys = [
        [types.InlineKeyboardButton(text='Оплачено', callback_data=f'cryptopaid_{inv_id}_{inv_sum}_{product_id}')],
        [types.InlineKeyboardButton(text='Отмена', callback_data=f"cancel_adding_{product_id}")]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb


def kb_geopay_proces_pay(trade, product_id):
    keys = [
        [types.InlineKeyboardButton(text='Оплачено', callback_data=f'geopaid_{trade}_{product_id}')],
        [types.InlineKeyboardButton(text='Отмена', callback_data=f"cancel_adding_{product_id}")]
    ]
    kb = types.InlineKeyboardMarkup(inline_keyboard=keys)
    return kb

