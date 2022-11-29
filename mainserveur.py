import socket
import platform
import commandes

host = '127.0.0.1'
port = 10000

socketserv = socket.socket()
socketserv.bind((host, port))
socketserv.listen(1)


disconnect = 'disconnect'
kill = 'kill'


#platform.node renvoi le nom du serveur.
#platform.system() renvoi le système d'exploitation serveur.

class Serveur:
    def __init__(self) -> None:
        data = reply = ''
        while data != kill and reply != kill:
            conn, address = socketserv.accept()
            data = reply = ''
            print('Connexion établie avec: ', str(address))
            while data != disconnect and reply != disconnect and data != kill and reply != kill:
                data = conn.recv(1024).decode()
                print(data)
                commandes.reponse(data, reply)
                conn.send(reply.encode())
            conn.close()
            print('Connexion fermée avec: ', str(address))
        socketserv.close()
        print('Fermeture du serveur')



if __name__ == '__main__':
    Serveur()


