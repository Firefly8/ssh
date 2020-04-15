import re
import paramiko
from time import sleep


class SSH(object):
    def __init__(self, ip, username, passwd):
        self.ip = ip
        self.username = username
        self.passwd = passwd
        self.t = ''
        self.channel = ''
        self.try_times = 3

    def connect(self):
        while self.try_times > 0:
            try:
                self.t = paramiko.Transport(sock=(self.ip,22))
                self.t.connect(username = self.username, password = self.passwd)
                self.channel = self.t.open_session()
                self.channel.get_pty()
                self.channel.invoke_shell()
            except Exception as e:
                if self.try_times != 0:
                    self.try_times -= 1
                else:
                    print('timeout')
                    exit(1)
            self.try_times = 0


    def recv(self):
        print(self.channel.recv(65535).decode('utf-8'))

    def send(self,cmd):
        self.channel.send(cmd)

    def close(self):
        self.channel.close()
        self.t.close()


if __name__ == '__main__':
    host = SSH('192.168.1.7', 'ml', 'yyga@12315')
    host.connect()
    print('connect successful!')
    host.send('ls -l\n')
    while True:
        sleep(1)
        host.recv()

