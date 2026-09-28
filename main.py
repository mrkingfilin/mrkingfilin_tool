import os
import sys
from ping3 import ping
import colorama
import nmap3
import nslookup

menu=f'''{colorama.Fore.GREEN}
╔═══════════════════════════════════════════════════════╗
║ ██  ██  ▄▄▄▄ ▄▄  ▄▄ ▄▄ ▄█████ ▄▄   ▄▄ ▄██ ▄▄    ▄▄▄▄▄ ║
║ ██  ██ ██ ▄▄ ██  ▀███▀ ▀▀▀▄▄▄ ██▀▄▀██  ██ ██    ██▄▄  ║
║ ▀████▀ ▀███▀ ██▄▄▄ █   █████▀ ██   ██  ██ ██▄▄▄ ██▄▄▄ ║
╚═══════════════════════════════════════════════════════╝
╔════════════════════════menu═══════════════════════════╗
║ [1] Local Network Scan                                ║
║ [2] IP Port Scan                                      ║
║ [3] Domain lookup                                     ║
║ [4] Ping IP                                           ║
║ [0] Exit                                              ║
╚═══════════════════════════════════════════════════════╝'''

colorama.init(autoreset=True)

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def localnetworkscan():
    clear()
    ip = False
    iplist = []
    for i in ['192.168.0.1', '192.168.1.1', '192.168.10.1', '192.168.100.1']:
        if ping(i, timeout=0.5):
            ip = i.strip('.')[:-1]
            break
    else:
        input('No Wi-Fi connection or VPN is enabled...')
    if ip:
        for i in range(2, 100):
            filled = i // 10
            empty = 10 - filled
            print(f"\r{filled * '▰'}{empty * '▱'} {i}%", end="", flush=True)
            if ping(ip+str(i), timeout=0.3):
                iplist.append(ip+str(i))
        print(f"\r{colorama.Fore.GREEN}▰▰▰▰▰▰▰▰▰▰ 100%", end="", flush=True)
        print(f'''{colorama.Fore.BLUE}
   ╔══════════════╗
   ║ {ip+str(1):13}║
   ╚══════╦═══════╝
          ║''')
        for i in iplist:
            if i == iplist[-1]:
                print(f'''{colorama.Fore.BLUE}   ╔══════╩═══════╗
   ║ {i:13}║
   ╚══════════════╝''')
            else:
                print(f'''{colorama.Fore.BLUE}   ╔══════╩═══════╗
   ║ {i:13}║
   ╚══════╦═══════╝''')

        if ip:
            with open('localnetworkscan.txt', 'w+', encoding='utf-8') as file:
                for i in iplist:
                    file.write(f'{i}\n')
                print(colorama.Fore.GREEN + 'result save in localnetworkscan.txt')

        input('Enter...')

def ipportscan():
    clear()
    try:
        user = input('target ip> ')
        nm = nmap3.Nmap()
        result = nm.scan_top_ports(user)
        print('╔═══════════════════════════════╗')
        print(f'║TARGET: {user:23}║')
        print('╠════╦══════════╦═══════════════╣')
        for i in result[user]['ports']:
            color = ''
            if i['state']=='open':
                color = colorama.Fore.GREEN
            elif i['state']=='filtered':
                color = colorama.Fore.YELLOW
            elif i['state']=='closed':
                color = colorama.Fore.RED
            print(f'║{i['portid']:4}║{color}{i['state']:10}{colorama.Fore.WHITE}║ {i['service']['name']:14}║')
        print('╚════╩══════════╩═══════════════╝')
        input('Enter...')
    except:
        pass

def domainlookup():
    clear()
    result = []
    userinput = input('domain > ')
    domain = nslookup.Nslookup().dns_lookup(userinput)
    for i in domain.answer:
        result.append(i)
        if len(domain.answer) == 1:
            print(f'''{colorama.Fore.BLUE}   ╔═════════════════╗
   ║ {i:16}║
   ╚═════════════════╝''')
        elif i == domain.answer[0]:
            print(f'''{colorama.Fore.BLUE}   ╔═════════════════╗
   ║ {i:16}║
   ╚════════╦════════╝''')
        elif i == domain.answer[-1]:
            print(f'''{colorama.Fore.BLUE}   ╔════════╩════════╗
   ║ {i:16}║
   ╚═════════════════╝''')
        else:
            print(f'''{colorama.Fore.BLUE}   ╔════════╩════════╗
   ║ {i:16}║
   ╚════════╦════════╝''')

    if len(result) >= 1:
        with open(f'{userinput}.txt', 'w+', encoding='utf-8') as file:
            for i in result:
                file.write(f'{i}\n')
            print(f'Result save in {userinput}.txt')
    input('Enter...')

def pingip():
    clear()
    multiple = False
    ip = input('target ip> ')
    if ip.find('.txt') >= 0:
        multiple = True

    if multiple:
        with open(ip, 'r+', encoding='utf-8') as file:
            for ip in file:
                result = ping(ip.strip('\n'))
                print(f'{ip.strip('\n')} >> {result}ms')
        input('Enter...')
    else:
        result = ping(ip)
        if result:
            print(f'{ip} >> {result}ms')
        else:
            print('No connection')
        input('Enter...')


commands = [localnetworkscan, ipportscan, domainlookup, pingip, sys.exit]
comnum = [1, 2, 3, 4, 0]
def main():
    clear()
    print(menu)
    userinput = int(input('> '))
    if userinput in comnum:
        commands[comnum.index(userinput)]()

while True:
    main()
