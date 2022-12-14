import sys
import psutil
from client import *
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QProgressBar, QTextBrowser,
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt


cpu = int(psutil.cpu_percent())
ram = int(psutil.virtual_memory().percent)
disk = int(psutil.disk_usage('/').percent)

letxt = open("host.txt", "r")
text = letxt.read()
text = text.split("\n")
letxt.close()

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.txtcmd = ""
        self.cmd = ["OS", "IP", "Name", "CPU", "RAM", "Disconnect", "Connexion information", "kill", "reset"]
        widget = QWidget()
        self.resize(1200, 800) # taille de la fenêtre
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
        self.__btndeco = QPushButton("Déconnexion")
        self.__btnfermsrv = QPushButton("Fermer le serveur")
        self.__affichetat = QLabel("Etat de la connexion :")
        self.__list = QComboBox()
        self.__list.addItems(text)
        self.__etat = QLabel("Déconnecté")
        self.__etat.setStyleSheet("background-color: red")
        self.__btnnvserv = QPushButton("Ajouter un serveur")
        self.__btninfos = QPushButton("Infos sur le serveur")

        

        self.client = Client(self.__affichage)


        self.grid.addWidget(self.__btnnvserv, 0, 0, 1, 1)
        self.grid.addWidget(self.__list, 1, 0, 1, 1)
        self.grid.addWidget(self.__btnco, 2, 0, 1, 1)
        self.grid.addWidget(self.__btndeco, 2, 1, 1, 1)
        self.grid.addWidget(self.__btnfermsrv, 2, 2, 1, 1)

        self.grid.addWidget(self.__affichage, 1, 1, 1, 1)
        
        self.grid.addWidget(self.__affichetat, 0, 2, 1, 1)
        self.grid.addWidget(self.__etat, 0, 3, 1, 1)
        
        
        self.grid.addWidget(self.__info, 1, 2, 1, 1)
        self.grid.addWidget(self.__entrcmd, 3, 0, 1, 1)
        self.grid.addWidget(self.__cmd, 3, 1, 1, 1)
        self.grid.addWidget(self.__btnenv, 3, 2, 1, 1)
        self.grid.addWidget(self.__btninfos, 2, 3, 1, 1)

        
        
        
        self.__info.clicked.connect(self._actionInfo)
        self.__btnco.clicked.connect(self._actionCo)
        self.__btndeco.clicked.connect(self._actionDeco)
        self.__btnfermsrv.clicked.connect(self._actionFermSrv)
        self.__btnenv.clicked.connect(self._actionEnv)
        self.__cmd.returnPressed.connect(self._actionEnv)
        self.__btnnvserv.clicked.connect(self._actionNvserv)
        self.__btninfos.clicked.connect(self._actionInfos)




    def _actionInfo(self):
        msg = QMessageBox()
        message = "Voici la liste des commandes disponilbes : \n\n      Commandes simples :\nOS : affiche l'OS \nIP : affiche l'IP \nName : affiche le nom \nCPU : affiche le % d'uitilisation du CPU \nRAM : affiche la mémoire totale, mémoire utilisée et mémoire libre restante \ngetall : affiche toutes les informations \n\n        Commandes avancées : \nDisconnect : déconnexion de l'interface \nConnexion information : affiche les informations de connexion \nKill : arrête le serveur \nReset : redémarre le serveur \n\n       Commandes libres : \nToutes les commandes libres sont disponibles "
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.exec()

    def _actionCo(self):
        try:
            host = self.__list.currentText().split(",")[0]
            port = int(self.__list.currentText().split(",")[1])
            self.client.connexion(host, port)
            self.__affichage.append("Connexion réussie")
            self.__etat.setText("Connecté")
            self.__etat.setStyleSheet("background-color: green")
        except Exception as e:
            self.__affichage.append(f"Connexion échouée ({e})")
        
    def _actionDeco(self):
        try:
            self.client.disconnect()
            self.__affichage.append("Déconnexion réussie")
            self.__etat.setText("Déconnecté")
            self.__etat.setStyleSheet("background-color: red")
        except OSError:
            self.__affichage.append("Déconnexion échouée")

    def _actionFermSrv(self):
        try:
            self.client.kill()
            self.__affichage.append("Serveur fermé")
            self.__etat.setText("Déconnecté")
            self.__etat.setStyleSheet("background-color: red")
        except:
            self.__affichage.append("Serveur déjà fermé")

    def _actionEnv(self):
        try:
            if self.__cmd.text() == "kill":
                self.client.kill()
                self.__etat.setText("Déconnecté")
                self.__etat.setStyleSheet("background-color: red")
            elif self.__cmd.text() == "reset":
                self.client.reset()
                self.__etat.setText("Déconnecté")
                self.__etat.setStyleSheet("background-color: red")
            elif self.__cmd.text() == "disconnect":
                self.client.disconnect()
                self.__etat.setText("Déconnecté")
                self.__etat.setStyleSheet("background-color: red")
            else:
                self.txtcmd = self.__cmd.text()
                self.__affichage.append("Commande envoyée : " + self.txtcmd)
                self.client.envoi(self.txtcmd)
                self.__cmd.clear()

        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"Le serveur n'est pas connecté ({e})")
            msg.exec()

    def _actionNvserv(self):
        diag = NvServ(HOST,PORT)
        diag.show()
        diag.exec()
    
    def _actionInfos(self):
        diag = Infos()
        diag.show()
        diag.exec()

    def closeEvent(self, _e: QCloseEvent): # <--- Fermeture de l'application depuis la croix Windows
        try:
            box = QMessageBox()
            box.setWindowTitle("Quitter ?")
            box.setText("Voulez vous quitter ?")
            box.addButton(QMessageBox.Yes)
            box.addButton(QMessageBox.No)

            ret = box.exec()

            if ret == QMessageBox.Yes:
                self.client.kill()
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
            self.resize(300, 100)
            
            self.__host = QLabel("Host :")
            self.__port = QLabel("Port :")
            self.__enthost = QLineEdit()
            self.__entport = QLineEdit()
            self.__btnaj = QPushButton("Ajouter")
            self.__btnaj.clicked.connect(self._actionAj)
    
            self.__grid = QGridLayout()
            self.setLayout(self.__grid)
            self.__grid.addWidget(self.__host, 0, 0, 1, 1)
            self.__grid.addWidget(self.__enthost, 0, 1, 1, 1)
            self.__grid.addWidget(self.__port, 1, 0, 1, 1)
            self.__grid.addWidget(self.__entport, 1, 1, 1, 1)
            self.__grid.addWidget(self.__btnaj, 2, 1, 1, 1)
    
        def _actionAj(self):
            try:
                letxt = open("host.txt", "a")
                letxt.write("\n" + self.__enthost.text() + "," + self.__entport.text())
                letxt.close()
                self.close()
            except OSError:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Erreur")
                msg.exec()
         
class Infos(QDialog):
    def __init__(self):
            super().__init__()
            self.setWindowTitle("Infos sur la connexion")
            self.resize(300, 100)

            self.__cpubar = QProgressBar()
            self.__cpubar.setValue(cpu)
            self.__cpubar.setFormat("CPU : %p%")
            self.__cpubar.setStyleSheet("background-color: green")
            self.__cpubar.setOrientation(Qt.Horizontal)
            self.__cpubar.setTextVisible(True)
            self.__rambar = QProgressBar()
            self.__rambar.setValue(ram)
            self.__rambar.setFormat("RAM : %p%")
            self.__rambar.setStyleSheet("background-color: green")
            self.__rambar.setOrientation(Qt.Horizontal)
            self.__rambar.setTextVisible(True)
            self.__diskbar = QProgressBar()
            self.__diskbar.setValue(disk)
            self.__diskbar.setFormat("DISK : %p%")
            self.__diskbar.setStyleSheet("background-color: green")
            self.__diskbar.setOrientation(Qt.Horizontal)
            self.__diskbar.setTextVisible(True)

            self.__grid = QGridLayout()
            self.setLayout(self.__grid)
            self.__grid.addWidget(self.__cpubar, 0, 0, 1, 1)
            self.__grid.addWidget(self.__rambar, 1, 0, 1, 1)
            self.__grid.addWidget(self.__diskbar, 2, 0, 1, 1)

            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())



    # bouton "ouvrir une autre co" qui ouvre une nouvelle fenêtre ?