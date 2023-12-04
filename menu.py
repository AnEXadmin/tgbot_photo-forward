from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton,
                           CallbackQuery, LabeledPrice, PreCheckoutQuery, ReplyKeyboardMarkup, KeyboardButton,
                           BotCommand)
choices = InlineKeyboardMarkup()
choices.row(InlineKeyboardButton('По городу', callback_data='bycity'),
            InlineKeyboardButton('По партнеру', callback_data='bypartner')
            )


choices1 = InlineKeyboardMarkup()
choices1.row(InlineKeyboardButton('Все', callback_data='shall'),
            InlineKeyboardButton('По городу', callback_data='bycity'),
            InlineKeyboardButton('По кассе', callback_data='bykassa'),
            InlineKeyboardButton('По партнеру', callback_data='bypartner')
            )


main_admin = InlineKeyboardMarkup()
main_admin.row(InlineKeyboardButton('Балансы', callback_data='mnBalance'),
            InlineKeyboardButton('Резервы', callback_data='mnReserv'),
            InlineKeyboardButton('Адреса', callback_data='mnAddress'),
            InlineKeyboardButton('Статистика', callback_data='mnStat')
            )

main_user = InlineKeyboardMarkup()
main_user.row(InlineKeyboardButton('Балансы', callback_data='mnBalance'),
             InlineKeyboardButton('Партнеры', callback_data='mnPartner'),
             InlineKeyboardButton('Адреса', callback_data='mnAddress'),
             InlineKeyboardButton('Operations', callback_data='mnOperations')

            )

operation = InlineKeyboardMarkup()
operation.row(InlineKeyboardButton('Снять', callback_data='money_out'),
             InlineKeyboardButton('Пополнить', callback_data='money_in'),
             InlineKeyboardButton('В резерв', callback_data='rserv_in'),
             InlineKeyboardButton('Из резерва', callback_data='rserv_out')
             )


chmoney = InlineKeyboardMarkup()
chmoney.row(InlineKeyboardButton('Балансы', callback_data='mn_balance'),
            InlineKeyboardButton('Резервы', callback_data='mn_reserv'),
            InlineKeyboardButton('Адреса', callback_data='addresses'),
            InlineKeyboardButton('Статистика', callback_data='mn_stat'))

confirm = InlineKeyboardMarkup()
confirm.add(InlineKeyboardButton('Confirm', callback_data='confirm'))

cancel = InlineKeyboardMarkup()
cancel.row(InlineKeyboardButton("Отмена", callback_data="Cancel"))