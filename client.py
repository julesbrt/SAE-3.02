import socket

host = '127.0.0.1'
port = 10000
message = ''
client_socket = socket.socket()
bye = 'bye'
arret = 'arret'
data = ''

if __name__ == '__main__':
    client_socket.connect((host, port))
    while message != bye and data != bye and message != arret and data != arret:
        message = input(str('Entrez votre message: '))
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        print(data)
    
    print('Fermeture du client')
    client_socket.close()

class Client:
    def __init__(self):
        self.clsocket = socket.socket()
        self.port = 10000
        self.message = ''

    def connect(self):
        self.clsocket.connect((self))
        

