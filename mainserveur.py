import socket
import platform
import commandes

host = '127.0.0.1'
port = 10000

disconnect = 'disconnect' # déconnexion de l’interface permettant de libérer la machine monitorée pour permettre de libérer le serveur pour d’autres requêtes
kill = 'kill' #tue le serveur
reset = 'reset' #reset du serveur


#platform.node renvoi le nom du serveur.
#platform.system() renvoi le système d'exploitation serveur.

class Serveur:
    def __init__(self):

        msg =""
        while msg != kill:
            socketserv = socket.socket()
            socketserv.bind((host, port))
            socketserv.listen(1)

            while msg != kill and msg != reset:
                conn, address = socketserv.accept()
                print("Connection à " + str(address))

                while msg != kill and msg != reset and msg != disconnect:
                    msg = conn.recv(1024).decode()
                    print("Message reçu: " + msg)

                    rep = commandes.reponse(msg)
                    conn.send(rep.encode())
                    print("Réponse envoyée: " + rep)

                conn.close()
            print('Connexion fermée avec: ', str(address))
            #faire le reset
        socketserv.close()
        print('Fermeture du serveur')

        
            




if __name__ == '__main__':
    Serveur()


