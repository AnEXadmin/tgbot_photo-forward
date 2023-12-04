from aiogram.dispatcher.filters.state import StatesGroup, State


class NewPartner(StatesGroup):
    Start = State()
    Name = State()
    City = State()
    KassaName = State()
    Photo = State()
    Address = State()
    Confirm = State()


class Balance(StatesGroup):
    Start = State()
    Balances = State()
    Show = State()  #all
    Operation = State()
    Money_sh = State() #step 1.1
    Money_in = State()
    Money_out = State()
    Reserve_sh = State()
    Reserve_in = State()
    Reserve_out = State()
    Quantity = State()
    Kassa = State()
    Confirm = State()

class Stat(StatesGroup):
    Start = State()
    User = State()
    Partner = State()

class Photo(StatesGroup):
    Show = State()
    Menu = State()
    Kassa = State()
    Last = State()
    Finish = State()
class Remove(StatesGroup):
    Show = State()
    Delete = State()
    Confirm = State()