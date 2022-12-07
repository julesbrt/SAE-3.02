import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 10000
message = ''
# déconnexion de l’interface permettant de libérer la machine monitorée pour permettre de libérer le serveur pour d’autres requêtes
DISCONNECT = 'disconnect'
KILL = 'kill'  # tue le serveur
RESET = 'reset'  # reset du serveur
msgserv = ''

class Client:
    def __init__(self, host, port):
        self.clsocket = socket.socket()
        self.port = port
        self.host = host
        self.message = ''
        self.iskilled = False

    def connexion(self):
        self.clsocket.connect((self.host, self.port))
        
        thread = threading.Thread(target=self.reception)
        thread.start()
        # print('Fermeture du client')
        # self.clsocket.close()

    def envoi(self, message):
        self.clsocket.send(message.encode())

    def reception(self):
        msgserv = ""
        while message != DISCONNECT and msgserv != DISCONNECT and message != KILL and msgserv != KILL and self.iskilled == False:
            msgserv = self.clsocket.recv(1024).decode()
            print(msgserv)
        
    def kill(self):
        self.iskilled = True
        self.clsocket.send(KILL.encode())
        self.clsocket.close()
        print('Fermeture du client')

    def reset(self):
        self.clsocket.send(RESET.encode())
        self.clsocket.close()
        print('Redémarrage du serveur')

    def disconnect(self):
        self.iskilled = True
        self.clsocket.send(DISCONNECT.encode())
        self.clsocket.close()
        print('Fermeture du client')


if __name__ == '__main__':
    client = Client(HOST, PORT)
    try:
        client.connexion()
        #client2 = Client(HOST, int(sys.argv[1]))
        message = ''
        while message != DISCONNECT and message != KILL: 
            message = input('Entrer une commande: ')
            client.envoi(message)
            #client2.envoi(message)
    except KeyboardInterrupt:
        client.kill()