import socket
import commandes
import sys

HOST = '127.0.0.1'
PORT = int(input("Port: "))

# déconnexion de l’interface permettant de libérer la machine monitorée pour permettre de libérer le serveur pour d’autres requêtes
disconnect = 'disconnect'
kill = 'kill'  # tue le serveur
reset = 'reset'  # reset du serveur


# platform.node renvoi le nom du serveur.
# platform.system() renvoi le système d'exploitation serveur.


class Serveur:
    def __init__(self):

        msg = ""
        while msg != kill:
            socketserv = socket.socket()
            try:
                socketserv.bind((HOST, PORT))
            except OSError:
                print("Le port est déjà utilisé")
                sys.exit()
            socketserv.listen(1)

            while msg != kill and msg != reset:
                conn, address = socketserv.accept()
                print("Connection à " + str(address))

                while msg != kill and msg != reset and msg != disconnect:
                    try:
                        msg = conn.recv(1024).decode()
                        print("Message reçu: " + msg)
                    except ConnectionResetError:
                        print("Le client s'est déconnecté")
                        break
                    else:          
                        rep = commandes.reponse(msg)
                        conn.send(rep.encode())
                        print("Réponse envoyée: " + rep)
                conn.close()
                print('Connexion fermée avec: ', str(address))
            # faire le reset
        socketserv.close()
        print('Fermeture du serveur')

    def kill(self):
        self.iskilled = True
        self.socketserv.close()
        self.conn.close()
        print('Fermeture du client')


if __name__ == '__main__':
    try:
        Serveur()
    except KeyboardInterrupt:
        print('Fermeture du serveur')
