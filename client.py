import socket
import threading
import sys
import time

HOST = '127.0.0.1'
PORT = 10000
message = ''
# déconnexion de l’interface permettant de libérer la machine monitorée pour permettre de libérer le serveur pour d’autres requêtes
DISCONNECT = 'disconnect'
KILL = 'kill'  # tue le serveur
RESET = 'reset'  # reset du serveur
msgserv = ''

class Client:
    def __init__(self, affichage):
        self.clsocket = socket.socket()
        self.message = ''
        self.iskilled = False
        self.__affichage = affichage

    def connexion(self, host, port):
        self.clsocket.connect((host, port))
        thread = threading.Thread(target=self.reception)
        thread.start()
        # print('Fermeture du client')
        # self.clsocket.close()

    def envoi(self, message):
        self.clsocket.send(message.encode())

    def reception(self):
        msgserv = ""
        while message != DISCONNECT and msgserv != DISCONNECT and message != KILL and msgserv != KILL and self.iskilled == False:
            try:
                msgserv = self.clsocket.recv(1024).decode()
                self.__affichage.append(msgserv)
                print(msgserv)
            except ConnectionAbortedError:
                print("Le serveur s'est déconnecté")
                break
        
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
            time.sleep(0.05)
            #client2.envoi(message)
    except KeyboardInterrupt:
        client.kill()