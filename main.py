from ping3 import ping
import colorama
import os
import nmap3
import socket
import nslookup

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

name = f'fcosiety@{socket.gethostname()}> '

def local_ip_scan():
    clear()
    iplist = []
    num = 17
    ip = ''
    if ping('192.168.0.1'):
        ip = '192.168.0.'
    elif ping('192.168.1.1'):
        ip = '192.168.1.'
    elif ping('192.168.10.1'):
        ip = '192.168.10.'
    else:
        ip = '127.0.0.'
    
    print(colorama.Fore.RED + 'WAIT...')
    for i in range(1, num + 1):
        if ping(ip+str(i), timeout=1):
            iplist.append(ip+str(i))
    clear()
    for i in iplist:
        if i == iplist[0]:
            print(colorama.Fore.RED +   '╔════════════╗')
        else:
            print(colorama.Fore.RED +   '╔═════╩══════╗')
        print(colorama.Fore.RED +  f'║{i:12}║')
        if i != iplist[-1]:
            print(colorama.Fore.RED +   '╚═════╦══════╝')
            print(colorama.Fore.RED + '      ║      ')
        else:
            print(colorama.Fore.RED +   '╚════════════╝')

    print('Enter...')
    input(colorama.Fore.RED + name)
    menu()

def port_scan():
    clear()
    scan_result = []
    print(colorama.Fore.RED + 'Target IP: ...')
    inp = input(colorama.Fore.RED + name)
    print(colorama.Fore.RED + 'WAIT...')
    nm = nmap3.Nmap()
    scan = nm.scan_top_ports(inp)
    clear()
    print(colorama.Fore.RED + f'Target IP: {inp}')
    for i in scan[inp]['ports']:
        portid = colorama.Fore.WHITE + i['portid']
        if i['state'] == 'open':
            state = colorama.Fore.GREEN + i['state']
        elif i['state'] == 'filtered':
            state = colorama.Fore.YELLOW + i['state']
        elif i['state'] == 'closed':
            state = colorama.Fore.RED + i['state']
        service = colorama.Fore.WHITE + i['service']['name']
        print(f'{portid:12}║ {state:15}{colorama.Fore.WHITE + '║'} {service}')
        scan_result.append(f'{portid:12}║ {state:15}{colorama.Fore.WHITE + '║'} {service}')
    with open(f'ScanResult_{inp}.txt', 'w+', encoding='utf-8') as file:
        for i in scan[inp]['ports']:
            file.write(f'{i['portid']:12}║ {i['state']:12}{'║'} {i['service']['name']}\n')
    print(colorama.Fore.GREEN + f'IP save in ScanResult_{inp}.txt')
    input(colorama.Fore.RED + name)
    menu()

def nslookup_():
    clear()
    print('site domain:')
    inp = input(colorama.Fore.RED + name)
    a = nslookup.Nslookup(dns_servers=["8.8.8.8"], verbose=False, tcp=False).dns_lookup(domain=inp)
    if inp == '' or len(a.answer) < 1:
        nslookup_()
    else:
        with open(f'{inp}.txt', 'w+', encoding='utf-8') as file:
            for i in a.answer:
                file.write(f'{i}\n')
        for i in a.answer:
            if i == a.answer[0]:
                print(colorama.Fore.RED +   '╔═══════════════╗')
            else:
                print(colorama.Fore.RED +   '╔═══════╩═══════╗')
            print(colorama.Fore.RED +  f'║{i:15}║')
            if i != a.answer[-1]:
                print(colorama.Fore.RED +   '╚═══════╦═══════╝')
                print(colorama.Fore.RED + '        ║      ')
            else:
                print(colorama.Fore.RED +   '╚═══════════════╝')
        print(colorama.Fore.GREEN + f'IP save in {inp}.txt')
    input(colorama.Fore.RED + name)
    menu()

def menu():
    clear()
    print(colorama.Fore.RED + '''
███████╗    ███████╗ ██████╗  ██████╗██╗███████╗████████╗██╗   ██╗
██╔════╝    ██╔════╝██╔═══██╗██╔════╝██║██╔════╝╚══██╔══╝╚██╗ ██╔╝
█████╗      ███████╗██║   ██║██║     ██║█████╗     ██║    ╚████╔╝ 
██╔══╝      ╚════██║██║   ██║██║     ██║██╔══╝     ██║     ╚██╔╝  
██║         ███████║╚██████╔╝╚██████╗██║███████╗   ██║      ██║   
╚═╝         ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚══════╝   ╚═╝      ╚═╝   
''')
    print(colorama.Fore.WHITE + '''
[1] Local ip scan
[2] Port scan
[3] Nslookup
[0] Exit
    ''')
    inp = str(input(colorama.Fore.RED + name))
    if inp == '1':
        local_ip_scan()
    elif inp == '2':
        port_scan()
    elif inp == '3':
        nslookup_()
    elif inp == '0':
        clear()
        exit
    else:
        menu()
try:
    menu()
finally:
    print(colorama.Fore.WHITE)
    clear()
