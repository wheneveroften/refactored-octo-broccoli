import ipaddress
import struct
import os
import sys
import socket
import threading
import time


#Docelowa Podsieć
SUBNET= '192.168.1.0/24'
#Magiczny łańcuch , dla którego będziemy sprawdzać odpowiedzi ICMP
MESSAGE = 'PYTHONRULES!'

class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = header[0] >>4
        self.ihl = header[0] & 0xF

        self.toc = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        #Adres IP czytelny dla człowieka
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        #Powiązanie kodów protokołowych z ich nazwami
        self.protocol_map = {1: "IMCP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protcol_map[self.protocol_num]
        except Exception as e:
            print('%s Brak nazwy protokołu o kodzie %s' %(e, self.protocol_num))
            self.protocol = str(self.protocol_num)
class ICMP:
    def __init__(self, buff):
        header = struct.unpack('<BBHHH', buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

#Funkcja rozsyłania datagramy UDP zawierające magiczny komunikat
def udp_sender():
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(bytes(MESSAGE, 'utf -8'),(str(ip),65212))

class Scanner:
    def __init__(self,host  ):
        self.host = host
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socker.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL, 1)
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)


def sniff(host):
        #Kod podany do poprzedniego przykładu powinen wyglądać znajomo
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP


        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host, 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        try:
            while True:
                #Odczytanie pakietu
                raw_buffer = sniffer.recvfrom(65535)[0]
                #Utworzenie nagłówka IP na podstawie pierwszych 20 bajtów
                ip_header = IP(raw_buffer[0:20])
                #Wyświetlanie rozproznanego protokołu i adresów
                print('Protokół:%s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
                ip_header = IP(raw_buffer[0:20])
                #Jeżeli jest to pakiet ICMP , przetwarzamy go
                if ip_header.protocol == "ICMP":
                    print('Protokół: %s %s -> %s' %(ip_header.protocol, ip_header.src_address, ip_header.dst_address))
                    print(f'Wersja: {ip_header.ver}')
                    print(f'Dł.nagłówka: {ip_header.ihl}, TTL:{ip_header.ttl}')
                    #Wyliczanie początku pakietu ICMP:
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    #Utworzenie struktury
                    icmp_header = ICMP(buf)
                    print('ICMP -> Typ: %s, kod: %s\n   '% (icmp_header.type, icmp_header.code))


        except KeyboardInterrupt:
            #Jeśli użytkownik jest system Windows, wyłączamy tryb nieograniczony
            if os.name == 'nt':
                sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
            sys.exit()

if __name__=='__main__':
        if len(sys.argv) == 2:
            host = sys.argv[1]
        else:
            host = '192.168.56.1'
            sniff(host)


