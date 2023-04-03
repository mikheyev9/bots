import multiprocessing


cpu_count = multiprocessing.cpu_count()
default_settings = {
    'tele_bool': True,
    'order_threads': cpu_count,
    'sector_threads': cpu_count,
    'session_threads': 5,
    'session_duration': 3600,
    'counter_step': 50,
    'reimport_delay': 5,
    'limit': 8,
    'cart_threads': 0, #if 0, processes concurrently
    'tries_to_ban': 2,
    'ban_time': 30,
    'long_ban_time': 600,
    'order_multiplier': 1,
    'del_alones': True
}

def check_config(settings):
    for key in default_settings:
        if key not in settings:
            settings[key] = default_settings[key]