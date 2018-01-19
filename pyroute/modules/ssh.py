from paramiko import SSHClient, AutoAddPolicy
from pyroute.module import Module


class SSHModule(Module):

    def __init__(self, config):
        self.config_data = super().\
            __init__(config=config, defaults=self.defaults)
        self.module_config = self.config_data['defaults']        
        self.connection = SSHClient()
        self.connection.set_missing_host_key_policy(AutoAddPolicy())
        self.__connect()
        self.stdout, self.stdin = [], []

    def __connect(self):
        self.connection.connect(username=self.module_config['user'], 
                                password=self.module_config['password'],
                                hostname=self.module_config['host'])

    def __close(self):
        self.connection.close()

    def execute_command(self, command):
        stdin, stdout, _ = self.connection.exec_command(command)
        self.stdout = stdout.readlines()
        self.stdin = stdin
        self.__close()
        print(self.stdout)
        return ''.join(self.stdout).split('\n')[:-1]
        
    def get_file(self, r_file_dir, l_file_dir):
        self.sftp_connection = self.connection.open_sftp()
        self.sftp_connection.get(r_file_dir, l_file_dir)

    def put_file(self, l_file_dir, r_file_dir):
        self.sftp_connection = self.connection.open_sftp()
        self.sftp_connection.put(l_file_dir, r_file_dir)
