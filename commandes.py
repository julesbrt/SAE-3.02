import mainserveur
import platform
import psutil
import subprocess
import sys

def reponse(self, data, reply): #fonction de réponse
    if data == 'OS':
        getos()

    elif data == 'RAM':
        getram()
    
    elif data == 'CPU':
        getcpu()

    elif data == 'IP':
        getip()

    elif data == 'Name':
        getname()

    

def getos(): #fonction qui renvoi le système d'exploitation
    return platform.system()

def getram(): #fonction qui renvoi la mémoire vive
    return psutil.virtual_memory().total

def getcpu(): #fonction qui renvoi l'utilisation du processeur
    return psutil.cpu_percent()
     
def getip(): #fonction qui renvoi l'adresse IP du serveur en fonction de son OS
    
    if sys.platform == 'win32': #récupération de l'IP si l'OS est Windows
        ipconfig = subprocess.Popen('ipconfig', shell=True, stdout=subprocess.PIPE).stdout.read().decode()
        ip = ipconfig.split('IPv4')[1].split(':')[1].split(' ')[1]
        return ip

    elif sys.platform == 'linux': #récupération de l'IP si l'OS est Linux
        ip = subprocess.Popen("ip a | grep inet | grep global | awk '{print $2}'"), shell=True, stdout=subprocess.PIPE.stdout.read().decode()
        ip = ip.split("\n")[:-1] 
        return ip

    elif sys.platform == 'darwin': #récupération de l'IP si l'OS est Mac (Darwin)
        ip = subprocess.Popen('ifconfig en0 | grep inet | awk \'$1=="inet" {print $2}\'', shell=True, stdout=subprocess.PIPE).stdout.read().decode() 
        return ip #trouvé sur internet pusique je n'ai pas de Mac pour tester la commande
    
def getname(): #fonction qui renvoi le nom du serveur
    return platform.node()

def main():
    mainserveur.Serveur()