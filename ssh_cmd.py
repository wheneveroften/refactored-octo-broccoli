import paramiko

def ssh_command( ip, port, user, passwd,cmd):
    client = paramiko.SSHClient()
    client.set_missing_hot_key_policy(paramiko.AutoADDPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    _, stdout, stderr= client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('---Wynik---')
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    import getpass
    #user = getpass.getuser()
    user = input('Nazwa użytkownika')
    password = getpass.getpass('Hasło')

    ip = input('Adres IP Servera:') or '192.168.1.203'
    port = input('Port:') or 2222
    cmd = input('Polecenie: ') or 'id'
    ssh_command(ip, port, user, password, cmd)