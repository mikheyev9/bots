import os
import sys
import time
import json
import random
import inspect
import traceback
import threading
import concurrent.futures

import colorama
from colorama import Fore, Back


class Threadize(threading.Thread):
    def __init__(self, to_thread, *args, **kwargs):
        threading.Thread.__init__(self)
        self.to_thread = to_thread
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.start()
        
    def run(self):
        self.result = self.to_thread(*self.args, **self.kwargs)
        if not self.result:
            self.result = True
        del self.args
        del self.kwargs
        del self.to_thread
            
    def wait(self):
        while not self.result:
            time.sleep(0.3)
        return self.result


def parse_aim(aim):
    kwargs = {}
    key = None
    if not isinstance(aim, list):
        return [[aim], kwargs, key]
    if len(aim) == 3:
        args, kwargs, key = aim
    if len(aim) == 2:
        if isinstance(aim[1], dict):
            args, kwargs = aim
        else:
            args, key = aim
    if len(aim) == 1:
        args = aim[0]
    if len(aim) == 0:
        args = []
    return args, kwargs, key


def pool(function, aims, max_threads):
    # aims = [
    #     [args, kwargs, key_to_find_result],
    #     [args2, kwargs2],
    #     [args3, key_to_find_result3],
    #     [args4],
    #     arg5
    # ]
    results = {}
    maims = []
    for aim in aims:
        maims.append(parse_aim(aim))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures_dict = {
            executor.submit(function, *args, **kwargs): key for args, kwargs, key in maims
        }
        for future in concurrent.futures.as_completed(futures_dict):
            key = futures_dict[future]
            try:
                result = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (aim, exc))
                result = None
            results[key] = result
    return results


def utf_ignore(str_):
    return str_.encode('cp1251', 'ignore').decode('cp1251', 'ignore')


def differences(left, right):
    # Returns items which are only in the
    # left array and only in the right array
    set1 = set(left)
    set2 = set(right)
    dif1 = list(set1 - set2)
    intersection = list(set1 & set2)
    dif2 = list(set2 - set1)
    return dif1, intersection, dif2


def green(mes):
    return Fore.GREEN + Back.RESET + str(mes) + default_fore + default_back


def red(mes):
    return Fore.RED + Back.RESET + str(mes) + default_fore + default_back


def blue(mes):
    return Fore.BLUE + Back.RESET + str(mes) + default_fore + default_back


def blueprint(mes):
    mes = Fore.BLUE + Back.RESET + str(mes) + default_fore + default_back
    print(mes)


def yellow(mes):
    return Fore.YELLOW + Back.RESET + str(mes) + default_fore + default_back


def colorize(mes, color):
    return color + default_back + str(mes) + default_fore


def lprint(mes, ChrTab=0, end='\n', only_log=False, prefix=True, cp1251=False, 
           utf8=True, color=None, filename='log.txt'):
    if ('#' in str(ChrTab)) and color:
        tab_num = double_split(ChrTab, '#', ' ')
        tab_num = colorize('#' + tab_num, color)
        right_part = ChrTab.split(' ', 1)[1]
        ChrTab = f'{tab_num} {right_part}'
    if isinstance(ChrTab, int):
        addition = f'Бот #{ChrTab}'
    else:
        addition = ChrTab
    if color:
        mes = colorize(mes, color)
    if prefix:
        if ChrTab:
            mes = f'{addition}: {mes}'
        else:
            mes = f'Главный: {mes}'
    encoding = None
    if cp1251:
        prefix = False
        only_log = True
        encoding = 'cp1251'
    elif utf8:
        encoding = 'utf-8'
    lmes = ''
    if prefix:
        lmes = time.asctime() + ' ' + mes + end
    else:
        lmes = mes + end
    try:
        with open(filename, 'a+', encoding=encoding) as logs:
            logs.write(lmes)
    except:
        print(colorize('Log file is used by another app', Fore.RED))
    if not only_log:
        print(mes, end=end)


def all_cond(conds):
    for cond in conds:
        if not cond:
            return False
    else:
        return True


def double_split(source, lstr, rstr):
    # Возвращает n-ый эелемент
    SplPage = source.split(lstr, 1)[1]
    SplSplPage = SplPage.split(rstr)[0]
    return SplSplPage


def inclusive_split(source, lstr, rstr, n=0):
    splitted = double_split(source, lstr, rstr, n=n)
    return lstr + source + rstr


def lrsplit(source, lstr, rstr):
    # Возвращает массив эелементов
    if not lstr in source:
        return []
    SplPage = source.split(lstr)
    SplPage.pop(0)
    SplSplPage = [splitted.split(rstr)[0] for splitted in SplPage]
    return SplSplPage


def contains(obj, slash='//'):
    xpath = f"{slash}*[contains(@class,'{obj}')]"
    return xpath


def class_names(obj, slash='//'):
    xpath = f"{slash}*[@class='{obj}']"
    return xpath


def fpass():
    pass


def find_by_value(dict_, value):
    for key in dict_:
        if dict_[key] == value:
            return key
    else:
        return None


def any_from(list_, str_):
    for elem in list_:
        if elem in str_:
            return True
    return False


def str_in_elem(list_, str_):
    for elem in list_:
        if str_ in elem:
            return True
    return False


def elem_in_str(list_, str_):
    return any_from(list_, str_)


def pp_dict(d):
    for key, value in d.items():
        print("{0}: {1}".format(key,value))


def lp_dict(d):
    mes_lines = []
    for key, value in d.items():
        mes_lines.append("{0}: {1}".format(key,value))
    mes = '\n'.join(mes_lines)
    lprint(mes)


def json_to_py(to_save, max_indent=5):
    to_strings = to_save.replace(r'\"', '').split('"')
    strings = to_strings[1::2]
    for string in strings:
        string = '"' + string + '"'
        to_save = to_save.replace(string, '"' + json.loads(string) + '"')
    indents = ' ' * max_indent * 4
    return to_save.replace(' true', ' True') \
                  .replace(' false', ' False') \
                  .replace(',\n' + indents + '    ', ', ') \
                  .replace('\n' + indents + '    ', '') \
                  .replace('\n' + indents + ']\n', ']\n') \
                  .replace('\n' + indents + '],\n', '],\n') \
                  .replace('\n' + indents + '}\n', '}\n') \
                  .replace('\n' + indents + '},\n', '},\n')


def p_json(string):
    dumped = json.dumps(string, indent=4)
    return json_to_py(dumped)


def pp_json(string):
    dumped = json.dumps(string, indent=4)
    print(json_to_py(dumped))


def randdigits(digits):
    str_ = ''
    for _ in range(digits):
        digit = random.randint(0, 9)
        str_ += str(digit)
    return str_


def multi_try(to_try,
              to_except,
              name='Sub',
              tries=3,
              trytry=True,
              obj='',
              ChrTab=0,
              print_errors=True,
              multiplier=1.14,
              args=None):
    # Выполняет to_try tries раз. Каждый
    # раз когда выполняется except в tryfunc,
    # выполняется и to_except. После первой
    # попытки выполнить to_try ожидается 0.7
    # секунд, далее ожидание нелинейно
    # увеличивается. 5е ожидание - 12,38 сек
    # Пятнадцатое ожидание уже 896 сек
    if args is None:
        args = []
    seconds = 3.0
    for i in range(tries):
        seconds = seconds ** multiplier
        success, error = tryfunc(to_try,
                                 name,
                                 trytry = trytry,
                                 ChrTab=ChrTab,
                                 print_errors=print_errors,
                                 args=args)
        if success:
            return True
        else:
            wait_time = seconds - 3.0
            if print_errors:
                mes = ''
                if 'Ожидание досрочно прервано' not in error:
                    mes += ' | '
                mes += 'Объект %s не обнаружен' % obj if obj else ''
                if 'Ожидание досрочно прервано' not in error:
                    mes += '. Жду %.1fс' % wait_time
                lprint(mes, ChrTab, prefix=False, color=Fore.YELLOW)
            tryfunc(to_except, 'Exception', trytry = trytry, ChrTab=ChrTab)
            if 'Ожидание досрочно прервано' not in error:
                time.sleep(wait_time)
    else:
        restricted = ['Main', 'Init', 'Sub']
        if (name not in restricted) and (tries != 1):
            raise RuntimeError('Превышено число попыток - ' + str(tries))
    return False


def tryfunc(func, name='', tries=1, trytry=False, ChrTab=0,
            print_errors=True, args=None):
    # Если код выполнился без ошибок, вернёт True
    # Если была ошибка, а tries == 1, вернёт False
    # Если была ошибка, а tries != 1, рэйзнет RuntimeError
    if args is None:
        args = []
    if not trytry:
        func(*args)
        return True, None
    printing_error = ''
    for i in range(tries):
        try:
            func(*args)
        except Exception as error:
            restricted = ['Main', 'Init', 'Sub']
            if (name not in restricted) and ('topping explicit waiting' in str(error)):
                raise RuntimeError('Ожидание досрочно прервано...')
            printing_error = str(error).split('\n')[0] if '\n' in str(error) else str(error)
            if print_errors:
                end_char = '\n' if name == 'Exception' else ''
                lprint(name + ': ' + printing_error, ChrTab, end=end_char, color=Fore.RED)
                lprint(name + ': ' + str(error), ChrTab, only_log=True, color=Fore.RED)
                lprint(traceback.format_exc(), ChrTab, only_log=True, prefix=False, color=Fore.RED)
        else:
            return True, None
    else:
        if tries == 1:
            return False, printing_error
        restricted = ['Main', 'Init', 'Sub']
        if name not in restricted:
            raise RuntimeError('Превышено число попыток - ' + str(tries))


def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


def reg_changes(item, key='1'):
    global reg_change_state
    if key not in reg_change_state:
        reg_change_state[key] = item
    if item != reg_change_state[key]:
        reg_change_state[key] = item
        return True
    else:
        return False


def delete_module(modname, paranoid=None):
    try:
        thismod = sys.modules[modname]
    except KeyError:
        raise ValueError(modname)
    these_symbols = dir(thismod)
    if paranoid:
        try:
            paranoid[:]  # sequence support
        except:
            raise ValueError('must supply a finite list for paranoid')
        else:
            these_symbols = paranoid[:]
    del sys.modules[modname]
    for mod in sys.modules.values():
        try:
            delattr(mod, modname)
        except AttributeError:
            pass
        if paranoid:
            for symbol in these_symbols:
                if symbol[:2] == '__':  # ignore special symbols
                    continue
                try:
                    delattr(mod, symbol)
                except AttributeError:
                    pass


def unicode_fix(unicode_str):
    unicode_str = unicode_str.replace('"', '[d_q]')
    dict_str = '{"str": "' + unicode_str + '"}'
    json_dict = json.loads(dict_str)
    json_dict['str'] = json_dict['str'].replace('[d_q]', '"')
    return json_dict['str']


colorama.init()
reg_change_state = {}
default_fore = Fore.RESET
default_back = Back.RESET
