from ping3 import ping
import colorama
import os
import nmap
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
    print(colorama.Fore.RED + '''
██╗    ██╗ █████╗ ██╗████████╗      
██║    ██║██╔══██╗██║╚══██╔══╝      
██║ █╗ ██║███████║██║   ██║         
██║███╗██║██╔══██║██║   ██║         
╚███╔███╔╝██║  ██║██║   ██║██╗██╗██╗
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝╚═╝╚═╝╚═╝
''')
    for i in range(1, num + 1):
        if ping('192.168.0.' + str(i), timeout=1):
            iplist.append(f'192.168.0.{str(i)}')
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
    print('Target IP: ...')
    inp = input(colorama.Fore.RED + name)
    nm = nmap.PortScanner()
    nm.scan(inp, '22-443')

def nslookup_():
    clear()
    print('site domain:')
    inp = input()
    a = nslookup.Nslookup(dns_servers=["8.8.8.8"], verbose=False, tcp=False).dns_lookup(domain=inp)
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
[2] Port scan [NOT WORKING]
[3] Nslookup
[0] Exit
    ''')
    inp = str(input(colorama.Fore.RED + name))
    if inp == '1':
        local_ip_scan()
    elif inp == '2':
        menu()
    elif inp == '3':
        nslookup_()
    elif inp == '0':
        clear()
        exit
    else:
        menu()

menu()
