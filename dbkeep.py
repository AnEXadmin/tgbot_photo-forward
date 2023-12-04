import logging
import time
from datetime import date, datetime
from typing import List, Union
from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import Column, Integer, BigInteger, String, Sequence, TIMESTAMP, Boolean, DATE, JSON, and_, DateTime, distinct
from sqlalchemy import sql
#from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncEngine
#from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton,
                           CallbackQuery, LabeledPrice, PreCheckoutQuery, ReplyKeyboardMarkup, KeyboardButton, BotCommand)
import lists as txt
import menu as mn
from config import host, db_user, db_pass, db_name, TOKEN, root_id, admin_id, users_id, SQLE_URL

#engine: AsyncEngine = create_async_engine(SQLE_URL, echo=True)
#async_session = async_sessionmaker(engine)

db = Gino()




class Partner(db.Model):
    __tablename__ = 'partner'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    tgid = Column(Integer)
    name = Column(String(50))
    city = Column(String(50))
    kassa_name = Column(String(50))
    address = Column(String(500))
    photo = Column(String(500), default='-')
    money = Column(Integer, default=0)
    action = Column(String(50))
    quantity = Column(Integer, default=0)
    reserv_limit = Column(Integer, default=0)
    timechange = Column(DateTime, onupdate=datetime.now)
    timestart = Column(DateTime, default=datetime.now)
    query: sql.Select


class CMD:

    async def get_kassa(self):
        pass
    async def get_partner(self):
        pass
    async def get_money(self):
        pass
    async def change_money_in(int):
            pass
    async def change_money_out(int):
        pass
    async def change_money_reserv(int):
        pass
    async def get_stat(self):
        pass
    async def get_city(self) -> List:
 #       if req == 'city':
        result = await self.Partner.query.distinct(Partner.city).gino.all()
        return  result
    async def add_partner(**kwargs):
        newpart = await Partner(**kwargs).create()
        return newpart
    async def change_money(**kwargs):
        newchange = await Partner(**kwargs).create()
        return newchange

    async def add_kassa(**kwargs):
        newkassa = await Partner(**kwargs).create()
        return newkassa
async def kbmaker(param):
    req: object = await Partner.select('city', 'name', 'kassa_name').where(Partner.photo!='-').gino.all()
    n = await  Partner.select('name').where(Partner.photo!='-').gino.all()
    c = await  Partner.select('city').where(Partner.photo!='-').gino.all()
    k = await  Partner.select('kassa_name').where(Partner.photo!='-').gino.all()
    print('req:',req)
    btn= []
    x=0
    if param == 'city':
        while x<len(req):
            dtext = f'InlineKeyboardButton(text="{req[x][0]}:{req[x][2]}", callback_data="{x}")'
            btn.append(dtext)
            x+=1
            print('dtext:',dtext)
    print("btn:", btn)

    return btn

async def kbmake(param):
    ids = await Partner.select('id').where(Partner.photo!='-').gino.all()
    btn = InlineKeyboardMarkup(row_width=2)

    for id in ids:
        print(id[-1])
        n = await  Partner.select('name').where(Partner.id==id[-1]).gino.first()
        c = await  Partner.select('city').where(Partner.id==id[-1]).gino.first()
        k = await  Partner.select('kassa_name').where(Partner.id==id[-1]).gino.first()
        btn_text = f'{n[-1]} : {k[-1]}'
        callback_data = f"{id[-1]}"
        btn.insert(
            InlineKeyboardButton(text=btn_text,callback_data=callback_data)
        )
    print(btn)
    return btn

async def kassa_first(param):
    btn = InlineKeyboardMarkup(row_width=2)
    all_id = await Partner.select('id').where(Partner.photo != '-').gino.all()
    all_finded = await Partner.select().where(Partner.photo != '-').gino.all()
    if param == 'city':
        search = await Partner.select('city').distinct(Partner.city).gino.all()
        for x in search:
            c =  await Partner.select('city').where(Partner.city==x[-1]).gino.all()
            btn_text = f'{c[-1][-1]}'
            btn.insert(InlineKeyboardButton(text=btn_text, callback_data=btn_text))
        return btn
    elif param == 'partner':
        search = await Partner.select('name').distinct(Partner.name).gino.all()
        for x in search:
            n = await  Partner.select('name').where(Partner.name==x[-1]).gino.first()
            btn_text = f'{n[-1]}'
            btn.insert(InlineKeyboardButton(text=btn_text, callback_data=btn_text))
        return btn
    elif param == 'kassa':
        for id in all_id:
            k = await  Partner.select('kassa_name').where(Partner.id == id[-1]).gino.first()
            btn_text = f'{k[-1]}'
            callback_data = f"{id[-1]}"
            btn.insert(InlineKeyboardButton(text=btn_text, callback_data=btn_text))
        return btn
    elif param == 'all':
        for id in all_id:
            k = await  Partner.select('kassa_name').where(Partner.id == id[-1]).gino.first()
            btn_text = f'{k[-1]}'
            callback_data = f"{id[-1]}"
            btn.insert(InlineKeyboardButton(text=btn_text, callback_data=btn_text))
        return btn
    else:
        btn.insert(InlineKeyboardButton(text='Error, pls research', callback_data = 'cancel'))
    return btn

async def kassa_second(param,req, st):
    markup = InlineKeyboardMarkup(row_width=2)
    ids = await Partner.select('id').where(Partner.photo != '-').gino.all()
    if param == 'city':
        search = await Partner.select('id').where(and_(Partner.city==req, Partner.name==st)).gino.all()
    else:
        search = await Partner.select('id').where(and_(Partner.city == st, Partner.name == req)).gino.all()
    for id in ids:
        if id in search:
            kassa = await Partner.select('kassa_name').where(Partner.id==id[-1])
            btn_text = f'{kassa[-1]}'
            callback_data = f'{id[-1]}'
            btn.insert(InlineKeyboardButton(text=btn_text,callback_data=callback_data))
    return btn
async def ikb_partner_city(CallbackQuery, **kwargs):
    markup = InlineKeyboardMarkup(row_width=2)
    ids = await Partner.select('id').where(Partner.photo != '-').gino.all()
    std = await state.get_data()
    param = std.get('param')
    if param and callback_data:
        for id in ids:
            if param == 'city':
                chain = await Partner.select('name').where(
                    _and(Partner.city == callback_data, Partner.photo != '-')).gino.all()
            elif param == 'partner':
                chain = await Partner.select('city').where(
                    _and(Partner.name == callback_data, Partner.photo != '-')).gino.all()
            if id in chain:
                c = await Partner.select(Partner.kassa_name).where(Partner.id == id[-1]).gino.first()
                text = callback_data = f'"{c[-1]}"'
                markup.insert(
                    InlineKeyboardButton(text=text, callback_data=callback_data)
                )

    elif param:
        for id in ids:
            if param == 'city':
                chain = await Partner.select.distinct('name').where(Partner.photo != '-').gino.all()
            elif param == 'partner':
                chain = await Partner.select.distinct('city').where(Partner.photo != '-').gino.all()
            else:
                chain = await Partner.select().where(Partner.photo != '-').gino.all()
            if id in chain:
                c = await Partner.select(param).where(Partner.id == id[-1]).gino.first()
                text = callback_data = f'"{c[-1]}"'
                markup.insert(
                    InlineKeyboardButton(text=text, callback_data=callback_data)
                )
    return markup



async def show_ikb_kassa(param,req):
    markup = InlineKeyboardMarkup(row_width=2)
    ids = await Partner.select('id').where(Partner.photo != '-').gino.all()
    if param == 'partner':
        search = await Partner.select('id').where(Partner.name==req).gino.all()
    elif param == 'city':
        search = await Partner.select("city").where(Partner.city==req).gino.all()
    for id in ids:
        if id in search:
            kassa = await Partner.select('kassa_name').where(Partner.id==id[-1]).gino.all()
            text = f'{kassa[-1]}'
            callback_data = f'{id[-1]}'
            markup.insert(InlineKeyboardButton(text=text,callback_data=callback_data))
    return markup

async def photo_one(param):
    """
    take city|partner|all from call,
    check for call,
    make kb
    :return: inline keybord for next choice
    """
    btn = InlineKeyboardMarkup(row_width=2)
    all_id = await Partner.select('id').where(Partner.photo != '-').gino.all()
    all_finded = await Partner.select().where(Partner.photo != '-').gino.all()
    if param == 'city':
        search = await Partner.select('city').distinct(Partner.city).gino.all()
        for x in search:
            c = await Partner.select('city').where(Partner.city == x[-1]).gino.all()
            btn_text = f'{c[-1][-1]}'
            btn.insert(InlineKeyboardButton(text=btn_text, callback_data=btn_text))
        return btn
    elif param == 'partner':
        search = await Partner.select('name').distinct(Partner.name).gino.all()
        for x in search:
            n = await  Partner.select('name').where(Partner.name == x[-1]).gino.first()
            btn_text = f'{n[-1]}'
            btn.insert(InlineKeyboardButton(text=btn_text, callback_data=btn_text))
        return btn
    elif param == 'kassa':
        for id in all_id:
            k = await  Partner.select('kassa_name').where(Partner.id == id[-1]).gino.first()
            btn_text = f'{k[-1]}'
            callback_data = f"{id[-1]}"
            btn.insert(InlineKeyboardButton(text=btn_text, callback_data=btn_text))
        return btn
    elif param == 'all':
        for id in all_id:
            k = await  Partner.select('kassa_name').where(Partner.id == id[-1]).gino.first()
            btn_text = f'{k[-1]}'
            callback_data = f"{id[0]}"
            btn.insert(InlineKeyboardButton(text=btn_text, callback_data=btn_text))
        return btn
    else:
        btn.insert(InlineKeyboardButton(text='Error, pls research', callback_data='cancel'))
    return btn

async def photo_two(param, req):
    print(req)
    print(param)
    btn = InlineKeyboardMarkup(row_width=2)
    if param == 'partner':
        print('if')
        search = await Partner.select('city').distinct(Partner.city).where(Partner.name==req).gino.all()
        print('search by city:', search)
        for i in search:
            print(i)
            city = await Partner.select('city').distinct(Partner.city).gino.all()
            if i in city:
                text = f'{i[-1]}'
                btn.insert(InlineKeyboardButton(text=text, callback_data=text))
        return btn
    elif param == 'city':
        print('elif')
        search = await Partner.select('name').distinct(Partner.name).where(Partner.city==req).gino.all()
        print('search by name:',search)
        for i in search:
            name = await Partner.select('name').distinct(Partner.name).gino.all()
            if i in name:
                text = f'{i[-1]}'
                btn.insert(InlineKeyboardButton(text=text, callback_data=text))
        return btn

async def photo_three(param, req, st):

    markup = InlineKeyboardMarkup(row_width=2)
    ids = await Partner.select('id').where(Partner.photo != '-').gino.all()
    print('ids:',ids)
    if param == 'partner':
        search = await Partner.select('id').where(and_(Partner.name == str(req), Partner.city == str(st) )).gino.all()
        print('search:',search)
    else:
        search = await Partner.select('id').where(and_(Partner.city==str(req), Partner.name==str(st))).gino.all()
        print('els_search:', search)
    for i in ids:
        print(i[0])
        print(i)
        if i in search[:]:
            kassa = await Partner.select('kassa_name').where(Partner.id==i[0]).gino.first()
            print(kassa)
            text = f'{kassa[0]}'
            print(text)
            callback_data = f'{i[0]}'
            print(callback_data)
            markup.insert(InlineKeyboardButton(text=text,callback_data=callback_data))

    return markup



async def set_default_commands(bot: Bot):
    bot_commands = [
        types.BotCommand(command='/photo', description="гибкий выбор"),
        types.BotCommand(command='/kassa',description="выбор  текстом"),
        types.BotCommand(command='/add', description="добавить кассу"),
        types.BotCommand(command="/remove", description="удалить кассу"),
        ]
    return await bot.set_my_commands(bot_commands)
async def create_db():
    await db.set_bind(f'postgresql://{db_user}:{db_pass}@{host}/gino')
    # Create tables
    db.gino: GinoSchemaVisitor
#    await db.gino.drop_all()
    await db.gino.create_all()


class ikb():
    text = str
    callback_data = str