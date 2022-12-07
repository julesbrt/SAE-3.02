import sys
import psutil
import commandes
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QProgressBar
from PyQt5.QtCore import QCoreApplication

cpu = int(psutil.cpu_percent())

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.txtcmd = ""
        self.cmd = ["OS", "IP", "Name", "CPU", "RAM", "Disconnect", "Connexion information", "Kill", "Reset"]
        widget = QWidget()
        self.resize(500, 400) # taille de la fenêtre
        self.setWindowTitle('SAE 3.02')
        self.setCentralWidget(widget)
        self.grid = QGridLayout()
        widget.setLayout(self.grid)
        
        self.__entrcmd = QLabel("Entrer votre commande :")
        self.__cmd = QLineEdit()
        self.__btnenv = QPushButton("Envoyer")
        self.__affichage = QLabel("Le texte")
        self.__info = QPushButton("Infos sur les commandes")

        self.__cpubar = QProgressBar()


        self.grid.addWidget(self.__affichage, 0, 1, 1, 1)
        self.grid.addWidget(self.__info, 1, 2, 1, 1)
        self.grid.addWidget(self.__entrcmd, 2, 0, 1, 1)
        self.grid.addWidget(self.__cmd, 2, 1, 1, 1)
        self.grid.addWidget(self.__btnenv, 2, 2, 1, 1)

        

            
        self.__info.clicked.connect(self._actionInfo)
        self.__btnenv.clicked.connect(self._actionEnv)



    def _actionInfo(self):
        msg = QMessageBox()
        message = "Voici la liste des commandes disponilbes : \n\n      Commandes simples :\nOS : affiche l'OS \nIP : affiche l'IP \nName : affiche le nom \nCPU : affiche le % d'uitilisation du CPU \nRAM : affiche la mémoire totale, mémoire utilisée et mémoire libre restante \n\n        Commandes avancées : \nDisconnect : déconnexion de l'interface \nConnexion information : affiche les informations de connexion \nKill : arrête le serveur \nReset : redémarre le serveur \n\n       Commandes libres : \nToutes les commandes libres sont disponibles "
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.exec()

    def _actionEnv(self):
        try:
            if self.__cmd.text() in self.cmd:
                self.txtcmd = self.__cmd.text()
                self.__affichage.setText("Commande envoyée : " + self.txtcmd)

            elif self.txtcmd == "CPU":
                self.__cpubar.setValue(commandes.getcpu())
                self.grid.addWidget(self.__cpubar, 3, 1, 1, 1) #affichage ne fonctionne pas ??

            else:
                self.__affichage.setText("Commande inconnue : " + self.__cmd.text())
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Commande inconnue")
            msg.exec()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())