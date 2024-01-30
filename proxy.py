import sys
import threading
import socket

HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.'for i in range(256)])

def hexdump(src, lenght=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()
    results = list()
    for i in range(0, len(src),lenght):
        word = src(src[i:i+lenght])
        printable = word.translate(HEX_FILTER)
        hexa =' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = lenght*3
        results.apppend(f'{i:04x}   {hexa:<{hexwidth}}  {printable}    ')
    if show:
        for line in results:
            print(line)
    else:
        return results
def receive_from(connection):
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e :
        print('Błąd ', e )
        pass
    return buffer

def request_handler(buffer):
    #modyfikacja pakietu
    return buffer

def response_handler(buffer):
    #modyfikacje pakietu
    return buffer

def proxy_handel(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==Wysłanie %d bajtów do lokalnego hosta." % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[<==] Obebrano %d bajtów id lokalnego hosta" % len(local_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[<==] Wysłano do zdalnego hosta")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Odebrano %d bajtów od zdalnego hosta" % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Wyslano do lockalnego hosta")
        if not len(remote_buffer) or len(local_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*]Nie ma wiecej danych. Zamykanie połączenia.")
            break

def server_loop(local_host, local_port, remote_port, remote_host, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print('Problem z utearzeniem gniazda: %r' %e)

        print("[!!] Brak możliwości nasłuchania na %s:%d" % (local_host,local_port))
        print("[!!] Sprawdź inne gniazda nasłuchu lub zmień uprawnienia.")
        sys.exit()
    print("[*] Nasłuchiwanie na %s%d" % (local_host,local_port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        # Wyświetlanie informacji o lokalnym połączeniu
        line = "> Odebrano połaczenie przychodzące od %s%d" %(addr[0],addr[1])
        print(line)
        # Uruchonienie wątku od komunikacji ze zdalnym hostem
        proxy_thread = threading.Thread(target= proxy_handel, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def main():
     if len(sys.argv[1:]) !=5:
         print("Używacie: ./proxy.py [local host] [local port]", end='')
         print("[zdalny host] [zdalny port] [najpierw_odbiranie]")
         print("Przykład : python proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
         sys.exit(0)

     local_host = sys.argv[1]
     local_port = int(sys.argv[2])

     remote_host = sys.argv[3]
     remote_port = int (sys.argv[4])

     receive_first = sys.argv[5]

     if "True" in receive_first:
         receive_first = True
     else:
         receive_first = False

     server_loop(local_host,local_port,remote_port,remote_host, receive_first)

if __name__ == '__main__':
    main()
