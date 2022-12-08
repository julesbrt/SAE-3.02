import sys
import psutil
from client import *
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QProgressBar, QTextBrowser,
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QCloseEvent

cpu = int(psutil.cpu_percent())
client = Client(HOST, PORT)

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.txtcmd = ""
        self.cmd = ["OS", "IP", "Name", "CPU", "RAM", "Disconnect", "Connexion information", "kill", "reset"]
        widget = QWidget()
        self.resize(500, 400) # taille de la fenêtre
        self.setWindowTitle('SAE 3.02')
        self.setCentralWidget(widget)
        self.grid = QGridLayout()
        widget.setLayout(self.grid)
        
        self.__entrcmd = QLabel("Entrer votre commande :")
        self.__cmd = QLineEdit()
        self.__btnenv = QPushButton("Envoyer")
        self.__affichage = QTextBrowser()
        self.__info = QPushButton("Infos sur les commandes")
        self.__btnco = QPushButton("Connexion")
        self.__affichetat = QLabel("Etat de la connexion :")
        self.__etat = QLabel("Déconnecté")

        self.__cpubar = QProgressBar()


        self.grid.addWidget(self.__affichage, 1, 1, 1, 1)
        self.grid.addWidget(self.__affichetat, 0, 0, 1, 1)
        self.grid.addWidget(self.__etat, 0, 2, 1, 1)
        self.grid.addWidget(self.__btnco, 1, 0, 1, 1)
        self.grid.addWidget(self.__info, 1, 2, 1, 1)
        self.grid.addWidget(self.__entrcmd, 2, 0, 1, 1)
        self.grid.addWidget(self.__cmd, 2, 1, 1, 1)
        self.grid.addWidget(self.__btnenv, 2, 2, 1, 1)

        self.__cpubar.setValue(cpu)
        self.grid.addWidget(self.__cpubar, 3, 1, 1, 1) #affichage ne fonctionne pas ??
        
        
        self.__info.clicked.connect(self._actionInfo)
        self.__btnco.clicked.connect(self._actionCo)
        self.__btnenv.clicked.connect(self._actionEnv)



    def _actionInfo(self):
        msg = QMessageBox()
        message = "Voici la liste des commandes disponilbes : \n\n      Commandes simples :\nOS : affiche l'OS \nIP : affiche l'IP \nName : affiche le nom \nCPU : affiche le % d'uitilisation du CPU \nRAM : affiche la mémoire totale, mémoire utilisée et mémoire libre restante \n\n        Commandes avancées : \nDisconnect : déconnexion de l'interface \nConnexion information : affiche les informations de connexion \nKill : arrête le serveur \nReset : redémarre le serveur \n\n       Commandes libres : \nToutes les commandes libres sont disponibles "
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.exec()

    def _actionCo(self):
        try:
            client.connexion()
            self.__affichage.append("Connexion réussie")
            self.__etat.setText("Connecté")
        except:
            self.__affichage.append("Connexion échouée")

    def _actionEnv(self):
        try:
            if self.__cmd.text() == "kill":
                client.kill()
                self.__etat.setText("Déconnecté")
            elif self.__cmd.text() == "reset":
                client.reset()
                self.__etat.setText("Déconnecté")
            elif self.__cmd.text() == "disconnect":
                client.disconnect()
                self.__etat.setText("Déconnecté")
            else:
                self.txtcmd = self.__cmd.text()
                self.__affichage.append("Commande envoyée : " + self.txtcmd)
                client.envoi(self.txtcmd)
          
                
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Le serveur n'est pas connecté")
            msg.exec()

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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())