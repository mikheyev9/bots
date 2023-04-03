from netifaces import interfaces, ifaddresses, AF_INET

def get_local_ip():
    addresses = []
    for ifaceName in interfaces():
        addresses.extend([i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )])
    addresses = [address for address in addresses if (address != '127.0.0.1') and (address != 'No IP addr')]
    return addresses[0]