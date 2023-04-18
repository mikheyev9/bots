import os
import sys
import json
from multiprocessing import Queue
from socketserver import *

import telebot
from telebot import types

s_path = os.path.dirname(os.path.abspath(__file__)).split('\\')[:-1]
sys.path.insert(0, '\\'.join(s_path) + '\\[MySources]')
root_path = '\\'.join(s_path)
import main_utils
from vis import *

DEBUG = True
tele_profiles_path = main_utils.get_source_path() + '\\tele_profiles.json'
with open(tele_profiles_path, 'r') as tele_profiles_json:
    TELE_PROFILES = json.load(tele_profiles_json)

def start_telebot(telegram_key):
    bot = telebot.TeleBot(telegram_key)
    proxies_json_path = main_utils.get_source_path() + '\\proxies.json'
    with open(proxies_json_path, 'r') as proxiesjson:
        proxies = json.load(proxiesjson)
    p_type, p_host, p_port, p_user, p_pass = main_utils.parse_proxy(proxies[1])
    telebot.apihelper.proxy = {'https':f'{p_type}://{p_user}:{p_pass}@{p_host}:{p_port}'}
    return bot


def get_tele_profiles():
    tele_profiles_path = main_utils.get_source_path() + '\\tele_profiles.json'
    with open(tele_profiles_path, 'r') as tele_profiles_json:
        tele_profiles = json.load(tele_profiles_json)
    return tele_profiles


class TeleHandler(main_utils.MyTCPHandler):
    def process_message(self, to_load):
        for mes, tele_ids in to_load:
            mes_tele_ids = [tele_id for tele_id in tele_ids if tele_id not in [454746771, 1128666119, 647298152]]
            if mes_tele_ids == []:
                profiles = ''
            else:
                profiles = '['
                for mes_tele_id in mes_tele_ids:
                    is_written = False
                    for profile, profile_data in TELE_PROFILES.items():
                        if mes_tele_id == profile_data[0]:
                            profiles += profile + ', '
                            is_written = True
                    
                    if not is_written:
                        profiles += str(mes_tele_id) + ', '
                profiles = profiles[:-2] + ']\n'
            
            others_mes = mes
            our_mes = profiles + mes
            
            for tele_id in tele_ids:
                if tele_id in [454746771, 1128666119, 647298152]:
                    mes = our_mes
                else:
                    mes = others_mes
                
                SenderThread.q.put([mes, tele_id])
            print(time.asctime().split()[-2], 'Got message!')

def trymethod(func):
    def wrapper(message, *args):
        try:
            func(message, *args)
        except Exception as exc:
            text = ('Что-то было введено не так и Вы были возвращены на первый шаг')
            SenderThread.bot.send_message(message.from_user.id, text=text)
            Commands.first(message)
    if DEBUG:
        return func
    return wrapper
            
class Commands:
    bot_common_names = []
    last_messages = {}
    
    with open('needed_params.json', encoding='utf-8') as f:
        needed_params = json.load(f)
    
    @staticmethod
    def save_message(message):
        sender = message.from_user.id
        if sender not in Commands.last_messages:
            Commands.last_messages[sender] = []
        Commands.last_messages[sender].append(message)
        
    @staticmethod
    def decrease_level(from_user, levels):
        for _ in range(levels):
            del Commands.last_messages[from_user][-1]
        
    @staticmethod
    def modify_white_list_keys(needed_events):
        for event in needed_events:
            white_list = event[3]['white_list']
            white_list_modified = {}
            for white_item in white_list:
                white_item_value = white_list[white_item]
                if white_item_value == '*':
                    white_list_modified[white_item] = '*'
                    continue
                white_item_modified = {}
                for row in white_item_value:
                    white_item_modified[int(row)] = white_item_value[row]
                white_list_modified[white_item] = white_item_modified
            event[3]['white_list'] = white_list_modified
        
    @staticmethod
    def load_message(from_user, back=True):
        print('----')
        if back:
            print([mes.text for mes in Commands.last_messages[from_user]])
            Commands.decrease_level(from_user, 1)
        print([mes.text for mes in Commands.last_messages[from_user]])
        last_mes = Commands.last_messages[from_user][-1]
        Commands.decrease_level(from_user, 1)
        return last_mes
    
    @staticmethod
    def load_common_names():
        def load_file():
            with open('bots.json', 'r', encoding='utf-8') as f:
                bot_common_names = json.load(f)
            return bot_common_names
        for _ in range(3):
            try:
                return load_file()
            except:
                lprint('Error loading file - common names')
                time.sleep(0.5)
        else:
            raise RuntimeError('Error loading file in 3 times')
        
    @staticmethod
    def get_needed(fpath):
        for _ in range(3):
            try:
                with open(fpath, encoding='utf-8') as needed:
                    needed_events = json.load(needed)
                Commands.modify_white_list_keys(needed_events) # nado chi ne nado?
                return needed_events
            except:
                lprint('Error loading file - needed events')
                time.sleep(0.5)
        else:
            raise RuntimeError('Error loading file in 3 times')

    @staticmethod
    def save_needed(fpath, needed_events, max_indent=5):
        for _ in range(3):
            try:
                to_save = json.dumps(needed_events, indent=4, ensure_ascii=False)
                indents = ' ' * max_indent * 4
                to_save = to_save.replace(',\n' + indents + '    ', ', ') \
                                 .replace('\n' + indents + '    ', '') \
                                 .replace('\n' + indents + ']\n', ']\n') \
                                 .replace('\n' + indents + '],\n', '],\n') \
                                 .replace('\n' + indents + '}\n', '}\n') \
                                 .replace('\n' + indents + '},\n', '},\n')
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(to_save)
                return True
            except:
                lprint('Error saving file')
                time.sleep(0.5)
        else:
            raise RuntimeError('Error saving file in 3 times')

    @staticmethod
    def filter_sectors(fpath, key):
        parent_path = '\\'.join(fpath.split('\\')[:-1])
        sectors_path = parent_path + '\\' + 'predefined_sectors.cfg'
        print(sectors_path)
        sectors = []
        for _ in range(3):
            try:
                with open(sectors_path, 'r', encoding='utf-8') as f:
                    sectors = f.read().split('\n')
                break
            except:
                lprint('Error loading file')
                time.sleep(0.5)
        else:
            raise RuntimeError('Error loading file in 3 times')
        return [sector for sector in sectors if key in sector]
        
    @staticmethod
    def go_back(message):
        text = ('Что-то было введено не так и Вы были возвращены на первый шаг')
        SenderThread.bot.send_message(message.from_user.id, text=text)
        Commands.first(message)

    @staticmethod
    def first(message):
        Commands.last_messages[message.from_user.id] = []
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('[Контрольная панель]')
        
        text = 'Для обновления списка ботов, нажимайте эту кнопку снова'
        Commands.save_message(message)
        SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
        SenderThread.bot.register_next_step_handler(message, Commands.show_cp)
        
    @trymethod
    def blacklist(message, fpath, event):
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('[Добавить]')
        
        for black_item in event[3]['black_list']:
            keyboard.row(black_item)
        keyboard.row('[Назад]')
        
        text = ('Это меню строк-исключений. Если любая из строк в '
                'блэклисте входит в название сектора, этот сектор будет '
                'игнорироваться ботом для откупки. Для того, чтобы'
                'удалить строку-исключение, просто нажмите на неё.')
        Commands.save_message(message)
        SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
        callback = lambda m: Commands.black_action(m, fpath, event)
        SenderThread.bot.register_next_step_handler(message, callback)
        
    @trymethod
    def whitelist(message, fpath, event):
        def str_filters(rows):
            if not rows:
                return '-Пусто-'
            if rows == '*':
                return '-Всё-'
            
            # row string
            row_nums = rows.keys()
            min_row = min(row_nums)
            max_row = max(row_nums)
            sample_span = set(range(min_row, max_row + 1))
            if set(row_nums) == sample_span:
                row_string = f'[{min_row}-{max_row}]'
            else:
                row_string = ', '.join([str(row) for row in row_nums])
            
            # seats string
            comparing_row = list(rows.values())[0]
            print(comparing_row)
            for row in list(rows.values()):
                if row != comparing_row:
                    seats_string = '-Custom-'
                    break
            else:
                if comparing_row == '*':
                    seats_string = '-Все-'
                else:
                    range_ = "-".join([str(extr) for extr in comparing_row])
                    seats_string = f'[{range_}]'
                    
            return f'Ряды {row_string}, Места {seats_string}'
            
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('[Добавить]')
        
        for white_item, white_filters in event[3]['white_list'].items():
            addition = str_filters(white_filters)
            white_item += ': ' + addition
            keyboard.row(white_item)
        keyboard.row('[Назад]')
        
        text = ('Это меню строк-вхождений. Если строка входит в название сектора, '
                'этот сектор будет использоваться ботом для откупки. То есть '
                'откупаться будет всё из whitelist. Если whitelist пустой, откупка'
                'не будет фильтроваться whitelist\'ом'
                'Для того, чтобы удалить строку-вхождение, просто нажмите на неё.')
        Commands.save_message(message)
        SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
        callback = lambda m: Commands.white_action(m, fpath, event)
        SenderThread.bot.register_next_step_handler(message, callback)
        
    @trymethod
    def parameters(message, fpath, event):
        keyboard = types.ReplyKeyboardMarkup(True, True)
        ev_params = {}
        for param in event[3]:
            if param == 'white_list':
                continue
            if param == 'black_list':
                continue
            if param not in Commands.needed_params:
                continue
            human_readable = Commands.needed_params[param][0]
            ev_param = f"[{human_readable}]: {event[3][param]}"
            ev_params[ev_param] = (param, event[3][param],)
            keyboard.row(ev_param)
        keyboard.row('[Назад]')
        
        text = 'Нажимайте на параметр, чтобы изменить его значение'
        Commands.save_message(message)
        SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
        callback = lambda m: Commands.change_parameter(m, fpath, event, ev_params)
        SenderThread.bot.register_next_step_handler(message, callback)
        
    @trymethod
    def change_parameter(message, fpath, event, pv_pairs):
        def change(params, param):
            available_options = Commands.needed_params[param][1]
            current_value = params[param]
            if current_value in available_options:
                index = available_options.index(current_value)
                index += 1
                if index == len(available_options):
                    index = 0
                new_option = available_options[index]
                params[param] = new_option
            else:
                params[param] = available_options[0]
            
        if message.text == '[Назад]':
            Commands.choose_event(Commands.load_message(message.from_user.id), fpath)
            return True
        else:
            parameter, value = pv_pairs[message.text]
        
            needed_events = Commands.get_needed(fpath)
            for needed_event in needed_events:
                if needed_event[0] == event[0]:
                    change(needed_event[3], parameter)
                    needed_event[3]['version'] += 1
                    change(event[3], parameter)
                    event[3]['version'] += 1
            Commands.save_needed(fpath, needed_events)
            
            last_command = Commands.load_message(message.from_user.id, False)
            Commands.parameters(last_command, fpath, event)
        
    @trymethod
    def black_action(message, fpath, event):
        if message.text == '[Назад]':
            Commands.choose_event(Commands.load_message(message.from_user.id), fpath)
            return True
        elif message.text == '[Добавить]':
            keyboard = types.ReplyKeyboardMarkup(True, True)
            keyboard.row('[Назад]')
            
            text = ('Введите строку-исключение. После ввода для удобства '
                    'будут указаны все сектора, которые будут исключены.')
                    
            Commands.save_message(message)
            SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
            callback = lambda m: Commands.black_add(m, fpath, event)
            SenderThread.bot.register_next_step_handler(message, callback)
        else:
            Commands.black_remove(message, fpath, event)
        
    @trymethod
    def white_action(message, fpath, event):
        def check_if_rows():
            white_sector = message.text.split(': ')[0]
            white_rows = event[3]['white_list'][white_sector]
            return (white_rows != '*') and white_rows
        if message.text == '[Назад]':
            Commands.choose_event(Commands.load_message(message.from_user.id), fpath)
            return True
        elif message.text == '[Добавить]':
            keyboard = types.ReplyKeyboardMarkup(True, True)
            keyboard.row('[Назад]')
            
            text = ('Введите строку-вхождение. После ввода для удобства '
                    'будут указаны все сектора, которые будут добавлены.')
            Commands.save_message(message)
            SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
            callback = lambda m: Commands.white_add(m, fpath, event)
            SenderThread.bot.register_next_step_handler(message, callback)
        else:
            keyboard = types.ReplyKeyboardMarkup(True, True)
            first_row = ['[Ограничить ряды]']
            # Ебануть здесь проверку - нужны ли ряды
            if check_if_rows():
                first_row.append('[Ограничить сбоку]')
            keyboard.row(*first_row)
            keyboard.row('[Удалить]', '[Назад]')
            
            text = ('Это меню редактирования строки-вхождения '
                    'На сектора, соответствующие этой строке могут '
                    'быть наложены ограничения по рядам или с краёв. '
                    'По умолчанию сектор не ограничен')
            Commands.save_message(message)
            SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
            callback = lambda m: Commands.white_edit(m, fpath, event, message.text)
            SenderThread.bot.register_next_step_handler(message, callback)
            
    @trymethod
    def param_action(message, fpath, event):
        if message.text == '[Назад]':
            Commands.choose_event(Commands.load_message(message.from_user.id), fpath)
            return True
        else:
            white_sector_name = white_sector.split(': ')[0]
            needed_events = Commands.get_needed(fpath)
            for needed_event in needed_events:
                if needed_event[0] == event[0]:
                    needed_event[3]['white_list'].pop(white_sector_name)
                    needed_event[3]['version'] += 1
                    event[3]['white_list'].pop(white_sector_name)
                    event[3]['version'] += 1
            Commands.save_needed(fpath, needed_events)
            SenderThread.bot.send_message(message.from_user.id, text='Удалено!')
            Commands.whitelist(Commands.load_message(message.from_user.id), fpath, event)
            
    @trymethod
    def white_edit(message, fpath, event, white_descr):
        if message.text == '[Назад]':
            Commands.whitelist(Commands.load_message(message.from_user.id), fpath, event)
        elif message.text == '[Удалить]':
            Commands.white_remove(message, fpath, event, white_descr)
        elif message.text == '[Ограничить ряды]':
            text = ('Введите ряды через запятую или диапазон. '
                    'Пробелы игнорируются. Если нужны все ряды, '
                    'отправьте "*" (без кавычек). Пример: 1, 3-5,6')
            keyboard = types.ReplyKeyboardMarkup(True, True)
            keyboard.row('[Назад]')
            
            Commands.save_message(message)
            SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
            callback = lambda m: Commands.white_restrict_rows(m, fpath, event, white_descr)
            SenderThread.bot.register_next_step_handler(message, callback)
        elif message.text == '[Ограничить сбоку]':
            text = 'Здесь допускается только один диапазон. Пример: 6-22'
            keyboard = types.ReplyKeyboardMarkup(True, True)
            keyboard.row('[Назад]')
            
            Commands.save_message(message)
            SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
            callback = lambda m: Commands.white_restrict_seats(m, fpath, event, white_descr)
            SenderThread.bot.register_next_step_handler(message, callback)
            
    @trymethod
    def black_remove(message, fpath, event):
        needed_events = Commands.get_needed(fpath)
        for needed_event in needed_events:
            if needed_event[0] == event[0]:
                needed_event[3]['black_list'].remove(message.text)
                needed_event[3]['version'] += 1
                event[3]['black_list'].remove(message.text)
                event[3]['version'] += 1
        Commands.save_needed(fpath, needed_events)
        
        SenderThread.bot.send_message(message.from_user.id, text='Удалено!')
        last_messages = Commands.load_message(message.from_user.id, False)
        Commands.blacklist(last_messages, fpath, event)
            
    @trymethod
    def white_remove(message, fpath, event, white_sector):
        white_sector_name = white_sector.split(': ')[0]
        needed_events = Commands.get_needed(fpath)
        for needed_event in needed_events:
            if needed_event[0] == event[0]:
                needed_event[3]['white_list'].pop(white_sector_name)
                needed_event[3]['version'] += 1
                event[3]['white_list'].pop(white_sector_name)
                event[3]['version'] += 1
        Commands.save_needed(fpath, needed_events)
        SenderThread.bot.send_message(message.from_user.id, text='Удалено!')
        Commands.whitelist(Commands.load_message(message.from_user.id), fpath, event)
        
    @trymethod
    def white_restrict_rows(message, fpath, event, white_descr):
        def str_range_to_list(str_):
            if str_ == '*':
                return '*'
            list_ = []
            str_ = str_.replace(' ', '')
            ranges = str_.split(',')
            for range_ in ranges:
                if '-' in range_:
                    min_row, max_row = range_.split('-')
                    int_range = list(range(int(min_row), int(max_row) + 1))
                    list_.extend(int_range)
                else:
                    list_.append(int(range_))
            return list_
            
        if message.text == '[Назад]':
            Commands.white_action(Commands.load_message(message.from_user.id), fpath, event)
            return True
        def to_try():
            rows = str_range_to_list(message.text)
            sector = white_descr.split(': ')[0]
            needed_events = Commands.get_needed(fpath)
            for needed_event in needed_events:
                if len(rows) > 50:
                    text = 'Ошибка! Максимум 50 рядов'
                    break
                if needed_event[0] != event[0]:
                    continue
                white_list = needed_event[3]['white_list']
                white_sector = white_list[sector]
                
                if (not white_sector) or (white_sector == '*'):
                    filler = [0, 100]
                else:
                    filler = list(white_sector.values())[0]
                if rows == '*':
                    to_white_list = '*'
                else:
                    filling_dict = dict.fromkeys(rows, filler)
                    to_white_list = filling_dict.copy()
                white_list[sector] = to_white_list
                event[3]['white_list'][sector] = to_white_list
                needed_event[3]['version'] += 1
                event[3]['version'] += 1
                
                Commands.save_needed(fpath, needed_events)
            
                text = 'Ограничения заданы.'
                break
            else:
                text = 'Что-то не так, обратитесь к Владу'
            SenderThread.bot.send_message(message.from_user.id, text=text)
            Commands.white_action(Commands.load_message(message.from_user.id), fpath, event)
        def to_except():
            text = 'Ошибка! Неверно заданы ограничения. Смотрите пример.'
            SenderThread.bot.send_message(message.from_user.id, text=text)
            Commands.white_action(Commands.load_message(message.from_user.id), fpath, event)
        multi_try(to_try, to_except, 'Sub', 1, True)
        
    @trymethod
    def white_restrict_seats(message, fpath, event, white_descr):
        def str_range_to_list(str_):
            str_ = str_.replace(' ', ' ')
            min_, max_ = str_.split('-')
            return [int(min_), int(max_)]
            
        if message.text == '[Назад]':
            Commands.white_action(Commands.load_message(message.from_user.id), fpath, event)
            return True
        try:
            range_ = str_range_to_list(message.text)
            sector = white_descr.split(': ')[0]
            needed_events = Commands.get_needed(fpath)
            for needed_event in needed_events:
                if needed_event[0] != event[0]:
                    continue
                white_list = needed_event[3]['white_list']
            
                for row in white_list[sector]:
                    white_list[sector][row] = range_
                for row in event[3]['white_list'][sector]:
                    event[3]['white_list'][sector][row] = range_
                needed_event[3]['version'] += 1
                event[3]['version'] += 1
                Commands.save_needed(fpath, needed_events)
            
                text = 'Ограничения заданы.'
                break
            else:
                text = 'Что-то не так, обратитесь к Владу'
        except:
            text = 'Ошибка! Неверно заданы ограничения. Смотрите пример.'
        SenderThread.bot.send_message(message.from_user.id, text=text)
        Commands.white_action(Commands.load_message(message.from_user.id), fpath, event)
            
    @trymethod
    def black_add(message, fpath, event):
        keyboard = types.ReplyKeyboardMarkup(True, True)
        if message.text == '[Назад]':
            Commands.blacklist(Commands.load_message(message.from_user.id), fpath, event)
            return True
        else:
            sectors = Commands.filter_sectors(fpath, message.text)
            keyboard.row('[Добавить]', '[Отмена]')
            
            text = 'Сектора, которые не будут учитываться согласно фильтру:\n'
            text += '\n'.join(['--' + sector for sector in sectors])
            text += '\n\nПодтвердите действие.'
            
            Commands.save_message(message)
            SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
            callback = lambda m: Commands.black_add_confirm(m, fpath, event, message.text)
            SenderThread.bot.register_next_step_handler(message, callback)
            
    @trymethod
    def white_add(message, fpath, event):
        keyboard = types.ReplyKeyboardMarkup(True, True)
        if message.text == '[Назад]':
            Commands.whitelist(Commands.load_message(message.from_user.id), fpath, event)
            return True
        else:
            sectors = Commands.filter_sectors(fpath, message.text)
            keyboard.row('[Добавить]', '[Отмена]')
            
            text = 'Сектора, которые будут учитываться согласно фильтру:\n'
            text += '\n'.join(['--' + sector for sector in sectors])
            text += '\n\nПодтвердите действие.'
            
            Commands.save_message(message)
            SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
            callback = lambda m: Commands.white_add_confirm(m, fpath, event, message.text)
            SenderThread.bot.register_next_step_handler(message, callback)
        
    @trymethod
    def black_add_confirm(message, fpath, event, sector):
        if message.text == '[Отмена]':
            Commands.black_action(Commands.load_message(message.from_user.id), fpath, event)
        else:
            needed_events = Commands.get_needed(fpath)
            for needed_event in needed_events:
                if needed_event[0] == event[0]:
                    needed_event[3]['black_list'].append(sector)
                    needed_event[3]['version'] += 1
                    event[3]['black_list'].append(sector)
                    event[3]['version'] += 1
            Commands.save_needed(fpath, needed_events)
            Commands.decrease_level(message.from_user.id, 1)
            SenderThread.bot.send_message(message.from_user.id, text='Добавлено!')
            Commands.blacklist(Commands.load_message(message.from_user.id), fpath, event)
        
    @trymethod
    def white_add_confirm(message, fpath, event, sector):
        if message.text == '[Отмена]':
            Commands.white_action(Commands.load_message(message.from_user.id), fpath, event)
        elif message.text == '[Добавить]':
            needed_events = Commands.get_needed(fpath)
            for needed_event in needed_events:
                if needed_event[0] == event[0]:
                    needed_event[3]['white_list'][sector] = '*'
                    needed_event[3]['version'] += 1
                    event[3]['white_list'][sector] = '*'
                    event[3]['version'] += 1
            Commands.save_needed(fpath, needed_events)
            Commands.decrease_level(message.from_user.id, 1)
            SenderThread.bot.send_message(message.from_user.id, text='Добавлено!')
            Commands.whitelist(Commands.load_message(message.from_user.id), fpath, event)
        else:
            Commands.go_back(message)
    
    @trymethod
    def delete_event(message, fpath, event):
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('[Удалить событие]', '[Назад]')
        
        text = 'Вы уверены что хотите удалить мероприятие и все его настройки?'
        Commands.save_message(message)
        SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
        callback = lambda m: Commands.delete_event_confirm(m, fpath, event)
        SenderThread.bot.register_next_step_handler(message, callback)
        
    @trymethod
    def delete_event_confirm(message, fpath, event):
        keyboard = types.ReplyKeyboardMarkup(True, True)
        if message.text == '[Назад]':
            Commands.choose_event(Commands.load_message(message.from_user.id), fpath)
        else:
            needed_events = Commands.get_needed(fpath)
            needed_events.remove(event)
            Commands.save_needed(fpath, needed_events)
            Commands.decrease_level(message.from_user.id, 1)
            Commands.choose_bot(Commands.load_message(message.from_user.id))
        
    @trymethod
    def command(message, fpath, event):
        def on_try(func):
            if DEBUG:
                func(message, fpath, event)
                return True
            try:
                func(message, fpath, event)
            except Exception as error:
                error = 'Ошибка при выполнении действия: ' + str(error)
                Commands.choose_bot(Commands.load_message(message.from_user.id))
                SenderThread.bot.send_message(message.from_user.id, text=error)
                printing_error = str(error).split('\n')[0] if '\n' in str(error) else str(error)
                name = 'Exception'
                end_char = '\n'
                lprint(name + ': ' + printing_error, end=end_char, color=Fore.RED)
                lprint(name + ': ' + str(error), only_log=True, color=Fore.RED)
                lprint(traceback.format_exc(), only_log=True, prefix=False, color=Fore.RED)
        if message.text == '[Назад]':
            Commands.choose_bot(Commands.load_message(message.from_user.id))
        elif message.text == '[Blacklist]':
            on_try(Commands.blacklist)
        elif message.text == '[Whitelist]':
            on_try(Commands.whitelist)
        elif message.text == '[Параметры]':
            on_try(Commands.parameters)
        elif message.text == '[Удалить]':
            on_try(Commands.delete_event)
        else:
            Commands.go_back(message)
        
    @trymethod  
    def choose_event(message, fpath):
        keyboard = types.ReplyKeyboardMarkup(True, True)
        if message.text == '[Назад]':
            Commands.show_cp(Commands.load_message(message.from_user.id))
            return True
        if message.text == '[Направлятель]':
            fpath = fpath.replace('\\needed.json', '\\to_needed.json')
            needed_events = Commands.get_needed(fpath)
            for event in needed_events:
                addition = '' if event[3]['buy_mode'] else '[Off] '
                keyboard.row(addition + event[0])
            keyboard.row('[Назад]')
                
            text = ('Здесь задаются настройки, по которым бот событий'
                    ' перенаправляляет на откупку мероприятия сразу как они появятся')
            Commands.save_message(message)
            SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
            callback = lambda m: Commands.sender(m, fpath)
            SenderThread.bot.register_next_step_handler(message, callback)
        else:
            event = []
            if message.text.startswith('[Off] '):
                message.text = message.text[6:]
                
            for event_ in Commands.get_needed(fpath):
                if event_[0] == message.text:
                    event = event_
                    break
            else:
                lprint('Event not found')
                Commands.go_back(message)
                return True
                
            options = [
                ['[Параметры]', '[Whitelist]'],
                ['[Удалить]', '[Назад]']
            ]
            for option in options:
                keyboard.row(*option)
                
            text = ('Для того чтобы исключить определённые сектора, добавьте '
                    'их в blacklist. Если же, наооборот, требуются только определённые '
                    'сектора - используйте whitelist. Если whitelist пуст, рассматриваются '
                    'все сектора (кроме, конечено, секторов, описанных в blacklist)')
            Commands.save_message(message)
            SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
            callback = lambda m: Commands.command(m, fpath, event)
            SenderThread.bot.register_next_step_handler(message, callback)
            
    @trymethod
    def choose_bot(message):
        keyboard = types.ReplyKeyboardMarkup(True, True)
        if message.text == '[Назад]':
            Commands.first(Commands.load_message(message.from_user.id))
            return True
        else:
            bot_name = find_by_value(Commands.bot_common_names, message.text)
            if bot_name == None:
                Commands.go_back(message)
                return True
            fpath = f"{root_path}\\{bot_name}\\needed.json"
            needed_events = Commands.get_needed(fpath)
            
            keyboard.row('[Назад]')
            keyboard.row('[Направлятель]')
            for event in needed_events:
                addition = '' if event[3]['buy_mode'] else '[Off] '
                keyboard.row(addition + event[0])
            
            text = 'Выберите событие, которые нужно отредактировать'
            Commands.save_message(message)
            SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
            callback = lambda m: Commands.choose_event(m, fpath)
            SenderThread.bot.register_next_step_handler(message, callback)
            
    @trymethod
    def show_cp(message):
        keyboard = types.ReplyKeyboardMarkup(True, True)
        
        Commands.bot_common_names = Commands.load_common_names()
        listdir = [dir_ for dir_ in os.listdir(root_path) if not dir_.endswith('.lnk')]
        bot_names = [dir_ for dir_ in listdir if dir_.startswith('bot_')]
        for bot_name in bot_names:
            if bot_name in Commands.bot_common_names:
                common_name = Commands.bot_common_names[bot_name]
                keyboard.row(common_name)
            
        keyboard.row('[Назад]')
        text = 'Выберите бота'
        Commands.save_message(message)
        SenderThread.bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
        SenderThread.bot.register_next_step_handler(message, Commands.choose_bot)
    
            
class SenderThread(threading.Thread):
    q = Queue()
    bot = start_telebot('924962518:AAGXdJHgfFOjx77PGlW99QtDUCrVG9etOlA')
    
    @bot.message_handler(content_types=['text'])
    def get_message(message):
        lprint('Телеграм: %s' % message.text, message.from_user.id)
        if '/delcookies' in message.text:
            arg = message.text.split(' ')[1]
            del_cookies(arg)
            
            SenderThread.bot.send_message(message.from_user.id, 'Кукисы удалены');
        elif (message.text == '/reg') or (message.text == '/start'):
            with open('telegram.json', 'r') as telejson:
                tele_ids = json.load(telejson)
            tele_ids.append(message.from_user.id)
            with open('telegram.json', 'w') as telejson:
                json.dump(tele_ids, telejson, indent=4)
            mes = 'Вы успешно зарегистрированы! Теперь Вы будете получать уведомления о билетах'
            SenderThread.bot.send_message(message.from_user.id, mes);
        elif '/bots' in message.text:
            Commands.first(message)
            
    def send_telegram(self, mes, tele_id):
        try:
            self.bot.send_message(tele_id, mes)
        except Exception as error:
            if 'Forbidden: bot was blocked by the user' in str(error):
                print(tele_id, 'blocked the bot')
            else:
                lprint('TELEGRAM ERROR ' + str(error))
                    
    def run(self):
        time_stamper = time.time()
        while True:
            final_messages = {}
            while (time.time() - time_stamper) < 0.5:
                if not self.q.empty():
                    mes, tele_id = self.q.get()
                    if tele_id not in final_messages:
                        final_messages[tele_id] = []
                    final_messages[tele_id].append(mes)
                else:
                    time.sleep(0.05)
            time_stamper = time.time()
            final_message_packs = {}
            for tele_id in final_messages:
                final_messages[tele_id].reverse()
                mes_collection = []
                final_mes = ''
                first_mes = True
                while final_messages[tele_id]:
                    mes = final_messages[tele_id].pop()
                    mes_collection.append(mes)
                    final_mes = '\n\n'.join(mes_collection)
                    if len(final_mes) > 4000:
                        if first_mes:
                            lprint(red('Слишком большое сообщение!'))
                            mes_collection = []
                            first_mes = True
                            continue
                        mes = mes_collection.pop()
                        final_messages[tele_id].append(mes)
                        if tele_id not in final_message_packs:
                            final_message_packs[tele_id] = []
                        final_message_packs[tele_id].append(mes_collection)
                        mes_collection = []
                    first_mes = False
                else:
                    if mes_collection:
                        if tele_id not in final_message_packs:
                            final_message_packs[tele_id] = []
                        final_message_packs[tele_id].append(mes_collection)
            else:
                counter = 0
                while counter < 8:
                    tele_ids_to_del = []
                    for tele_id in final_message_packs:
                        mes_collection = final_message_packs[tele_id].pop(0)
                        final_message = '\n\n'.join(mes_collection)
                        self.send_telegram(final_message, tele_id)
                        counter += 1
                        if not final_message_packs[tele_id]:
                            tele_ids_to_del.append(tele_id)
                    for tele_id in tele_ids_to_del:
                        del final_message_packs[tele_id]
                    if not final_message_packs:
                        counter = 100
                for tele_id in final_message_packs:
                    for mes_collection in final_message_packs[tele_id]:
                        for mes in mes_collection:
                            self.q.put([mes, tele_id])
    
def poll():
    to_try = lambda: SenderThread.bot.polling(none_stop=True)
    to_except = lambda: print(yellow('Polling error! Restarting...'))
    while True:
        multi_try(to_try, to_except, 'Main', 5, True)

def start_server():
    def stop_bot():
        time.sleep(0.3)
        input('Press Enter to close')
        raise os._exit(0)
        
    #Threadize(stop_bot)
    sender = SenderThread()
    sender.start()
    try:
        server = TCPServer(('185.203.119.33', 9105), TeleHandler)
        threading.Thread(target=poll).start()
        print('opened on 185.203.119.33')
    except:
        server = TCPServer(('localhost', 9105), TeleHandler)
        #threading.Thread(target=poll).start()
        print('opened on localhost')
    server.serve_forever()
    
if __name__ == '__main__':
    start_server()