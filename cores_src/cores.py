import io
import base64
import zipfile
import statistics

from screeninfo import get_monitors
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from .telecore import TeleCore, BillingCore
from . import main_utils, bot_socket
from .soup_driver import *
bot_socket.change_dir()
os.system('color 70')

TELE_PROFILES = {
    'misha': [593327317, 454277155],
    'misha_nekit': [593327317, 454277155],
    'only_misha': [593327317],
    'misha2': [580858479],
    'nekit': [454277155],
    'other': [],
    'sanya': [1653020880],
    'valera': [494440079],
    'we': [1653020880, 454277155],
    'me': [],
    'korben': [1743563751, 1320967532, 494440079],
    "abu": [1561247698],
    'andrey': [737762467, 836786118, 494440079],
    'seva': [671184187, 494440079],
    'vanya_sochi': [494440079, 1762475074],
    'vanya_office': [413874224],
    'piter': [174063933, 383791178],
    'elvina': [712759031],
    'yulya': [345109720],
    'ioann': [427840788],
    'olya': [472533395],
    'mama': [1271234019],
    'otdel': [593327317, 454277155, 494440079, 1653020880, 472533395],
    'sergey': [1351470607],
    'operator_bt': [],
    'helper_bt': []
}



class BotCore(threading.Thread):
    mode = 'bot'                    # 'bot' - зацикливаем, 'queue' - один раз проходим
    max_tries = 3                   # максимальное число попыток в конструкциях try-except
    tab_size = 60                   # ширина окна в процентах
    log_interval = 15               # интервал логирования телеграмма
    timeout = 30                    # таймаут прогрузки страницы
    max_waste_time = 180            # таймаут сессии
    driver_source = 'selenium'      # использовать ли селениум
    counter_step = 1                # Раз в сколько проходов выводить "Проход номер i"
    tele_bool = False               # отправлять ли уведомления в телеграм кому-то кроме меня
    release = True                  # unsafe mode
    headless = False                # невидимый хром
    listener = False                # выводить инофрмацию о соединении в логи
    retry = True                    # обновлять ли страницы через httpbin.org
    load_cookies_bool = False       # Загружить куки из cookies.json на первом проходе
    save_cookies_bool = False       # Сохранять куки после каждого прохода
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/96.0.4664.45 Safari/537.36')
                                    # какой user_agent подставлять. Возможны опции 'ChrTab' и 'random'
    api_key = 'f86fe003c5bc005f93a7516e2973658c' # RuCaptcha
    client_key = 'ebe8ee8e171f79095a4a4603cfa8b448' # Anti-Captcha
    proxy_centralized = True        # загружать ли из cores_src proxies.json
    listen_response = False         # listen_response JS inject (onLoad)
    listen_request_headers = False  # Записывать Headers исходящих запросов в localStorage['headers']
    listen_requests = False         # Записывать ли ответы всех запросов в консоль
    blocking_hosts = ('*.facebook.net', # Перенаправление запросов с определенных хостов localhost с целью блокировки скриптов
                      '*.facebook.com',
                      '*.google-analytics.com',
                      'mc.yandex.ru',
                      'vk.com')
    
    ChrTab = 0
    working = 0
    proxies_json_path = ''
    last_log_write = time.time()
    logs_buffer = ''
    cookies_on_tabs = []
    parse_logic = []
    user_agents = []
    first_names = [[]] * 4
    second_names = [[]] * 4
    emails = []
    adresses = []
    url_queue = []

    try:
        monitor = get_monitors()[0]
        scrw = monitor.width
        scrh = monitor.height
    except:
        scrw = 1080
        scrh = 720
    
    #Блок проверки прокси
    
    
    def __init__(self, ChrTab):
        threading.Thread.__init__(self)
        self.ChrTab = ChrTab
        BotCore.working += 1
        self.error_timer = time.time()
        self.bot_name = ''
        self.short_name = ''
        self.first = True
        self.progress = False
        self.terminator = False
        self.inspect_vanishing_lock = False
        self.user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                           '537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
        self.first_change = []
        self.events_state = {}
        self.tickets_state = {}
        self.events_for_check = {}
        self.check_counter = {}
        self.comments = {}
        self.proxies = []
        self.tele_ids = []
        self.cookies_string = ''
        self.last_call = 0
        self.plen = 0
        self.num = -1
        self.last_update = None
        self.tele_profile = []
        self.last_time_body = time.time()
    def __str__(self):
        if self.bot_name:
            chr_tab = str(self.ChrTab).ljust(3)
            return f'[{self.bot_name}#{chr_tab}]'
        else:
            return f'[Бот #{self.ChrTab}]' if self.ChrTab else f'[Главный бот]'
        
    def fill_url_queue(self, url, count):
        urls = [url] * count
        BotCore.url_queue.extend(urls)
    
    def get_proxy(self):
        """
        Строка файла JSON может быть представлена в виде:
        "type://ip:port" #лучше использовать для граббленых прокси
            без аутенфикацияя
        "type://ip:port@log:paa" #лучше использовать для граббленых
            прокси с аутенфикацией
        ["type", "host", port, "user", "pass"]
        ["host", port, "user", "pass"]
        ["type", "host", port]
        ["host", port]
        """
        if not self.proxies:
            if self.proxy_centralized:
                self.proxies_json_path = source_path + '\\proxies.json'
            else:
                self.proxies_json_path = 'json\\proxies.json'
            with open(self.proxies_json_path, 'r') as proxiesjson:
                self.proxies = json.load(proxiesjson)
        self.plen = len(self.proxies)
        i = (self.ChrTab - 1) % self.plen
        proxy = self.proxies[i]
        return main_utils.parse_proxy(proxy)
        
    def requests_proxies(self):
        ptype, host, port, user, pwd = self.get_proxy()
        proxies = {
            'http' : '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port),
            'https' : '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port)
        }
        return proxies
    
    def get_url(self):
        with open(r'json\urls.json', 'r') as urljson:
            urls = json.load(urljson)
        url = urls[self.ChrTab]
        return url

    def nullify_out_headers(self):
        self.driver.execute_script("localStorage['headers'] = new Map();")

    def get_out_headers(self):
        if not self.listen_request_headers:
            print('listen_request_headers == False')
            return None
        headers = self.driver.execute_script("return localStorage['headers']")
        try:
            headers_dd = json.loads(headers)
            headers_dict = {pair[0]: pair[1].replace("'''", '"') for pair in headers_dd}
        except:
            headers_dict = None
        return headers_dict
    
    def hrenium(self):
        driver = HrenDriver(ChrTab=self.ChrTab,
            proxies=self.requests_proxies(),
            user_agent=BotCore.user_agent)
        return driver
    
    def proxyfied_chrome(self, user_agent=None, add_headers=None):
        # Если ChrTab == 0, запустится браузер без прокси
        self.set_short_name()
        proxy_type, proxy_host, proxy_port, proxy_user, proxy_pass = self.get_proxy()
        if self.ChrTab:
            self.bprint('#%d Прокси: %s:%s@%s:%d' % (self.ChrTab,
                                                     proxy_user,
                                                     proxy_pass,
                                                     proxy_host,
                                                     proxy_port))
        else:
            self.bprint('Запущен с ОСНОВНОГО ip')
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "activeTab",
                "proxy",
                "tabs",
                "debugger",
                "unlimitedStorage",
                "storage",
                "http://*/*",
                "https://*/*",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            """
        if self.listen_response:
            manifest_json += """"content_scripts": [
                {
                    "matches": [
                        "http://*/*",
                        "https://*/*"
                    ],
                    "js": ["jquery.js", "content.js"],
                    "run_at": "document_start"
                }
            ],
            """
        manifest_json += """"web_accessible_resources": ["/listen_response.js"],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version": "22.0.0"
        }
        """
        background_js = ''
        if self.ChrTab:
            background_js += """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                      singleProxy: {
                        scheme: "%s",
                        host: "%s",
                        port: parseInt(%s)
                      },
                      bypassList: ["localhost"]
                    }
                  };
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            chrome.webRequest.onAuthRequired.addListener(
                        function callbackFn(details) {
                            return {
                                authCredentials: {
                                    username: "%s",
                                    password: "%s"
                                }
                            };
                        },
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """ % (proxy_type, proxy_host, proxy_port, proxy_user, proxy_pass)
        if self.listen_requests:
            background_js += """
            var currentTab;
            var version = "1.0";

            chrome.tabs.query( //get current Tab
                {
                    currentWindow: true,
                    active: true
                },
                function(tabArray) {
                    currentTab = tabArray[0];
                    chrome.debugger.attach({ //debug at current tab
                        tabId: currentTab.id
                    }, version, onAttach.bind(null, currentTab.id));
                }
            )
            function onAttach(tabId) {

                chrome.debugger.sendCommand({ //first enable the Network
                    tabId: tabId
                }, "Network.enable");

                chrome.debugger.onEvent.addListener(allEventHandler);

            }
            function allEventHandler(debuggeeId, message, params) {

                if (currentTab.id != debuggeeId.tabId) {
                    return;
                }

                if (message == "Network.responseReceived") { //response return 
                    chrome.debugger.sendCommand({
                        tabId: debuggeeId.tabId
                    }, "Network.getResponseBody", {
                        "requestId": params.requestId
                    }, function(response) {
                        alert(response)
                        chrome.debugger.detach(debuggeeId);
                    });
                }

            }
            """
        if self.listen_request_headers:
            background_js += """
            var all_headers = new Map();
            //var all_headers = [];
            chrome.webRequest.onBeforeSendHeaders.addListener(
                function(details) {
                    var headers = details.requestHeaders
                    for (var i = 0, l = headers.length; i < l; ++i) {
                        var sourceHeader = headers[i];
                        if (sourceHeader.name != 'Cookie') {
                            all_headers.set(sourceHeader.name, sourceHeader.value.replace(new RegExp('"','g'),"'''"));
                            json_headers = JSON.stringify([...all_headers]);
                            chrome.tabs.executeScript({code: "window.localStorage.setItem('headers', '" + json_headers + "');"});
                        }
                        //all_headers.push(sourceHeader.name + ': ' + sourceHeader.value);
                        //alert(sourceHeader.name + ': ' + sourceHeader.value);
                    }
                    blockingResponse = {}
                    blockingResponse.requestHeaders = details.requestHeaders;
                    return blockingResponse;
                },
                {urls: ['<all_urls>']},
                [ 'blocking', 'requestHeaders']
            );"""
        if add_headers:
            headers = [{'name': key, 'value': add_headers[key]} for key in add_headers.keys()]
            addHeaders = json.dumps(headers)
            background_js += f'var addHeaders = {addHeaders};'
            background_js += """
            var targetHeaders = [];
            chrome.webRequest.onBeforeSendHeaders.addListener(
                function(details) {
                    var headers = details.requestHeaders,
                            blockingResponse = {};
                    targetHeaders.splice(0, targetHeaders.length);
                    for (var i = 0, l = headers.length; i < l; ++i) {
                        var sourceHeader = headers[i];
                        targetHeaders.push({name: sourceHeader.name, value: sourceHeader.value});
                    }
                    for (var i = 0, l = addHeaders.length; i < l; ++i) {
                        var header = addHeaders[i];
                        targetHeaders.push({name: header.name, value: header.value});
                    }
                    blockingResponse.requestHeaders = targetHeaders;
                    return blockingResponse;
                },
                {urls: ['<all_urls>']},
                [ 'blocking', 'requestHeaders']
            );
            """
        if self.listen_response:
            content_js = """
            var s = document.createElement('script');
            s.src = chrome.extension.getURL('listen_response.js');
            s.onload = function() {
                this.remove();
            };
            (document.head || document.documentElement).appendChild(s);
            """
            listen_response_js = """
    (function(xhr) {

        var XHR = XMLHttpRequest.prototype;

        var open = XHR.open;
        var send = XHR.send;
        var setRequestHeader = XHR.setRequestHeader;
        var xhr_buffer = [];

        XHR.open = function(method, url) {
            this._method = method;
            this._url = url;
            this._requestHeaders = {};
            this._startTime = (new Date()).toISOString();
            console.log(this.response)

            return open.apply(this, arguments);
        };

        XHR.setRequestHeader = function(header, value) {
            this._requestHeaders[header] = value;
            return setRequestHeader.apply(this, arguments);
        };

        XHR.send = function(postData) {
            this.addEventListener('load', function() {
                var endTime = (new Date()).toISOString();

                var myUrl = this._url ? this._url.toLowerCase() : this._url;
                if(myUrl) {

                    if (postData) {
                        if (typeof postData === 'string') {
                            try {
                                // here you get the REQUEST HEADERS, in JSON format, so you can also use JSON.parse
                                this._requestHeaders = postData;    
                            } catch(err) {
                                console.log('Request Header JSON decode failed, transfer_encoding field could be base64');
                                console.log(err);
                            }
                        } else if (typeof postData === 'object' || typeof postData === 'array' || typeof postData === 'number' || typeof postData === 'boolean') {
                                // do something if you need
                        }
                    }

                    // here you get the RESPONSE HEADERS
                    var responseHeaders = this.getAllResponseHeaders();

                    if (this.responseType != 'blob') {
                        // responseText is string or null
                        try {
                            if (!this.responseText) {
                                console.log("Error in responseText");
                                return False
                            }
                            // here you get RESPONSE TEXT (BODY), in JSON format, so you can use JSON.parse
                            var arr = this.responseText;

                            // printing url, request headers, response headers, response body, to console
                            xhr_buffer.push([this._url, responseHeaders, arr])
                            window.localStorage.setItem('listened_responses', JSON.stringify(xhr_buffer))                        

                        } catch(err) {
                            console.log("Error in responseType try catch");
                            console.log(err);
                        }
                    }

                }
            });

            return send.apply(this, arguments);
        };

    })(XMLHttpRequest);
            """
        chrome_options = webdriver.ChromeOptions()
        if BotCore.headless:
            chrome_options.add_argument('--headless')
        if user_agent:
            if user_agent == 'ChrTab':
                user_agent = self.get_user_agent()
                chrome_options.add_argument('--user-agent=%s' % user_agent)
            elif user_agent == 'random':
                user_agent = self.get_user_agent(random_mode=True)
                chrome_options.add_argument('--user-agent=%s' % user_agent)
            else:
                chrome_options.add_argument('--user-agent=%s' % user_agent)
        else:
            chrome_options.add_argument('--user-agent=%s' % self.user_agent)
        if BotCore.blocking_hosts:
            stringed_rules = [f'MAP {host} 127.0.0.1' for host in BotCore.blocking_hosts]
            to_args = ', '.join(stringed_rules)
            chrome_options.add_argument(f'--host-rules={to_args}')
        pluginfile = ''
        if background_js:
            pluginfile = 'ext_' + str(self.ChrTab) + '.zip'
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr('manifest.json', manifest_json)
                zp.writestr('background.js', background_js)
                if self.listen_response:
                    zp.write(source_path + 'jquery.js', 'jquery.js')
                    zp.writestr('content.js', content_js)
                    zp.writestr('listen_response.js', listen_response_js)
                chrome_options.add_extension(pluginfile)
        try:
            driver = webdriver.Chrome(chrome_options=chrome_options)
        except Exception as exc:
            try:
                print(f'EXCEPTION {exc}, retrying')
                chrome_options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                driver = webdriver.Chrome(chrome_options=chrome_options)
            except Exception as exc:
                print(f'EXCEPTION {exc}, retrying')
                chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                driver = webdriver.Chrome(chrome_options=chrome_options)
        # delfile
        return driver

    def get_response(self, url, key):
        # needs listen_response switched to True
        script = "return window.localStorage['listened_responses']"
        for i in range(2, 20):
            start = time.time()
            saved_responses = self.driver.execute_script(script)
            if not saved_responses:
                time.sleep(2)
                continue
            resp_load = json.loads(saved_responses)
            for response in resp_load:
                resp_url = response[0]
                if url in resp_url:
                    return response[key]
            time.sleep(2 + i/5)
        else:
            raise RuntimeError(f'Не перехвачен запрос {url}')
            
    def get_response_body(self, url, load=False):
        response = self.get_response(url, 2)
        if load:
            return json.loads(response)
        return response
        
    def get_response_headers(self, url):
        return self.get_response(url, 1)

    def get_user_agent(self, random_mode=False):
        if not self.user_agents:
            agents_path = source_path + 'user_agents.txt'
            with open(agents_path, 'r') as f:
                file_text = f.read()
                self.user_agents = file_text.split('\n')
        user_agent = random.choice(self.user_agents)
        return user_agent
        
    def get_first_name(self, lang='rus', sex='m'):
        i1 = 0 if lang == 'eng' else 1
        i2 = 0 if sex == 'm' else 1
        arr_num = (i1 * 2) + i2
        if not self.first_names[arr_num]:
            names_path = source_path + f'register\\first_names_{arr_num}.txt'
            with open(names_path, 'r', encoding='utf-8') as f:
                file_text = f.read()
                self.first_names[arr_num] = file_text.split('\n')
        choice = random.choice(self.first_names[arr_num])
        return choice
        
    def get_mail(self, shuffle=False):
        if not BotCore.emails:
            with open('mails.txt', 'r', encoding='utf-8') as f:
                file_text = f.read()
                rows = file_text.split('\n')
                if shuffle:
                    random.shuffle(rows)
                BotCore.emails = rows
        choice = BotCore.emails.pop()
        return choice
        
    def get_second_name(self, lang='rus', sex='m'):
        i1 = 0 if lang == 'eng' else 1
        i2 = 0 if sex == 'm' else 1
        arr_num = (i1 * 2) + i2
        if not self.second_names[arr_num]:
            names_path = source_path + f'register\\second_names_{arr_num}.txt'
            with open(names_path, 'r', encoding='utf-8') as f:
                file_text = f.read()
                self.second_names[arr_num] = file_text.split('\n')
        choice = random.choice(self.second_names[arr_num])
        return choice

    def get_passport(self, country_code='RU'):
        if country_code == 'DE':
            digits = 9
            passport = 'C0'
            chars = '0123456789CFGHJKLMNPRTVWXYZ'
        elif country_code == 'DK':
            digits = 9
            passport = '2'
            chars = '0123456789'
        elif country_code == 'NL':
            digits = 9
            passport = 'S'
            chars = '0123456789ECP'
        elif country_code == 'PT':
            digits = 7
            passport = 'K'
            chars = '0123456789'
        elif country_code == 'FR':
            digits = 9
            passport = '0'
            chars = '0123456789CFGMNPTU'
        else:
            digits = 10
            passport = '4'
            chars = '0123456789'
        last_digits = [random.choice(chars) for i in range(digits - len(passport))]
        for digit in last_digits:
            passport += digit
        return passport
        
    def get_address(self, country_code='RU'):
        if not self.adresses:
            low_code = country_code.lower()
            names_path = source_path + f'register\\adresses_{low_code}.txt'
            with open(names_path, 'r', encoding='utf-8') as f:
                file_text = f.read()
                self.adresses = file_text.split('\n')
        street = random.choice(self.adresses)
        if country_code == 'RU':
            prefixes = ['улица', 'улица', 'ул.', 'шоссе', 'ул.', 'пр.', 'т.']
            separators = [', к.', '\\', '/',]
        else:
            prefixes = ['street', 'st.', 'avenue', 'av.', 'path', 'street', 'str.', 'Street', 'ul.', 'pr.']
            separators = [', b.', ', ']
        street_values = [random.choice(prefixes), street]
        separator = random.choice(separators)
        random.shuffle(street_values)
        street_name = ' '.join(street_values)
        house = random.randint(1, 78)
        building = random.choice([0, 0, 0, 0, 0, 0])
        flat = random.randint(1, 120)
        if building:
            numeric_name = f', {house}{separator}{building}, {flat}'
        else:
            numeric_name = f', {house}, {flat}'
        full_address = street_name + numeric_name
        return full_address
        
    def get_index(self, country_code='RU'):
        if country_code == 'RU':
            index = random.randint(101, 199) * 1000 + random.randint(2, 100)
        else:
            index = random.randint(10, 40) * 1000 + random.randint(2, 500)
        return str(index)
        
    def get_phone(self, country_code='RU'):
        if country_code == 'FR':
            return random.choice(['1', '4']) + ''.join([str(random.randint(0, 9)) for i in range(8)])
        elif country_code == 'PT':
            return '21' + ''.join([str(random.randint(0, 9)) for i in range(7)])
        elif country_code == 'DK':
            return '9' + ''.join([str(random.randint(0, 9)) for i in range(7)])
        elif country_code == 'NL':
            return '70' + ''.join([str(random.randint(0, 9)) for i in range(7)])
        else:
            return '9' + ''.join([str(random.randint(0, 9)) for i in range(9)])
            
    def get_birthday(self, drange=(1, 28,), mrange=(1, 12,), yrange=(1980, 2004,)):
        d = random.randint(*drange)
        m = random.randint(*mrange)
        y = random.randint(*yrange)
        return d, m, y

    def set_window(self, tab=0, n=1):
        scrw = BotCore.scrw
        tabw = float(BotCore.scrw) * self.tab_size / 100
        tabh = BotCore.scrh - 80
        if n == 0:
            n = 1
        self.driver.set_window_position(int((scrw - tabw) / n) * tab, 0)
        self.driver.set_window_size(tabw, tabh)
        
    def tprint(self, mes, only_log=False):
        #BotCore.logs_buffer += time.asctime() + ' ' + str(mes) + '\n'
        if not only_log:
            print(mes)
        #if (time.time() - BotCore.last_log_write) > BotCore.log_interval:
        #    with open(r'log.txt', 'a+', encoding='utf-8') as logs:
        #        logs.write(BotCore.logs_buffer)
        #    with open(source_path + 'log.txt', 'a+', encoding='utf-8') as logs:
        #        logs.write(BotCore.logs_buffer)
        #    BotCore.logs_buffer = ''
        #    BotCore.last_log_write = time.time()
        try:
            self.send_telegram(str(mes))
            with open(source_path + 'log.txt', 'a+', encoding='utf-8') as logs:
                logs.write(time.asctime() + ' ' + str(mes) + '\n')
        except Exception as err:
            with open(source_path + 'log.txt', 'a+', encoding='utf-8') as logs:
                logs.write(time.asctime() + ' ' + str(mes) + '\n')
            raise err
        
    def tprint_billing(self, mes, only_log=False):
        if not only_log:
            print(mes)
        with open(source_path + 'log.txt', 'a+', encoding='utf-8') as logs:
            logs.write(time.asctime() + ' ' + str(mes) + '\n')
        self.send_telegram(str(mes), billing=True)
        
    def cprint(self, mes):
        if (time.time() - self.last_call) < 600:
            return False
        self.last_call = time.time()
        json_path = 'json\\phones.json'
        if BotCore.tele_bool:
            with open(json_path, 'r') as read_file:
                phones_arr = json.load(read_file)
        else:
            phones_arr = ["+79104717002"]
        log_mes = 'ЗВОНОК: ' + mes + '\n'
        with open(r'log.txt', 'a', encoding='utf-8') as logs:
            logs.write(log_mes)
        with open(source_path + 'log.txt', 'a', encoding='utf-8') as logs:
            logs.write(log_mes)
        phones = ';'.join(phones_arr)
        params = {
           'login': 'OutOfMystic',
           'psw': 'Vlad12345123@',
           'phones': phones,
           'mes': mes,
           'call': '1'
           }
        r = requests.get('https://smsc.ru/sys/send.php', params=params)
        page = r.text
        print(mes)
        return True

    def java_click(self, elem):
        script = 'arguments[0].click()'
        self.driver.execute_script(script, elem)
        return True
        
    def insta_click(self, elem):
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(elem, 1, 1)
        actions.click()
        actions.perform()
        
    def expl_wait(self, ByWhat, obj, condition='presence', wait_time=15, print_errors=True):
        # Рефрешит страницу каждый раз, когда
        # выполняется exception в multi_try
        if self.driver_source == None:
            if not isinstance(self.driver, webdriver.Chrome):
                self.driver.expl_wait(ByWhat, obj)
        def to_try():
            if condition == 'visibility':
                WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((ByWhat, obj)))
            elif condition == 'presence':
                WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located((ByWhat, obj)))
            elif condition == 'clickable':
                WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable((ByWhat, obj)))
        def to_except():
            self.except_on_wait()
        max_tries = self.max_tries if self.release else 1
        res = multi_try(to_try, to_except, 'Wait', max_tries, self.release, obj=obj, ChrTab=self.short_name, print_errors=print_errors)
        return res
        
    def expl_wait_multi(self, elems, wait_time=15):
        # self.extra() should return True if
        # explicit waiting have to be stopped
        # right now to raise except_on_main
        # checking
        def to_try():
            start = time.time()
            while (time.time() - start) < wait_time:
                if any(self.driver.find_elements(*elem) for elem in elems):
                    break
                if self.extra():
                    raise RuntimeError('Stopping explicit waiting')
                time.sleep(2)
            if not any(self.driver.find_elements(*elem) for elem in elems):
                raise RuntimeError('Ни один объект не был обнаружен')
        def to_except():
            self.except_on_wait()
        obj = 'ожидания'
        res = multi_try(to_try, to_except, 'Wait', 1, self.release, obj=obj, ChrTab=self.short_name)
        return res
        
    def item_subsists(self, ByWhat, obj):
        # Когда просто нужна проверка, есть ли элемент на странице
        # Возвращает True если obj есть на странице
        if self.release:
            wait_time = 5
        else:
            wait_time = 3
        def to_try():
            WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located((ByWhat, obj)))
        res = tryfunc(to_try, 'Subsist', trytry=True, print_errors=False)
        return res

    def print_page(self, path='screen\\'):
        page = self.driver.page_source
        filename = path + str(time.asctime()) + '.html'
        filename = filename.replace(':', '') \
                           .replace(' ', '_')
        with open(filename, 'w+', encoding='utf-8') as f:
            f.write(page)
        
    def screen_page(self, path='screen\\'):
        filename = path + str(time.asctime()) + '.png'
        filename = filename.replace(':', '') \
                           .replace(' ', '_')
        self.driver.save_screenshot(filename)
        return filename
            
    def download(self, url, name=None, session=None, save=True, **kwargs):
        if not os.path.exists('downloads'):
            os.mkdir('downloads')
        if not session:
            r = requests.get(url, **kwargs)
        else:
            r = session.get(url, **kwargs)
        if not name:
            if 'content-disposition' in r.headers:
                disposition = r.headers['content-disposition']
                name = double_split(disposition, 'filename="', '"')
            else:
                name = url.split('/')[-1]
        addition = ''
        name_parts = name.split('.')
        if len(name_parts) > 1:
            format_ = '.' + name_parts.pop()
            name = '.'.join(name_parts)
        else:
            name = name_parts.pop()
            format_ = ''
        while os.path.exists(f'downloads\\{addition}{name}{format_}'):
            addition += '#'
        if save:
            with open(f'downloads\\{addition}{name}{format_}', 'wb+') as f:
                f.write(r.content)
            return r.text
        else:
            return r.content

    def load(self, url, cookies=True, retry=False):
        if self.driver_source == 'hrenium':
            return self.driver.load(url, cookies=cookies)
        if cookies:
            self.driver.get(url)
            self.driver.delete_all_cookies()
            if not self.cookies_on_tabs:
                with open(r'json\cookies.json', 'r') as read_file:
                    self.cookies_on_tabs = json.load(read_file)
            if self.ChrTab < len(self.cookies_on_tabs):
                cookies = self.cookies_on_tabs[self.ChrTab]
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
        if retry:
            self.driver.get('http://httpbin.org/ip')
        self.driver.get(url)
    
    def save_cookies(self):
        if not self.cookies_on_tabs:
            with open(r'json\cookies.json', 'r') as read_file:
                self.cookies_on_tabs = json.load(read_file)
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            del cookie['httpOnly']
            if cookie.get('expiry') != None:
                cookie['expiry'] = int(cookie['expiry'])
        length = len(self.cookies_on_tabs)
        if self.ChrTab >= length:
            count = self.ChrTab - length + 1
            empties = [[]] * count
            self.cookies_on_tabs.extend(empties)
        self.cookies_on_tabs[self.ChrTab] = cookies
        with open(r'json\cookies.json', 'w') as f:
            json.dump(self.cookies_on_tabs, f, indent=4)
            
    def del_cookies(self, aims):
        with open(r'json\cookies.json', 'r') as read_file:
            cookies_arr = json.load(read_file)
        if aims == '-a':
            for a in range(len(cookies_arr)):
                cookies_arr[a] = []
        else:
            cookies_arr[int(aims)] = []
        with open(r'json\cookies.json', 'w') as f:
            json.dump(cookies_arr, f, indent=4)
            
    def refresh_cookies(self, r, domain):
        old_cookies_arr = self.cookies_string.split('; ')
        old_cookies_spl = [old_cookie.split('=', 1) for old_cookie in old_cookies_arr]
        old_cookies_dict = {name: value for name, value in old_cookies_spl}
        new_cookies_dict = r.cookies.get_dict(domain=domain)
        for cookie in new_cookies_dict:
            old_cookies_dict[cookie] = new_cookies_dict[cookie]
        res_cookies = [cookie + '=' + old_cookies_dict[cookie] for cookie in old_cookies_dict]
        self.cookies_string = '; '.join(res_cookies)
        return True

    def first_check(self, by_what=None, by_value=None, condition='presence', wait_time=15):
        if self.driver_source == 'selenium':
            if not self.expl_wait(by_what, by_value, condition=condition, wait_time=wait_time):
                raise RuntimeError('--Не прогрузилась страница--')
        elif self.driver_source == 'hrenium':
            self.driver.first_check(by_what, by_value)
        else:
            if not self.r.text:
                RuntimeError('--Получил пустой ответ--')
            if self.r.status_code != 200:
                raise RuntimeError(f'--status code == {self.r.status_code}--')
            
    def first_check_multi(self, elems, wait_time=15):
        if not self.expl_wait_multi(elems, wait_time=wait_time):
            raise RuntimeError('--Не прогрузилась страница--')
        for i, elem in enumerate(elems):
            if self.driver.find_elements(*elem):
                return i
        else:
            return None

    def html_decode(self, text):
        return text \
        .replace(u"&amp;", u"&") \
        .replace(u"&quot;", u'"') \
        .replace(u"&#039;", u"'") \
        .replace(u"&lt;", u"<") \
        .replace(u"&gt;", u">")
    
    def send_telegram(self, mes, billing=False):
        if self.tele_bool:
            if not self.tele_ids:
                with open('json\\telegram.json', 'r') as telejson:
                    self.tele_ids = json.load(telejson)
            if billing:
                BillingCore.send_message(mes, self.tele_ids)
            else:
                TeleCore.send_message(mes, self.tele_ids)
        else:
            if billing:
                BillingCore.send_message(mes, [454746771, 647298152])
            else:
                TeleCore.send_message(mes, [454746771, 647298152])
    
    def send_telegram_to(self, mes, profiles):
        if not profiles:
            TeleCore.send_message(mes, [454746771, 647298152])
            return
        
        ids = get_tele_ids(profiles)
        TeleCore.send_message(mes, ids)
    
    def tprint_me(self, mes):
        print(mes)
        TeleCore.send_message(mes, [454746771, 647298152])
        
    def tprint_err(self, mes, billing=False):
        print(red(mes))
        to_send = f'{sys.argv[0]}: {mes}'
        if billing:
            BillingCore.send_message(to_send, [454746771, 647298152])
        else:
            TeleCore.send_message(to_send, [454746771, 647298152])
        raise RuntimeError(mes)
    
    def change_ticket_state(self,
                            key,
                            to_state,
                            url='',
                            comments={},
                            appeared='билеты',
                            separator=' ',
                            print_minus=True,
                            min_increase=5,
                            min_amount=2,
                            repeater=1,
                            repeat_delay=5,
                            cprint=False,
                            only_first=False,
                            fast=False):
        # to_state может быть передан как bool, list или dict
        # dict успользуем когда есть информация о количестве билетов
        # Если to_state передается списком, при release=False
        # не будет первого сообщения об отсутствии билетов
        # comments может быть передан как словарь или список
        def parse_state(to_state, instance):
            def del_state(state):
                if instance == 'list':
                    try:
                        new_to_state.remove(state)
                    except:
                        pass
                elif instance == 'dict':
                    new_to_state.pop(state, None)
            new_to_state = to_state.copy()
            if isinstance(self.parse_mode, list):
                if self.parse_mode[0] == 'THIS':
                    expecteds = self.parse_mode[1]
                    for state in to_state:
                        if all([expected not in state for expected in expecteds]):
                            del_state(state)
                    to_state = new_to_state.copy()
            for logic in self.parse_logic:
                for state in to_state:
                    act_foo, act_boo = logic.split('###')
                    if act_foo == 'NOT':
                        if act_boo in state:
                            del_state(state)
                            continue
            return new_to_state
        def check_for_repeat(to_state):
            if repeater == 1:
                return True
            if key not in self.check_counter:
                self.check_counter[key] = 0
            if isinstance(to_state, str):
                events_bool = to_state == self.tickets_state[key]
            else:
                new_events = [event for event in to_state if event not in self.tickets_state[key]]
                old_events = [event for event in self.tickets_state[key] if event not in to_state]
                events_bool = new_events or old_events
            if self.check_counter[key] == 0:
                if events_bool:
                    self.events_for_check[key] = to_state
                    self.check_counter[key] = 1
                    self.delay = repeat_delay
                    self.bprint('Detected different value, starting check (1)')
                    return False
                else:
                    return True
            else:
                if isinstance(to_state, str):
                    events_bool = self.events_for_check[key] == to_state
                else:
                    new_events_check = [event for event in to_state if event not in self.events_for_check[key]]
                    old_events_check = [event for event in self.events_for_check[key] if event not in to_state]
                    events_check_bool = new_events_check or old_events_check
                if events_check_bool:
                    if not events_bool:
                        self.delay = self.defeault_delay
                        self.bprint(yellow(f'Changes declined ({self.check_counter[key] + 1})'))
                        self.check_counter[key] = 0
                        return False
                    else:
                        self.delay = repeat_delay
                        self.bprint(yellow(f'Bot has got new instant changes ({self.check_counter[key]})'))
                        self.check_counter[key] = 0
                        self.tickets_state[key] = to_state
                        return False
                else:
                    self.check_counter[key] += 1
                    if self.check_counter[key] == repeater:
                        self.bprint(f'Value changes accepted ({self.check_counter[key]})')
                        self.check_counter[key] = 0
                        self.delay = self.defeault_delay
                        return True
                    else:
                        self.delay = repeat_delay
                        self.bprint(f'Checking values ({self.check_counter[key]})')
                        return False
        self.last_update = time.asctime()
        if self.first:
            self.defeault_delay = self.delay
        if not self.parse_logic:
            try:
                with open(r'json\parse_logic.json', 'r+', encoding='utf-8') as f:
                    loaded = json.load(f)
            except:
                print('No parse logic, exiting')
                raise SystemExit()
            self.parse_mode, self.parse_logic = loaded
        to_plus = []
        first_plus = []
        Appeared = appeared.capitalize()
        if isinstance(to_state, list):
            to_state = parse_state(to_state, 'list')
            tire_states = ['---' + state for state in to_state]
            lined_state = '\n'.join(tire_states)
            if key not in self.tickets_state:
                self.tickets_state[key] = to_state if self.release else []
            if key not in self.events_state:
                self.events_state[key] = []
            if key not in self.first_change:
                self.events_state[key] = list(set(self.events_state[key]) | set(to_state))
                threading.Thread(target=self.events_state_write, args=(key,)).start()
                self.first_change.append(key)
            
            no_repeat = check_for_repeat(to_state)
            if (set(self.tickets_state[key]) != set(to_state)) and no_repeat:
                mes = ''
                to_minus = [i for i in self.tickets_state[key] if i not in to_state]
                to_plus = [i for i in to_state if i not in self.tickets_state[key]]
                to_first_plus = [i for i in to_state if i not in self.events_state[key]]  # отсеиваю не новые
                if isinstance(comments, dict):
                    minus = [f'{state}{comments[state]}' for state in to_minus if state in comments]
                    minus += [f'{state}' for state in to_minus if state not in comments]
                    plus = [f'{state}{comments[state]}' for state in to_plus if state in comments]
                    plus += [f'{state}' for state in to_plus if state not in comments]
                    first_plus = [f'{state}{comments[state]}' for state in to_first_plus if state in comments]
                    first_plus += [f'{state}' for state in to_first_plus if state not in comments]
                else:
                    minus = [f'{state}{comment}' for state, comment in zip(to_minus, comments)]
                    plus = [f'{state}{comment}' for state, comment in zip(to_plus, comments)]
                    first_plus = [f'{state}{comment}' for state, comment in zip(to_first_plus, comments)]
                psep = ',' + separator
                if first_plus:
                    self.check_events_state(key, plus, first_plus)
                    first_plus_mes = psep.join(first_plus)
                    first_plus_mes = f"ВПЕРВЫЕ появились {appeared}. {key}: {separator}{first_plus_mes}\n"
                    mes += first_plus_mes
                if plus and not only_first:
                    plus_mes = psep.join(plus)
                    mes += f"Появились {appeared}. {key}:{separator}{plus_mes}"
                    if cprint:
                        self.cprint('Ахтунг. ' + mes)
                if print_minus:
                    if plus and minus:
                        mes += '\n'
                    if minus and not only_first:
                        minus_mes = psep.join(minus)
                        mes += f"{Appeared} исчезли из продажи. {key}:{separator}{minus_mes}"

                mes += f'\n{url}'
                if only_first:
                    if first_plus:
                        self.tprint(mes)
                elif print_minus:
                    self.tprint(mes)
                else:
                    if plus or first_plus:
                        self.tprint(mes)
            if no_repeat:
                self.tickets_state[key] = to_state
            if lined_state:
                lined_state = '\n' + lined_state
            if not self.release:
                self.lprint(f'Состояние билетов:{lined_state}', utf8=True)
            if first_plus and not fast:
                threading.Thread(target=self.events_state_write, args=(key,)).start()
            return to_plus
        elif isinstance(to_state, dict):
            to_state = parse_state(to_state, 'dict')
            listed_dict = [f'---{foo}: {boo}' for foo, boo in to_state.items()]
            lined_state = '\n'.join(listed_dict)
            refreshed_state = {}
            only_plus = []
            for i in to_state:
                if isinstance(to_state[i], str) or (to_state[i] >= min_amount):
                    refreshed_state[i] = to_state[i]
            if not (key in self.tickets_state):
                self.tickets_state[key] = refreshed_state.copy() if self.release else {}
            if key not in self.events_state:
                self.events_state[key] = []
            if key not in self.first_change:
                self.events_state[key] = list(set(self.events_state[key]) | set(self.tickets_state[key].keys()))
                threading.Thread(target=self.events_state_write, args=(key,)).start()
                self.first_change.append(key)
            
            no_repeat = check_for_repeat(refreshed_state)
            if (self.tickets_state[key] != refreshed_state) and no_repeat:
                to_minus = [[i, self.tickets_state[key][i]] for i in self.tickets_state[key] if i not in refreshed_state]
                to_plus = [[i, refreshed_state[i]] for i in refreshed_state if i not in self.tickets_state[key]]
                only_plus = [plus[0] for plus in to_plus]
                to_increase = []  # возможно снизу надо if not in self.tickets_state добавить
                to_first_plus = [[i, refreshed_state[i]] for i in refreshed_state if i not in self.events_state[key]]  # отсеиваю не новые
                only_first_plus = [f_plus[0] for f_plus in to_first_plus]
                for i in refreshed_state:
                    if i in self.tickets_state[key]:
                        if isinstance(refreshed_state[i], int):
                            if refreshed_state[i] > self.tickets_state[key][i]:
                                start = self.tickets_state[key][i]
                                diverg = refreshed_state[i] - start
                                if diverg >= min_increase:
                                    to_append = [i, diverg, start]
                                    to_increase.append(to_append)
                if isinstance(comments, dict):
                    minus = [f'{state[0]}{comments[state[0]]}' for state in to_minus if state[0] in comments]
                    minus += [f'{state[0]}' for state in to_minus if state[0] not in comments]
                    plus = [f'{state[0]}|{state[1]}{comments[state[0]]}' for state in to_plus if state[0] in comments]
                    plus += [f'{state[0]}|{state[1]}' for state in to_plus if state[0] not in comments]
                    first_plus = [f'{state[0]}|{state[1]}{comments[state[0]]}' for state in to_first_plus if state[0] in comments]
                    first_plus += [f'{state[0]}|{state[1]}' for state in to_first_plus if state[0] not in comments]
                    increase = [f'{state[0]}|{state[2]}{comments[state[0]]}| + {state[1]}шт' for state in to_increase if state[0] in comments]
                    increase += [f'{state[0]}|{state[2]}|+{state[1]}шт' for state in to_increase if (state[0] not in comments)]
                else:
                    minus = [f'{state[0]}{comment}' for state, comment in zip(to_minus, comments)]
                    plus = [f'{state[0]}|{state[1]}{comment}' for state, comment in zip(to_plus, comments)]
                    first_plus = [f'{state[0]}|{state[1]}{comment}' for state, comment in zip(to_first_plus, comments)]
                    increase = [f'{state[0]}{comment}|+{state[1]}шт' for state, comment in zip(to_increase, comments)]
                psep = ',' + separator
                to_mes = []
                if first_plus:
                    self.check_events_state_dict(key, plus, only_first_plus)
                    first_plus_mes = psep.join(first_plus)
                    first_plus_mes = f"ВПЕРВЫЕ появились {appeared}. {key}: {separator}{first_plus_mes}"
                    to_mes.append(first_plus_mes)
                if plus and not only_first:
                    plus_mes = psep.join(plus)
                    to_mes.append(f"Появились {appeared}. {key}:{separator}{plus_mes}")
                    if cprint:
                        self.cprint('Ахтунг. ' + ', '.join(to_mes))
                if increase:
                    increase_mes = psep.join(increase)
                    to_mes.append(f"{Appeared}: наличие увеличилось. {key}:{separator}{increase_mes}")
                if print_minus:
                    if minus and not only_first:
                        minus_mes = psep.join(minus)
                        to_mes.append(f"{Appeared} исчезли из продажи. {key}:{separator}{minus_mes}")
                to_mes.append(f'{url}')
                mes = '\n'.join(to_mes)
                if only_first:
                    if first_plus:
                        self.tprint(mes)
                elif print_minus:
                    if plus or first_plus or increase or minus:
                        self.tprint(mes)
                else:
                    if plus or first_plus or increase:
                        self.tprint(mes)
            if lined_state:
                lined_state = '\n' + lined_state
            if not self.release:
                self.lprint(f'Состояние билетов:{lined_state}', utf8=True)
            if no_repeat:
                self.tickets_state[key] = refreshed_state.copy()
            if first_plus and not fast:
                threading.Thread(target=self.events_state_write, args=(key,)).start()
            return only_plus
        else:
            if not (key in self.tickets_state):
                self.tickets_state[key] = to_state if self.release else None
            no_repeat = check_for_repeat(to_state)
            if (self.tickets_state[key] != to_state) and no_repeat:
                if to_state:
                    self.tprint(f'Появились {appeared}. {key}:\n{url}')
                    to_plus = [key]
                    if cprint:
                        self.cprint('Ахтунг. Появились билеты. ' + key)
                else:
                    if print_minus:
                        self.tprint(f'{Appeared} исчезли из продажи. {key}:\n{url}')
            if no_repeat:
                self.tickets_state[key] = to_state
            if not self.release:
                self.lprint(f'Состояние билетов:{to_state}', utf8=True)
            return to_plus

    def events_state_read(self):
        for i in range(2):
            try:
                with open('events_state.json', encoding='utf-8') as events_state:
                    self.events_state = json.load(events_state)
                    break
            except FileNotFoundError as e:
                print(yellow(f'Не удалось прочитать файл: {e}'))
                time.sleep(0.5)
            except json.decoder.JSONDecodeError as e:
                print(yellow(f'Не удалось прочитать файл, rewriting: {e}'))
                with open('events_state.json', 'w', encoding='utf-8') as events_state_json:
                    json.dump({}, events_state_json)
                time.sleep(0.5)
        else:
            with open('events_state.json', 'w', encoding='utf-8') as events_state_json:
                json.dump({}, events_state_json)
            print(green('Создан новый файл'))

    def events_state_write(self, key):
        try:
            with open('events_state.json', 'r', encoding='utf-8') as events_state:
                events_state_file = json.load(events_state)
            if key not in events_state_file:
                events_state_file[key] = self.events_state[key]
            else:
                events_state_file[key] += self.events_state[key]
                events_state_file[key] = list(set(events_state_file[key]))  # Скорее всего ивенты повторялись изза отутствия этой строчки, если проблема не решится, надо попробовать вынести ее за if
            with open('events_state.json', 'w', encoding='utf-8') as events_state_json:
                json_ = json.dumps(events_state_file, indent=4, ensure_ascii=False)
                events_state_json.write(json_)
        except Exception as err:
            print(yellow('Error writing events state. This may cause problems with events_state.json'))

    def check_events_state(self, key, plus, first_plus):
        self.events_state[key].extend(first_plus)
        for item in first_plus:
            plus.pop(plus.index(item))

    def check_events_state_dict(self, key, plus, first_plus):
        self.events_state[key].extend(first_plus)
        for item in first_plus:
            for item_ in plus:
                if item in item_:
                    plus.pop(plus.index(item_))
                    break
                    
    def proxy_to_string(self, p_type, p_user, p_pass, p_host, p_port):
        if p_user:
            return f'{p_type}://{p_host}:{p_port}@{p_user}:{p_pass}'
        else:
            return f'{p_type}://{p_host}:{p_port}'

    def check_proxies(self, url='http://httpbin.org/ip', method='get', concurrent=False,
                      personal=False, rewrite=True, **kwargs):
        if self.proxy_centralized:
            self.proxies_json_path = source_path + '\\all_proxies.json'
        else:
            self.proxies_json_path = 'json\\all_proxies.json'
        with open(self.proxies_json_path, 'r') as proxiesjson:
            proxies = json.load(proxiesjson)
        plen = len(proxies)

        threads = []
        for i, proxy in enumerate(proxies):
            sleep_time = random.random() * 30 if concurrent else 0
            def check(i, proxy):
                time.sleep(sleep_time)
                proxy_type, proxy_host, proxy_port, proxy_user, proxy_pass = main_utils.parse_proxy(proxy)
                proxies = {
                    'http' : '%s://%s:%s@%s:%d' % (proxy_type, proxy_user, proxy_pass, proxy_host, proxy_port),
                    'https' : '%s://%s:%s@%s:%d' % (proxy_type, proxy_user, proxy_pass, proxy_host, proxy_port)
                }
                try:
                    if method == 'get':
                        r = requests.get(url, proxies=proxies, timeout=5, **kwargs)
                    elif method == 'post':
                        r = requests.post(url, proxies=proxies, timeout=5, **kwargs)
                    status = 'Работает' if r.status_code == 200 else f'НЕ РАБОТАЕТ {r.status_code}'
                except:
                    status = 'НЕ РАБОТАЕТ'
                return i+1, proxy_type, proxy_user, proxy_pass, proxy_host, proxy_port, status
            threads.append(Threadize(check, i, proxy))
        good_proxies = []
        for thread in threads:
            i, proxy_type, proxy_user, proxy_pass, proxy_host, proxy_port, status = thread.wait()
            string_proxy = self.proxy_to_string(proxy_type, proxy_user, proxy_pass, proxy_host, proxy_port)
            if status == 'Работает':
                good_proxies.append(string_proxy)
            print(f'#{i} Прокси {proxy_host}:{proxy_port} {status}')
        a_len = len(good_proxies)
        print(f'Доступно {a_len} из {plen}')
        if not rewrite:
            print('Продолжение проверки...')
            return good_proxies
        input('Перезаписать ли файл прокси? ')
        if personal:
            rewrite_path = 'json\\proxies.json'
        else:
            rewrite_path = self.proxies_json_path.replace('all_proxies', 'proxies')
        with open(rewrite_path, 'w+') as proxiesjson:
            json.dump(good_proxies, proxiesjson, indent=4)
            
    def get_good_proxies(self, url, **kwargs):
        return self.check_proxies(url=url, rewrite=False, **kwargs)
            
    def slide_tab(self):
        self.ChrTab += 1
        if self.driver_source == 'selenium':
            self.driver.quit()
            self.driver = self.proxyfied_chrome(user_agent=BotCore.user_agent)
            self.driver.set_page_load_timeout(BotCore.timeout)
            self.set_window()
            self.driver.get(self.URL)
        elif self.driver_source == 'hrenium':
            self.driver.quit()
            self.driver = self.hrenium()
            self.driver.get(self.URL)
        else:
            self.before_body()
        return True

    def requests_cookies_to_string(self, r):
        dict_ = r.cookies.get_dict()
        res_cookies = []
        for cookie in dict_:
            res_cookies.append(cookie + '=' + dict_[cookie])
        cookies_string = '; '.join(res_cookies)
        return cookies_string

    def get_refreshed_cookies_from_r(self, old_cookies, r):
        old_cookies_arr = old_cookies.split('; ')
        old_cookies_spl = [old_cookie.split('=', 1) for old_cookie in old_cookies_arr]
        old_cookies_dict = {name: value for name, value in old_cookies_spl}
        new_cookies_dict = r.cookies.get_dict()
        for cookie in new_cookies_dict:
            old_cookies_dict[cookie] = new_cookies_dict[cookie]
        res_cookies = []
        for cookie in old_cookies_dict:
            res_cookies.append(cookie + '=' + old_cookies_dict[cookie])
        cookies_string = '; '.join(res_cookies)
        return cookies_string

    def get_cookies_string(self, domain):
        #SELENIUM COOKIES FROM DRIVER TO STRING
        if '://' in domain:
            domain = domain.split('://')[1]
        if '/' in domain:
            domain = domain.split('/')[0]
        if 'www.' in domain:
            domain.replace('www.', '')
        domain_spl = domain.split('.')
        domain = domain_spl[-2] + '.' + domain_spl[-1]
        all_cookies = self.driver.get_cookies()
        cookies = [cookie['name'] + '=' + cookie['value'] for cookie in all_cookies if domain in cookie['domain']]
        cookies_string = '; '.join(cookies)
        return cookies_string
         
    def driver_to_session(self, domain):
        if '://' in domain:
            domain = domain.split('://')[1]
        if '/' in domain:
            domain = domain.split('/')[0]
        if 'www.' in domain:
            domain.replace('www.', '')
        domain_spl = domain.split('.')
        domain = domain_spl[-2] + '.' + domain_spl[-1]
        all_cookies = self.driver.get_cookies()
        cookies = {cookie['name']: cookie['value'] for cookie in all_cookies if domain in cookie['domain']}
        session = main_utils.ProxySession(self)
        for cookie in cookies:
            session.cookies[cookie] = cookies[cookie]
        return session
        
    def session_to_driver(self, domain, session=None):
        if '://' in domain:
            domain = domain.split('://')[1]
        if '/' in domain:
            domain = domain.split('/')[0]
        if 'www.' in domain:
            domain.replace('www.', '')
            
        current_session = session if session else self.session
        cookies_dict = current_session.cookies.get_dict() #######
        cookies_selenium = []
        for name, value in cookies_dict.items():
            cookie_dict = {
                "domain": '.' + domain,
                "name": name,
                "path": "/",
                "value": value
            }
            cookies_selenium.append(cookie_dict)
        
        driver = self.proxyfied_chrome()
        driver.get('http://httpbin.org/ip')
        driver.delete_all_cookies()
        for cookie in cookies_selenium:
            driver.add_cookie(cookie)
        return driver
        
    def selenium_cookies_to_string(self, domain, chrtab):
        #SELENIUM COOKIES FROM FILE TO STRING
        if '://' in domain:
            domain = domain.split('://')[1]
        if '/' in domain:
            domain = domain.split('/')[0]
        if 'www.' in domain:
            domain.replace('www.', '')
        domain_spl = domain.split('.')
        domain = domain_spl[-2] + '.' + domain_spl[-1]
        with open('json\\cookies.json', 'r') as cookies_file:
            cookies = json.load(cookies_file)
            all_cookies = cookies[chrtab]
        cookies = [cookie['name'] + '=' + cookie['value'] for cookie in all_cookies if domain in cookie['domain']]
        cookies_string = '; '.join(cookies)
        return cookies_string
        
    def string_to_selenium_cookies(self, cookies_string, domain):
        #STRING TO SELENIUM COOKIES
        cookies_spl = cookies_string.split('; ')
        cookies_on_tab = []
        for cookie in cookies_spl:
            name, value = cookie.split('=', 1)
            cookie_dict = {
                "domain": '.' + domain,
                "name": name,
                "path": "/",
                "value": value
            }
            cookies_on_tab.append(cookie_dict)
        return cookies_on_tab

    def cookies_dict_to_string(self, cookies_dict):
        cookies_arr = [str(key) + '=' + str(cookies_dict[key]) for key in cookies_dict]
        cookies_string = '; '.join(cookies_arr)
        return cookies_string

    def get_number(self):
        api_url = 'http://sms-activate.ru/stubs/handler_api.php'
        api_key = '87991b90918A8d89b5df004924998d76'
        params = {'api_key': api_key,
            'service': 'ot',
            'action': 'getNumber',
            'forward': 0,
            'operator': 'any',
            'country': 0
        }
        r = requests.get(api_url, params=params)
        response = r.text
        print(response)
        if ':' not in response:
            print('ERROR: ', response)
            return False, False
        res, id, phone_num = response.split(':')
        print(id)
        return id, phone_num
        
    def get_sms(self, id):
        print('Ставлю статус:')
        api_url = 'http://sms-activate.ru/stubs/handler_api.php'
        api_key = '87991b90918A8d89b5df004924998d76'
        params = {'api_key': api_key,
            'id': id,
            'action': 'setStatus',
            'status': '1',
            'forward': 0
        }
        r = requests.get(api_url, params=params)
        response = r.text
        print(response)
        
        print('Получаю код:')
        response = ''
        time.sleep(5)
        for i in range(10):
            time.sleep(3)
            api_url = 'http://sms-activate.ru/stubs/handler_api.php'
            api_key = '87991b90918A8d89b5df004924998d76'
            params = {'api_key': api_key,
                'id': id,
                'action': 'getStatus'
            }
            r = requests.get(api_url, params=params)
            response = r.text
            print(response)
            if 'STATUS_OK' in response:
                res, sms = response.split(':', 1)
                return sms
        else:
            raise RuntimeError('Не приходит смс на номер!')
                
    def get_pass(self):
        my_bytes = random.getrandbits(72).to_bytes(10, byteorder='big', signed=True)
        string = base64.standard_b64encode(my_bytes).decode('utf-8')
        return string
        
    def solve_hcaptcha(self):
        page = self.driver.page_source
        site_key = double_split(page, 'data-sitekey="', '"')
        params = {
           'key': BotCore.api_key,
           'method': 'hcaptcha',
           'sitekey': site_key,
           'pageurl': self.driver.current_url,
           'json': '1'
        }
        r = requests.get('https://rucaptcha.com/in.php', params=params)
        print('rucaptcha.com: ' + r.text)
        try:
            response = json.loads(r.text)
        except:
            if r.text == 'ERROR_NO_SLOT_AVAILABLE':
                time.sleep(10)
            raise RuntimeError(f'Captcha error: {r.text}')
        status = response['status']
        if status:
            id = response['request']
            params = {
               'id': id,
               'action': 'get',
               'json': '1',
               'key': BotCore.api_key
               }
            time.sleep(10)
            for i in range(15):
                time.sleep(i * 1.5)
                r = requests.get('https://rucaptcha.com/res.php', params=params)
                response = json.loads(r.text)
                status = response['status']
                request = response['request']
                if status:
                    print(f'rucaptcha.com: status={status}')
                    to_execute = f"document.querySelector('[name=g-recaptcha-response]').innerText = '{request}'; " + \
                                 f"document.querySelector('[name=h-captcha-response]').innerText = '{request}'; " + \
                                  "document.querySelector('.challenge-form').submit()"
                    self.driver.execute_script(to_execute)
                    return True
                if request != 'CAPCHA_NOT_READY':
                    raise RuntimeError(f'Captcha error: {request}')
        raise RuntimeError('Не могут решить капчу')
        
    def solve_distil_recaptcha(self):
        self.solve_recaptcha_callback('solvedCaptcha')
        return True
        
    def solve_recaptcha_callback(self, callbackfn):
        payload = self.solve_recaptcha(type_code = False)
        script = f"return {callbackfn}('{payload}')"
        response = self.driver.execute_script(script)
        return True
        
    def solve_recaptcha_callback_dynamic(self, script_num=0):
        page = self.driver.page_source
        script_apis = lrsplit(page, 'https://www.google.com/recaptcha/api.js', '">')
        script_api = 'https://www.google.com/recaptcha/api.js'
        to_concat = self.html_decode(script_apis[script_num])
        script_api += to_concat
        headers = {
            'authority': 'www.google.com',
            'method': 'GET',
            'path': '/recaptcha/api.js' + to_concat,
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': self.driver.current_url,
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': self.user_agent
        }
        r = requests.get(script_api, headers=headers, proxies=self.requests_proxies())
        rpart = double_split(r.text, 'https://www.gstatic.com', "';")
        recaptcha__js = 'https://www.gstatic.com' + rpart
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'connection': 'keep-alive',
            'host': 'www.gstatic.com',
            'referer': self.driver.current_url,
            'user-agent': self.user_agent
        }
        r = requests.get(recaptcha__js, headers=headers, proxies=self.requests_proxies())
        literals = double_split(r.text, '[1]),-1),this.', '),this.')
        self.solve_recaptcha_callback(f'___grecaptcha_cfg.clients[0].{literals}.callback')
        
    def solve_recaptcha(self, type_code=True):
        page = self.driver.page_source
        if 'data-sitekey="' in page:
            key = double_split(page, 'data-sitekey="', '"')
        else:
            key = double_split(page, 'anchor?ar=1&amp;k=', '&')
        params = {
           'key': BotCore.api_key,
           'method': 'userrecaptcha',
           'googlekey': key,
           'pageurl': self.driver.current_url,
           'json': '1'
           }
        r = requests.get('https://rucaptcha.com/in.php', params=params)
        page = r.text
        self.lprint('rucaptcha.com: ' + page)
        response = json.loads(r.text)
        status = response['status']
        if status:
            id = response['request']
            params = {
               'id': id,
               'action': 'get',
               'json': '1',
               'key': BotCore.api_key
               }
            time.sleep(10)
            if type_code:
                for i in range(3):
                    try:
                        to_execute = f'var element = document.getElementsByName("g-recaptcha-response")[{i}];' \
                                    + 'element.style.display="block";'
                        self.driver.execute_script(to_execute)
                    except:
                        pass
            for i in range(15):
                time.sleep(i * 1.5)
                r = requests.get('https://rucaptcha.com/res.php', params=params)
                page = r.text
                response = json.loads(page)
                status = response['status']
                request = response['request']
                if status:
                    self.lprint('rucaptcha.com: status=%s' % status)
                    if type_code:
                        textareas = self.driver.find_elements_by_name('g-recaptcha-response')
                        for textarea in textareas:
                            try:
                                textarea.send_keys(request)
                            except:
                                pass
                        for i in range(3):
                            try:
                                to_execute = f'var element = document.getElementsByName("g-recaptcha-response")[{i}];' \
                                            + 'element.style.display="none";'
                                self.driver.execute_script(to_execute)
                            except:
                                pass
                        return True
                    return request
                if request != 'CAPCHA_NOT_READY':
                    raise RuntimeError(f'Captcha error: {request}')
        raise RuntimeError('Не могут решить капчу')
        
    def solve_recaptcha_v3(self, sitekey, action, pageurl, min_score=0.4):
        recaptcha_v3(sitekey, action, pageurl, min_score=min_score)
        return False
        
    def solve_distil_geetest(self):
        def get_ajax_header():
            page = self.driver.page_source
            defer_pos = page.find(r'" defer')
            str50 = page[defer_pos - 30 : defer_pos]
            dstl_js = str50.split('src="')[1]
            tmol_dstl = website_url + dstl_js
            headers = {
                'referer': self.driver.current_url,
                'sec-fetch-mode': 'no-cors',
                'user-agent': self.user_agent
            }
            if self.ChrTab:
                proxies = {
                    'http' : '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port),
                    'https' : '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port)
                }
                r = requests.get(tmol_dstl, headers=headers, proxies=proxies)
            else:
                r = requests.get(tmol_dstl, headers=headers)
            response = self.html_decode(r.text)
            dsplitted = double_split(response, '",ajax_header:"', '",')
            ajax_header = self.html_decode(dsplitted)
            return ajax_header
        page = self.driver.page_source
        gt = double_split(page, "gt: '", "' ,")
        got_challenge = self.get_response_body('_challenge')
        challenge = got_challenge.split(';')[0]
        ptype, host, port, user, pwd = self.get_proxy()
        href_spl = self.URL.split(r'://', 1)
        domain_l = href_spl[1].split(r'/', 1)
        domain = domain_l[0]
        page_path = domain_l[1]
        website_url = href_spl[0] + r'://' + domain + '/'
        x_distil_ajax = get_ajax_header()
        if 'www.' in domain:
            domain.replace('www.', '')
        all_cookies = self.driver.get_cookies()
        cookies = [cookie['name'] + '=' + cookie['value'] for cookie in all_cookies if domain in cookie['domain']]
        cookies_string = '; '.join(cookies)
        task = {
            'type': 'GeeTestTask',
            'websiteURL': self.URL,
            'gt': gt,
            'challenge': challenge,
            'geetestApiServerSubdomain': 'api-na.geetest.com',
            'proxyType' : ptype,
            'proxyAddress': host,
            'proxyPort': port,
            'proxyLogin': user,
            'proxyPassword': pwd,
            'cookies' : cookies_string,
            'userAgent': self.user_agent
        }
        params = {
           'clientKey': BotCore.client_key,
           'task' : task
        }
        r = requests.post('https://api.anti-captcha.com/createTask', json=params)
        
        page = r.text
        self.lprint('anti-captcha.com: ' + page)
        response = json.loads(r.text)
        error_id = response['errorId']
        if error_id:
            raise RuntimeError(f'anti-captcha.com: in.php error (code {error_id})')
        id = response['taskId']
        params = {
           'taskId': id,
           'clientKey': BotCore.client_key
        }
        page = self.driver.page_source
        dsplitted = double_split(page, 'name="dCF_ticket" type="hidden" value="', '"')
        dCF_ticket = self.html_decode(dsplitted)
        time.sleep(10)
        for i in range(100):
            time.sleep((i + 2) * 1.5)
            r = requests.post('https://api.anti-captcha.com/getTaskResult', json=params)
            page = r.text
            response = json.loads(page)
            error_id = response['errorId']
            if error_id:
                raise RuntimeError(f'GeeTest error: {error_id}')
                return False
            else:
                status = response['status']
                if status == 'ready':
                    self.lprint(f'anti-captcha.com: status={status}')
                    break
        solution = response['solution']
        request_id = ''
        referrer = '/' + page_path
        params = {
            'dCF_ticket': dCF_ticket,
            'geetest_challenge': solution['challenge'],
            'geetest_validate': solution['validate'],
            'geetest_seccode': solution['seccode'],
            'isAjax': 1
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'content-length': '366',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': cookies_string,
            'origin': website_url,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'referer': self.driver.current_url,
            'sec-fetch-mode': 'cors',
            'user-agent': self.user_agent,
            'x-distil-ajax': x_distil_ajax
        }
        time.sleep(1)
        
        page = self.driver.page_source
        mode = 'easy' if 'geetest_easy' in page else 'hard'
        dsplitted = double_split(page, f'class="geetest_{mode}" action="', '" method="post">')
        distil_r_captcha = self.html_decode(dsplitted)
        distil_r_captcha_href = website_url[:-1] + distil_r_captcha
        if self.ChrTab:
            proxies = {
                'http' : '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port),
                'https' : '%s://%s:%s@%s:%d' % (ptype, user, pwd, host, port)
            }
            r = requests.post(distil_r_captcha_href, data=params, headers=headers, proxies=proxies)
        else:
            r = requests.post(distil_r_captcha_href, headers=headers, json=params)
        self.driver.get(self.driver.current_url)
        
    def solve_image_element(self, element):
        captcha_image = element.screenshot_as_png
        im_io = io.BytesIO(captcha_image)
        solved_captcha = self.solve_image(im_io)
        return solved_captcha
        
    def solve_image(self, file, format_='png'):
        params = {
            'key': BotCore.api_key,
            'method': 'post',
            'json': '1',
        }
        files = {'file': (f'captcha.{format_}', file)}
        r = requests.post('https://rucaptcha.com/in.php', data=params, files=files)
        page = r.text
        response = json.loads(r.text)
        status = response['status']
        if status:
            id = response['request']
            params = {
               'id': id,
               'action': 'get',
               'json': '1',
               'key': BotCore.api_key
               }
            time.sleep(3)
            for i in range(20):
                time.sleep(i * 0.75)
                r = requests.get('https://rucaptcha.com/res.php', params=params)
                page = r.text
                response = json.loads(page)
                status = response['status']
                request = response['request']
                if status:
                    return request
                if request != 'CAPCHA_NOT_READY':
                    raise RuntimeError(f'Captcha error: {request}')
        else:
            raise RuntimeError(f'Captcha quest didn\'t started: {response}')
        print('rucaptcha.com: ' + page)

    @staticmethod
    def non_selenium_recaptcha(googlekey, url,
                               print_logs=True, timeout=160,
                               invisible=False, proxy=None,
                               user_agent=None):
        start_time = time.time()
        params = {
            'key': BotCore.api_key,
            'method': 'userrecaptcha',
            'googlekey': googlekey,
            'pageurl': url,
            'json': 1
        }
        if invisible:
            params['invisible'] = 1
            
        if proxy:
            proxy_type = proxy[0].upper()
            proxy_str = f"{proxy[3]}:{proxy[4]}@{proxy[1]}:{proxy[2]}"
            params['proxytype'] = proxy_type
            params['proxy'] = proxy_str
            
        if user_agent:
            params['userAgent'] = user_agent
            
        r = requests.post('https://rucaptcha.com/in.php', data=params)
        if print_logs:
            print('rucaptcha.com: ' + r.text)
        try:
            response = json.loads(r.text)
        except:
            raise RuntimeError('Captcha contain error: ' + r.text)
        status = response['status']
        if status:
            id = response['request']
            params = {
               'id': id,
               'action': 'get',
               'json': '1',
               'key': BotCore.api_key
               }
            time.sleep(7)
            while (time.time() - start_time) < timeout:
                time.sleep(5)
                r = requests.get('https://rucaptcha.com/res.php', params=params)
                try:
                    response = json.loads(r.text)
                except:
                    raise RuntimeError(f'Captcha error: {r.text}')
                status = response['status']
                request = response['request']
                if status:
                    if print_logs:
                        print('rucaptcha.com: ' + r.text)
                    return request
                if request != 'CAPCHA_NOT_READY':
                    raise RuntimeError(f'Captcha error: {request}')
        else:
            id_ = response['request']
            raise RuntimeError(f'Captcha init error: {id_}')
       
    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, 10000);")
        
    def inspect_vanishing(self, page):
        def print_page():
            self.inspect_vanishing_lock = False
            self.tprint(page) if len(page) < 4000 else self.screen_r(page)
            self.bprint('INSTANT VANISH DETECTED!')
        state = self.tickets_state[self.event_name]
        if isinstance(state, bool) or isinstance(state, list):
            if not state:
                print_page()
        elif isinstance(state, dict):
            state_copy = state.copy()
            keys_to_del = []
            for sector in state_copy:
                if state_copy[sector] < 2:
                    keys_to_del.append(sector)
            for key in keys_to_del:
                del state_copy[key]
            if not state_copy:
                print_page()
    
    def lprint(self, mes, **kwargs):
        if self.short_name:
            if 'color' not in kwargs:
                kwargs['color'] = Fore.GREEN
        lprint(mes, self.short_name, **kwargs)
    
    def bprint(self, mes, color=Fore.GREEN):
        if self.bot_name:
            chr_tab = str(self.ChrTab).ljust(3)
            mes = f'{self.bot_name}#{chr_tab}| {colorize(mes, color)}\n'
        else:
            mes = f'Бот {self.ChrTab}: {mes}\n' if self.ChrTab else f'Главный: {colorize(mes, color)}\n'
        print(mes, end='')
    
    def refresh(self):
        url = self.driver.current_url
        self.driver.get('http://httpbin.org/ip')
        self.driver.get(url)
        return True
        
    def back(self):
        self.driver.get('http://httpbin.org/ip')
        self.driver.get(self.URL)
        return True
    
    def except_on_main(self):
        if self.driver_source == 'selenium':
            self.back()
        
    def extra(self):
        # dont paste huge code here
        # if True, expl_wait_multi will be stopped
        return False
        
    def except_on_wait(self):
        self.driver.get(self.driver.current_url)
    
    def before_body(self):
        pass
    
    def on_errors(self):
        pass

    def show_consts(self):
        to_mes = []
        if self.driver_source:
            to_mes.append(self.driver_source)
        if self.release:
            to_mes.append('release')
        if self.tele_bool:
            to_mes.append('tele_bool')
        if self.driver_source == 'selenium':
            if self.retry:
                to_mes.append('retry')
            if self.headless:
                to_mes.append('headless')
        print('; '.join(to_mes))
    
    def record_body_time(self):
        self.last_time_body = time.time()

    def bot_mode(self, multi=False):
        self.events_state_read()
        if not multi:
            bot_socket.run_socket([self])
        self.show_consts()
        self.num = -1
        if self.driver_source == 'selenium':
            self.driver = self.proxyfied_chrome(user_agent=BotCore.user_agent)
            self.driver.set_page_load_timeout(BotCore.timeout)
            self.set_window()
        elif self.driver_source == 'hrenium':
            self.driver = self.hrenium()
        self.before_body()
        def to_try():
            if self.driver_source:
                if self.load_cookies_bool:
                    self.load(self.URL, self.first, retry=self.retry)
                else:
                    self.load(self.URL, False, retry=self.retry)
            if self.terminator:
                return False
            self.body()
            self.record_body_time()
            if self.driver_source:
                if self.inspect_vanishing_lock:
                    self.inspect_vanishing(self.driver.page_source)
            if self.save_cookies_bool:
                self.save_cookies()
            self.error_timer = time.time()
            self.first = False
        def to_except():
            try:
                self.progress = False
                time_string = f'{time.time() - self.error_timer} sec'
                print(colorize(time_string, Fore.YELLOW))
                if (time.time() - self.error_timer) >= self.max_waste_time:
                    mes = f'--МЕНЯЮ ЛИЧНОСТЬ, max_waste_time превышен ({self.max_waste_time} сек)--'
                    lprint(mes, self.short_name, color=Fore.RED)
                    self.error_timer = time.time()
                    self.slide_tab()
                self.except_on_main()
            except Exception as error:
                printing_error = str(error).split('\n')[0] if '\n' in str(error) else str(error)
                lprint('Except on exception: ' + str(error), self.short_name, only_log=True, color=Fore.RED)
                lprint('Except on exception: ' + printing_error, self.short_name, color=Fore.RED)
                lprint(traceback.format_exc(), self.short_name, only_log=True, color=Fore.RED)
            time.sleep(1)
        while True:
            self.num += 1
            if multi:
                if self.num and (self.num % self.counter_step == 0): 
                    self.bprint('Проход номер ' + str(self.num))
            else:
                print('Проход номер ' + str(self.num))
            if self.terminator:
                return False
            if not multi_try(to_try, to_except, 'Main', self.max_tries, self.release, ChrTab=self.short_name):
                self.on_errors()
            delay = get_delay(self.delay)
            time.sleep(delay)
            
    def queue_mode(self):
        self.show_consts()
        def to_try():
            self.progress = True
            if self.driver_source == 'selenium':
                self.driver = self.proxyfied_chrome(user_agent=BotCore.user_agent)
                self.driver.set_page_load_timeout(BotCore.timeout)
                self.set_window()
            elif self.driver_source == 'hrenium':
                self.driver = self.hrenium()
            self.before_body()
            if self.driver_source:
                self.load(self.URL, False, retry=self.retry)
            success = False
            while not success:
                success = self.body()
            if self.driver_source:
                self.driver.quit()
        def to_except():
            self.progress = False
            if self.driver_source:
                self.driver.quit()
        multi_try(to_try, to_except, 'Main', self.max_tries, self.release, ChrTab=self.short_name)
        BotCore.working -= 1
    
    def set_short_name(self):
        if not self.bot_name:
            self.short_name = self.ChrTab
            return True
        name_items = self.bot_name.split(chr(183))
        stripped = [name.strip() for name in name_items]
        tab, event_name, city, domain, _ = stripped
        if len(event_name) >= 6:
            event_name = event_name[:6]
        if len(city) >= 6:
            city = city[:6]
        self.short_name = f'#{tab} {event_name} {city}'
    
    def run(self):
        self.terminator = False
        self.set_short_name()
        if self.release:
            CommandThread(self).start()
        if self.mode == 'bot':
            self.bot_mode()
        if self.mode in ('multi_bot', 'multi'):
            self.bot_mode(multi=True)
        elif self.mode == 'queue':
            self.queue_mode()
            
    def stop(self):
        self.terminator = True
        

def recaptcha_v3(sitekey, action, pageurl, min_score=0.3, mode=0, report=False):
    if mode == 1:
        return recaptcha_v3_alt(sitekey, action, pageurl, min_score)
        
    params = {
        'key': BotCore.api_key,
        'method': 'userrecaptcha',
        'version': 'v3',
        'min_score': str(min_score),
        'googlekey': sitekey,
        'pageurl': pageurl,
        'json': '1'
        }
    if action:
        params['action'] = action
    r = requests.get('https://rucaptcha.com/in.php', params=params)
    page = r.text
    try:
        response = json.loads(r.text)
    except:
        raise RuntimeError(r.text)
    status = response['status']
    if status:
        id = response['request']
        params = {
            'id': id,
            'action': 'get',
            'json': '1',
            'key': BotCore.api_key
            }
        time.sleep(3)
        for i in range(10):
            time.sleep(2 + i * 1.5)
            r = requests.get('https://rucaptcha.com/res.php', params=params)
            page = r.text
            try:
                response = json.loads(page)
            except:
                raise RuntimeError(page)
            status = response['status']
            request = response['request']
            if status:
                #lprint('rucaptcha.com: status=%s' % status)
                if report:
                    return request, id
                else:
                    return request
        else:
            raise RuntimeError('Wasn\'t solved')


def recaptcha_v3_report(id_, action_):
    action = 'reportgood' if action_ else 'reportbad'
    
    params = {
        'key': BotCore.api_key,
        'action': action,
        'id': id_,
    }
    
    r = requests.get('https://rucaptcha.com/res.php', params=params)
    
    return r.text
            
            
def recaptcha_v3_alt(sitekey, action, pageurl, min_score=0.3):
    task = {
        'type': 'RecaptchaV3TaskProxyless',
        'websiteURL': pageurl,
        'websiteKey': sitekey,
        'pageAction': action,
        'minScore': min_score
    }
    params = {
        'clientKey': BotCore.client_key,
        'task' : task
    }
    r = requests.post('https://api.anti-captcha.com/createTask', json=params)
    
    response = r.json()
    error_id = response['errorId']
    if error_id:
        raise RuntimeError(f'anti-captcha.com: in.php error (code {error_id})')
    params = {
       'taskId': response['taskId'],
       'clientKey': BotCore.client_key
    }
    time.sleep(10)
    for i in range(10):
        time.sleep((i + 2) * 1.5)
        r = requests.post('https://api.anti-captcha.com/getTaskResult', json=params)
        response = r.json()
        error_id = response['errorId']
        if error_id:
            raise RuntimeError(f'ReCaptcha v3 error: {error_id}')
        else:
            status = response['status']
            if status == 'ready':
                return response['solution']['gRecaptchaResponse']
    raise RuntimeError(f'ReCaptcha v3 wasn\'t solved')


class CommandThread(threading.Thread):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        
    def print_state(self):
        mes = self.bot.event_name + ':\n'
        state = self.bot.tickets_state[self.bot.event_name]
        if isinstance(state, bool):
            mes += str(state)
        elif isinstance(state, list):
            items = [f"  -{item}" for item in state]
            mes += '\n'.join(items)
        elif isinstance(state, dict):
            items = [f"  --{item}|{state[item]}" for item in state]
            mes += '\n'.join(items)
        mes += f'\n{self.bot.last_update}'
        self.bot.lprint(mes)
        
    def print_page(self):
        self.bot.inspect_vanishing_lock = True
        self.bot.bprint('Waiting for vanishing set to True')
        
    def command(self, command):
        try:
            if command == 't':
                self.print_state()
            elif command == 'page':
                self.print_page()
            elif command == 'vipe':
                self.print_page()
        except:
            self.bot.lprint(red(f'Error processing command "{command}"'))
        
    def run(self):
        script_name = sys.argv[0]
        if ':\\' in script_name:
            script_name = script_name.split('\\')[-1]
        if not script_name.startswith('m_') and \
                not script_name.startswith('ev_') and \
                not script_name.startswith('news_'):
            return True
        while True:
            command = input()
            self.command(command)
            time.sleep(0.1)
            
            
def get_path(url):
    urlparts = url.split('/')
    path = '/' + '/'.join(urlparts[3:])
    if not path.endswith('/'):
        path += '/'
    return path
            
            
def get_chrtab(increase=True):
    chrtab_path = source_path + 'ChrTab.txt'
    while True:
        try:
            with open(chrtab_path, 'r') as f:
                payload = f.read()
            if payload == '':
                payload = '0'
            chrtab = int(payload)
            if increase:
                chrtab += 1
                with open(chrtab_path, 'w') as f:
                    f.write(str(chrtab))
            return chrtab
        except:
            print('Error writing to ChrTab.txt')
            time.sleep(1)


def get_tele_ids(profile):
    profile = profile.replace(' ', '')
    profile_spl = profile.split(';')
    
    not_found = [name for name in profile_spl if name not in TELE_PROFILES]
    if not_found:
        raise RuntimeError(f'Имена не найдены в TELE_PROFILES: {not_found}')
    
    id_lists = [TELE_PROFILES[profile] for profile in profile_spl]
    to_tele_ids = [elem for elems in id_lists for elem in elems]
    return [454746771, 647298152] + list(set(to_tele_ids))
    
    
def get_parent(elem):
    return elem.find_element_by_xpath('..')
        

def get_delay(delay, l_range=0.723, r_range=1.26):
    hour_activity = (8, 4, 2, 1.5, 0.8, 0.8, 1.0, 2, 4, 8, 10, 13, 15, 15, 15, 17, 19, 19, 18, 13, 11, 9, 8, 8)
    mean = statistics.mean(hour_activity)
    hour_activity = [hour / mean for hour in hour_activity]
    hour = time.strftime('%H')
    hour = int(hour)
    delay /= hour_activity[hour]
    
    spread_x = random.random() * (r_range - l_range) + l_range
    spread_y = spread_x ** 4
    delay *= spread_y
    return delay
    

def start_bots(needed_events, BotInit, auto_chrtab=False, inc=0, first=True, args=[], is_buying_bot=False):
    tabs = []
    def domain_from_link(link):
        if isinstance(link, dict):
            link = list(link.values())[0]
        if 'www.' in link:
            domain = double_split(link, 'www.', '/')
        else:
            domain = double_split(link, '://', '/')
        domain_levels = domain.split('.')
        domain = '.'.join(domain_levels[-2:])
        if len(domain_levels) > 2:
            domain = '*.' + domain
        return domain
    
    if first and not is_buying_bot:
        manager_client = bot_socket.run_socket(tabs)

    if BotCore.proxy_centralized:
        proxies_json_path = source_path + '\\proxies.json'
    else:
        proxies_json_path = 'json\\proxies.json'
    with open(proxies_json_path, 'r') as proxiesjson:
        proxies = json.load(proxiesjson)
    plen = len(proxies)


    event_count = len(needed_events)
    num_text_len = 0
    event_text_len = 0
    city_text_len = 0
    domain_text_len = 0
    domain_counter = {}
    for i in range(event_count):
        if auto_chrtab:
            name, link = needed_events[i][0:3:2]
            domain = domain_from_link(link)
            if domain not in domain_counter:
                domain_counter[domain] = 1
            else:
                domain_counter[domain] += 1
        else:
            name, link = needed_events[i][0:3:2]
            domain = domain_from_link(link)
        event, city, date = name.split('. ')
        num = str(i + 1)
        num_text_len = max(num_text_len, len(num))
        event_text_len = max(event_text_len, len(event))
        city_text_len = max(city_text_len, len(city))
        domain_text_len = max(domain_text_len, len(domain))
    counter_passed = dict.fromkeys(domain_counter.keys(), 0)
    for i in range(event_count):
        name, profile, link = needed_events[i][:3]
        kwargs = needed_events[i][3] if len(needed_events[i]) == 4 else {}
        tab_num = get_chrtab(BotInit.release)
        
        #getting bot_name
        bot_number = str(i + 1)
        domain = domain_from_link(link)
        event, city, date = name.split('. ')
        c_bot_number = bot_number + chr(183)
        c_event = event + chr(183)
        c_city = city + chr(183)
        c_domain = domain + chr(183)
        l_num = c_bot_number.ljust(num_text_len + 1)
        l_event = c_event.ljust(event_text_len + 1)
        l_city = c_city.ljust(city_text_len + 1)
        l_domain = c_domain.ljust(domain_text_len + 1)
        bot_name = f'{l_num}{l_event}{l_city}{l_domain}'
        
        if auto_chrtab:
            tab = BotInit(1 + inc, name, link, bot_name, *args, **kwargs)
        else:
            tab = BotInit(tab_num + inc, name, link, bot_name, *args, **kwargs)
        #getting proxies_on_bot to tab.proxies
        if auto_chrtab:
            bots_on_domain = domain_counter[domain]
            bot_on_domain = counter_passed[domain]
            plen_on_domain = int(plen / bots_on_domain)
            start = bot_on_domain * plen_on_domain
            end = (bot_on_domain + 1) * plen_on_domain
            proxies_on_bot = proxies[start: end]
            counter_passed[domain] += 1
        
        #getting tele_ids_on_bot to tab.tele_ids
        tele_ids_on_bot = get_tele_ids(profile)
        
        if auto_chrtab:
            tab.proxies = proxies_on_bot
        tab.tele_ids = tele_ids_on_bot
        tab.tele_profile = profile
        tab.bprint(profile)
        tab.start()
        
        tabs.append(tab)
        if BotInit.driver_source == 'selenium':
            time.sleep(1.9)
        if first:
            time.sleep(0.1)
    return tabs


def screen_r(text, addition=''):
    path='screen\\'
    filename = path + str(time.asctime()) + addition + '.html'
    filename = filename.replace(':', '') \
                       .replace(' ', '_')
    with open(filename, 'w+', encoding='utf-8') as f:
        f.write(text)


source_path = main_utils.get_source_path()
default_fore = Fore.RESET
default_back = Back.RESET
