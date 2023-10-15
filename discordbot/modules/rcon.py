from rcon.source import Client

class Rcon():
    def __init__(self, ip, port, pas):
        self.ip = ip
        self.port = port
        self.pas = pas

    def __get_client(self):
        return Client(self.ip, self.port, passwd=self.pas)

    def whitelist_add(self, name):
        with self.__get_client() as client:
            response = client.run(f'whitelist add {name}')
            print(response)