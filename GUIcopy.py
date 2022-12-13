import sys
import psutil
from client import *
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QProgressBar, QTextBrowser,
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QCloseEvent

client = Client(HOST, PORT)
cpu = int(psutil.cpu_percent())
letxt = open("host.txt", "r")
text = letxt.read()
text = text.split("\n")
letxt.close()

class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.resize(500, 400) # taille de la fenêtre
        self.setWindowTitle('SAE 3.02')
        self.setCentralWidget(widget)
        self.__grid = QGridLayout()
        widget.setLayout(self.__grid)


        self.__host = QLabel("Host :")
        self.__port = QLabel("Port :")
        self.__enthost = QLineEdit()
        self.__entport = QLineEdit()
        self.__btnco = QPushButton("Connexion")
        self.__btnco.clicked.connect(self._actionCo)
        self.__affichetat = QLabel("Etat de la connexion :")
        self.__etat = QLabel("Déconnecté")
        

 
        self.__grid.addWidget(self.__host, 0, 0, 1, 1)
        self.__grid.addWidget(self.__enthost, 0, 1, 1, 1)
        self.__grid.addWidget(self.__port, 1, 0, 1, 1)
        self.__grid.addWidget(self.__entport, 1, 1, 1, 1)
        self.__grid.addWidget(self.__btnco, 2, 0, 1, 1)
        self.__grid.addWidget(self.__affichetat, 3, 0, 1, 1)
        self.__grid.addWidget(self.__etat, 3, 1, 1, 1)
        
    
    def _actionCo(self):
        try:
            host = self.__enthost.text()
            port = int(self.__entport.text())
            client = Client(host, port)
            client.connexion()
            self.__etat.setText("Connecté")
            diag = NvServ(host,port)
            diag.show()
            diag.exec()
        except Exception as e:
            self.__etat.setText(f"Erreur de connexion ({e})")

  
    def closeEvent(self, _e: QCloseEvent): # <--- Fermeture de l'application depuis la croix Windows
        try:
            box = QMessageBox()
            box.setWindowTitle("Quitter ?")
            box.setText("Voulez vous quitter ?")
            box.addButton(QMessageBox.Yes)
            box.addButton(QMessageBox.No)
            ret = box.exec()
            if ret == QMessageBox.Yes:
                client.kill()
                QCoreApplication.exit(0)
            else:
                _e.ignore()
        except OSError:
            QCoreApplication.exit(0)

class NvServ(QDialog):

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.setWindowTitle("Nouvelle connexion")
        self.resize(1000, 500)
        self.grid = QGridLayout()
        self.txtcmd = ""
        self.cmd = ["OS", "IP", "Name", "CPU", "RAM", "Disconnect", "Connexion information", "kill", "reset"]

        self.__entrcmd = QLabel("Entrer votre commande :")
        self.__cmd = QLineEdit()
        self.__btnenv = QPushButton("Envoyer")
        self.__affichage = QTextBrowser()
        self.__info = QPushButton("Infos sur les commandes")
        self.__btndeco = QPushButton("Déconnexion")
        self.__btnfermsrv = QPushButton("Fermer le serveur")
        self.__affichetat = QLabel("Etat de la connexion :")
        self.__list = QComboBox()
        self.__list.addItems(text)
        self.__etat = QLabel("Déconnecté")
        self.__btnnvserv = QPushButton("Ajouter un serveur")

        self.__cpubar = QProgressBar()


        self.grid.addWidget(self.__btnnvserv, 0, 0, 1, 1)
        self.grid.addWidget(self.__list, 1, 0, 1, 1)
        self.grid.addWidget(self.__btndeco, 2, 1, 1, 1)
        self.grid.addWidget(self.__btnfermsrv, 2, 2, 1, 1)

        self.grid.addWidget(self.__affichage, 1, 1, 1, 1)
        
        self.grid.addWidget(self.__affichetat, 0, 1, 1, 1)
        self.grid.addWidget(self.__etat, 0, 2, 1, 1)
        
        
        self.grid.addWidget(self.__info, 1, 2, 1, 1)
        self.grid.addWidget(self.__entrcmd, 3, 0, 1, 1)
        self.grid.addWidget(self.__cmd, 3, 1, 1, 1)
        self.grid.addWidget(self.__btnenv, 3, 2, 1, 1)

        self.__cpubar.setValue(cpu)
        self.grid.addWidget(self.__cpubar, 4, 1, 1, 1)
        
        
        self.__info.clicked.connect(self._actionInfo)
        self.__btndeco.clicked.connect(self._actionDeco)
        self.__btnfermsrv.clicked.connect(self._actionFermSrv)
        self.__btnenv.clicked.connect(self._actionEnv)
        self.__btnnvserv.clicked.connect(self._actionNvserv)



    def _actionInfo(self):
        msg = QMessageBox()
        message = "Voici la liste des commandes disponilbes : \n\n      Commandes simples :\nOS : affiche l'OS \nIP : affiche l'IP \nName : affiche le nom \nCPU : affiche le % d'uitilisation du CPU \nRAM : affiche la mémoire totale, mémoire utilisée et mémoire libre restante \n\n        Commandes avancées : \nDisconnect : déconnexion de l'interface \nConnexion information : affiche les informations de connexion \nKill : arrête le serveur \nReset : redémarre le serveur \n\n       Commandes libres : \nToutes les commandes libres sont disponibles "
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.exec()
        
    def _actionDeco(self):
        try:
            client.disconnect()
            self.__affichage.append("Déconnexion réussie")
            self.__etat.setText("Déconnecté")
            NvServ.close()
        except:
            self.__affichage.append("Déconnexion échouée")

    def _actionFermSrv(self):
        try:
            client.kill()
            self.__affichage.append("Serveur fermé")
            self.__etat.setText("Déconnecté")
            NvServ.close()
        except:
            self.__affichage.append("Serveur déjà fermé")

    def _actionEnv(self):
        try:
            if self.__cmd.text() == "kill":
                client.kill()
                self.__etat.setText("Déconnecté")
                NvServ.close()
            elif self.__cmd.text() == "reset":
                client.reset()
                self.__etat.setText("Reset")
            elif self.__cmd.text() == "disconnect":
                client.disconnect()
                self.__etat.setText("Déconnecté")
                NvServ.close()
            else:
                self.txtcmd = self.__cmd.text()
                self.__affichage.append("Commande envoyée : " + self.txtcmd)
                client.envoi(self.txtcmd)
                self.__affichage.append("Réponse du serveur : " + client.reception())
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Le serveur n'est pas connecté")
            msg.exec()





        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
