from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types.base import String
from aiogram.types import Message, CallbackQuery

import dbkeep
import lists as txt
import menu as mn
import stateskeep as states
from config import admin_id, users_id
from dbkeep import CMD, Partner
from load_all import dp


def auth(func):
    async def wrapper(message):

        if message['from']['id'] in admin_id or message['from']['id'] in users_id:
            pass
        else:
            return await message.reply(text=txt.unreg, reply=False)

        return await func(message)

    return wrapper


@dp.message_handler(commands=["cancel"], state='*')
async def cancel(message: Message, state: FSMContext):
    """ remove state """
    await message.answer("Действие отменено")
    await state.reset_state()


@dp.message_handler(commands=['kassa'])
@auth
async def find_kassa(message: Message):
    req = await Partner.select('id', 'name', 'city', 'kassa_name').where(Partner.photo != '-').gino.all()
    req = str(req).replace('[', '').replace("'", "").replace(']', '').replace(')', '\n').replace(',', '').replace('(',
                                                                                                                  '')
    await message.answer(req)
    await message.answer('Введите номер кассы или /cancel')
    await states.Photo.Kassa.set()
    #


@dp.message_handler(state=states.Photo.Kassa)
async def kassa_photo(message: Message, state: FSMContext):
    kassa_id = message.text
    x = '0123456789'
    y = bool([i for i in kassa_id if i in x])
    if y:
        photo_req = await Partner.select('photo').where(Partner.id == int(kassa_id)).gino.all()
        info = await Partner.select('address').where(Partner.id == int(kassa_id)).gino.first()
        text_inf = info[0]
        file_id = photo_req[0][-1]
        await message.answer_photo(file_id, caption=text_inf)
        await state.reset_state()


@dp.callback_query_handler(text="mnBalance")
async def sh_nm_balances(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    result = str(callback_data[2:])
    st = callback_data[2:]
    text = f'yor choice {result} , press on buttons for next step or /cancel'
    markup = mn.choices
    await call.message.edit_reply_markup()
    await call.message.answer(text=text, reply_markup=markup)
    if st == 'Balance':
        await states.Balance.Start.set()
    elif st == 'Reserve':
        await state.set_state(states.Balance.Reserve_sh)
    elif st == 'Stat':
        await states.Stat.Start.set()
    await state.update_data({'s1': result})


@dp.callback_query_handler(text="bycity", state=states.Balance.Start)
async def input_city(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    req = await Partner.select('id', 'city', 'name', 'kassa_name', 'address').distinct(Partner.city).gino.all()
    await call.message.answer(req)


@dp.message_handler(commands=['money'])
@auth
async def show_money(message: Message):
    text = f'<b> MONEY MENU </b> \nif mistake press /chancel'
    btn = mn.operation
    await message.answer(text=text, reply_markup=btn)
    await states.Balance.Operation.set()


@dp.callback_query_handler(text="bypartner", state=states.Balance.Start)
async def input_city(call: CallbackQuery):
    req = await Partner.select('id', 'city', 'name', 'kassa_name', 'address', 'money').distinct(Partner.name).gino.all()
    await call.message.edit_reply_markup()
    await call.message.answer(req, reply_markup=mn.operation)
    await states.Balance.Operation.set()


@dp.callback_query_handler(state=states.Balance.Operation)
async def ch_operation(call: CallbackQuery, state: FSMContext):
    callback_data: String = call.data
    if 'money' not in callback_data:
        param = callback_data[6:]
        callback_data = 'reserv' + param
    else:
        callback_data = callback_data
    await state.update_data({'action': callback_data})
    await call.message.answer('enter quantity :')
    await states.Balance.Quantity.set()


@dp.message_handler(state=states.Balance.Quantity)
async def send_req(message: Message, state: FSMContext):
    quantity = message.text
    x = '0123456789'
    y = bool([i for i in quantity if i in x])
    if not y:
        text = 'please input numeric symbols or /cancel'
        await message.answer(text)

    else:
        await state.update_data({'quantity': quantity})
        shw = await Partner.select('id', 'name', 'city', 'kassa_name').gino.all()
        await message.answer(shw)
        await message.answer('enter id:')
        await states.Balance.Kassa.set()


@dp.message_handler(state=states.Balance.Kassa)
async def get_kassa_id(message: Message, state: FSMContext):
    std = await state.get_data()
    action = std.get('action')
    quantity = std.get('quantity')
    kassa_id = message.text
    tgid = message.from_user.id

    ids = await Partner.select('id').gino.all()
    if kassa_id not in str(ids):
        await message.answer('id not in list input num or press /cancel')
    else:
        kassa_name = await Partner.select('kassa_name').where(Partner.id == int(kassa_id)).gino.first()
        await state.update_data({'kassa_name': kassa_name})
        await state.update_data({'tgid': tgid})
        name = await Partner.select('name').where(Partner.id == int(kassa_id)).gino.first()
        await state.update_data({'name': name})
        text = f'action = {action}, quantity = {quantity},  kassa: {kassa_name} \nplease confirm or /cancel'
        await message.answer(text=text, reply_markup=mn.confirm)
        await states.Balance.Confirm.set()


@dp.callback_query_handler(state=states.Balance.Confirm)
async def do_confirm(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    std = await state.get_data()
    if callback_data != 'confirm':
        await call.message.answer('somthing wrong o_O please press /cancel and retry input')
    else:
        action = std.get('action')
        quantity = std.get('quantity')
        kassa_name = std.get("kassa_name")
        name = std.get('name')
        tgid = std.get('tgid')
        await Partner(Partner.tgid == tgid, Partner.name == name, Partner.kassa_name == kassa_name,
                      Partner.action == action, Partner.quantity == quantity).create()
        await call.message.answer(text="data is update!")
        await state.finish()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    chat_id = message.from_user.id
    if chat_id in users_id:
        await message.answer(txt.start)
    elif chat_id in admin_id:
        await message.answer(txt.start + txt.admin_cmd)

    else:
        await message.answer(txt.unreg)


@dp.message_handler(commands=['add'])
@auth
async def add_partner(message: types.Message):
    #
    await message.answer('Введите  <b> Имя Партнера </b> или жми /cancel')
    await states.NewPartner.Name.set()


#


@dp.message_handler(state=states.NewPartner.Name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    partner = Partner()
    partner.name = name
    await message.answer(("Имя партнера: {name}"
                          "\nВведи название города, или жми /cancel").format(name=name))

    await states.NewPartner.City.set()
    await state.update_data(partner=partner)


@dp.message_handler(state=states.NewPartner.City)
async def get_city(message: types.Message, state: FSMContext):
    city = message.text
    data = await state.get_data()
    partner: Partner = data.get('partner')
    partner.city = city
    await message.answer((f"Город: {city}"
                          "\nВведи имя кассы, или жми /cancel").format(city=city))
    await states.NewPartner.KassaName.set()
    await state.update_data(partner=partner)

@dp.message_handler(state=states.NewPartner.KassaName)
async def get_kassa_id(message: types.Message, state: FSMContext):
    kassa_name = message.text
    data = await state.get_data()
    partner: Partner = data.get('partner')
    partner.kassa_name = kassa_name
    await message.answer((f"Название кассы: {kassa_name}"
                          "\nПришли фото кассы, или жми /cancel").format(kassa_name=kassa_name))
    await states.NewPartner.Photo.set()
    await state.update_data(partner=partner)


@dp.message_handler(state=states.NewPartner.Photo, content_types=types.ContentType.PHOTO)
async def add_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    partner: Partner = data.get("partner")
    partner.photo = photo

    await message.answer_photo(
        photo=photo,
        caption=(("Партнер: {name}, город : {city} , касса: {kassa_name}"
                  "\nДобавь описание кассы (от 1 символа), или жми /cancel").format(name=partner.name,
                                                                                    city=partner.city,
                                                                                    kassa_name=partner.kassa_name)
                 ))
    await states.NewPartner.Address.set()
    await state.update_data(partner=partner)


@dp.message_handler(state=states.NewPartner.Address)
async def get_address(message: types.Message, state: FSMContext):
    #    result = message.text
    address = message.text
    data = await state.get_data()
    partner: Partner = data.get("partner")
    partner.address = address
    await message.answer(("Партнер: {name}, город : {city}, касса: {kassa_name}, описание: {address}"
                          "\nПодтвердить: /confirm отменить: /cancel").format(name=partner.name,
                                                                              address=partner.address,
                                                                              city=partner.city,
                                                                              kassa_name=partner.kassa_name))
    await states.NewPartner.Confirm.set()
    await state.update_data(partner=partner)

@dp.message_handler(state=states.NewPartner.Confirm)
async def do_confirm(message: types.Message, state: FSMContext):
    result = message.text
    data = await state.get_data()
    partner: Partner = data.get("partner")
    name = partner.name
    city = partner.city
    kassa_name = partner.kassa_name
    address = partner.address
    photo = partner.photo
    if result == '/confirm':
        await CMD.add_partner(name=name, city=city, kassa_name=kassa_name, photo=photo, address=address)
        await message.answer('Касса успешно добавлена!')
        await state.reset_state()
    else:
        await message.answer(f"Вы ввели: {result} \nПодтвердить: /confirm отмена: /cancel")



@dp.message_handler(commands=["partners"])
@auth
async def check_partners(message: types.Message):
    result = await Partner.select('id', 'name', 'city', 'kassa_name', 'address').gino.all()
    x = "'([]"
    text = str(result).replace("'), ", "\n").replace(",", " ")
    res: str = "".join(i for i in text if i not in x)
    res = res.replace(")", "").replace('"', '')
    await message.answer(res, reply_markup=mn.main_user)


@dp.message_handler(commands=["remove"])
@auth
async def remove_kassa(message: Message):
    req = await Partner.select('id', 'name', 'city', 'kassa_name').where(Partner.photo != '-').gino.all()
    req = str(req).replace('[', '').replace("'", "").replace(']', '').replace(')', '\n').replace(',', '').replace('(',
                                                                                                                  '')
    await message.answer(req)
    await message.answer('<b>Удаление кассы!!!</b> \nвведи номер удаляемой кассы, или жми /cancel')
    await states.Remove.Delete.set()


@dp.message_handler(state=states.Remove.Delete)
async def find_delete(message: Message, state: FSMContext):
    kassa_id = message.text
    ids = await Partner.select('id').where(Partner.photo != '-').gino.all()

    if kassa_id in str(ids):
        x = '0123456789'
        y = bool([i for i in kassa_id if i in x])
        if y:
            info = await Partner.select('id', 'name', 'city', 'kassa_name').where(
                Partner.id == int(kassa_id)).gino.first()
            text_inf = info[1] + info[2]
            await message.answer(f'Уверен, что нужно <b>УДАЛИТЬ</b> кассу? \n{text_inf}\n для отмены: /cancel',
                                 reply_markup=mn.confirm)
            await state.update_data(kassa_id=kassa_id)
            await states.Remove.Confirm.set()
        else:
            await message.answer('Не можешь набрать цифру - жми кнопку /cancel')
    else:
        await message.answer('Не можешь набрать цифру - жми кнопку /cancel\nЖду ввода цифры из первой колонки ...')


@dp.callback_query_handler(state=states.Remove.Confirm)
async def find_delete(call: CallbackQuery, state: FSMContext):
    std = await state.get_data()
    callback_data = call.data
    if callback_data == 'confirm':
        kassa_id = std.get('kassa_id')
        await Partner.delete.where(Partner.id == int(kassa_id)).gino.first()
        await call.message.edit_reply_markup()
        await call.message.answer('Касса удалена!')
        await state.finish()
    else:
        await call.message.answer('Отмена удаления!')
        await call.message.edit_reply_markup()
        await state.finish()


@dp.message_handler(commands=['city'])
async def get_city(message: Message):
    param = 'city'
    btn = await dbkeep.kbmake(param=param)
    await message.answer('city:', reply_markup=btn)


@dp.message_handler(commands=['photo'])
async def search_photo(message: Message):
    await message.answer('критерии выбора:',reply_markup=mn.choices)
    await states.Photo.Show.set()

@dp.callback_query_handler(state=states.Photo.Show)
async def param_for_photo(call: CallbackQuery, state: FSMContext):
    callback_data: str = call.data[2:]
    param = callback_data
    await call.message.edit_reply_markup()
    await state.update_data({'param': param})
    markup = await dbkeep.photo_one(param)
    await call.message.answer(text=param,reply_markup=markup)
    if param == 'kassa':
        await state.finish()
    elif param == 'all':
        await states.Photo.Finish.set()
    else:
        await states.Photo.Menu.set()

@dp.callback_query_handler(state=states.Photo.Menu)
async def ikb_form(call: CallbackQuery, state: FSMContext):
    std = await state.get_data()
    callback_data = call.data
    param = std.get('param')
    req = callback_data
    await state.update_data({'req': req})
    btn = await dbkeep.photo_two(param, req)
    await call.message.edit_reply_markup()
    await call.message.answer(text=callback_data, reply_markup=btn)
    await states.Photo.Last.set()

@dp.callback_query_handler(state=states.Photo.Last)
async def ikb_form(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    std = await state.get_data()
    param = std.get('param')
    req = std.get('req')
    st = callback_data
    markup = await dbkeep.photo_three(param, req, st)
    text = f'Список отбора по {req} {param} {st}:'
    await call.message.edit_reply_markup()
    await call.message.answer(text=text, reply_markup=markup)
    await states.Photo.Finish.set()

@dp.callback_query_handler(state=states.Photo.Finish)
async def ikb_photo_finish(call: CallbackQuery, state: FSMContext):
    callback_data = call.data
    photo_req = await Partner.select('photo').where(Partner.id == int(callback_data)).gino.first()
    info = await Partner.select('address').where(Partner.id == int(callback_data)).gino.first()
    text_inf = info[0]
    file_id = photo_req[0]
    await call.message.answer_photo(file_id, caption=text_inf)
    await call.message.edit_reply_markup()
    await state.finish()