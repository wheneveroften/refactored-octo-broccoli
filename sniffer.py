import os
import socket

#Host do nasłuchiwania
HOST = '192.168.56.1'

def main():
    #Utworzenie surowego gniazda i powwizanie go z interfajsem publicznym
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))
    #Przechwytujemy też nogłówek IP
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    #Wczytywanie pojedyniczego pakietu
    print(sniffer.recvfrom(65565))

    #Jeśli użytkowany jest windows, wyłączamy tryb nieograniczony

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__=='__main__':
    main()