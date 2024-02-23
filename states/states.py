from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Создаем класса, наследуемый от StatesGroup для группы состояний в FSM
class FSMMain(StatesGroup):

    pair_choice = State()              
    up_down_choice = State()   
    price_choice = State()         
    view_task = State