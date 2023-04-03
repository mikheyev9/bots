import json
import time

with open('config.json', 'r') as f:
    settings = json.load(f)


class BanRules:
    def __init__(self):
        self.ban_list = {}
        self.tickets_tries = {}
        self.tickets_ban_time = {}
        self.tries_to_ban = settings['tries_to_ban']
        self.ban_time = settings['ban_time']
        self.long_ban_time = settings['long_ban_time']

    def check_ban_list(self, ticket):
        if ticket in self.ban_list:
            if time.time() - self.ban_list[ticket] >= self.long_ban_time:
                del self.ban_list[ticket]
                return True
            return False
        return True

    def check_tickets_tries(self, ticket):
        if ticket not in self.tickets_tries:
            self.tickets_tries[ticket] = 1
            return True
        if self.tickets_tries[ticket] >= self.tries_to_ban:
            self.tickets_ban_time[ticket] = time.time()
            del self.tickets_tries[ticket]
            return False
        else:
            self.tickets_tries[ticket] += 1
            return True

    def check_ticket_ban_time(self, ticket):
        if ticket not in self.tickets_ban_time:
            return True
        if time.time() - self.tickets_ban_time[ticket] >= self.ban_time:
            del self.tickets_ban_time[ticket]
            return True
        return False

    def main_check(self, ticket, sector_name, event_name):
        key = f'{ticket["row"]}{ticket["seat"]}{sector_name}{event_name}'
        if self.check_ban_list(key) and self.check_ticket_ban_time(key) and self.check_tickets_tries(key):
            return True
        return False

    def add_to_ban_list(self, ticket_list, sector_name, event_name):
        for ticket in ticket_list:
            key = f'{ticket["row"]}{ticket["seat"]}{sector_name}{event_name}'
            self.ban_list[key] = time.time()
            
