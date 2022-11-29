import mainserveur
import platform
import psutil
import subprocess
import sys
import json

"""DOScmd = []
Lcmd = []
Pwcmd = []
cmd = []

def commandes(self, msg, DOScmd, Lcmd, Pwcmd, cmd):
    if msg == 'dir' or msg == 'mkdir':
        DOScmd.append(msg)

    elif msg == 'ls -la':
        Lcmd.append(msg)

    elif msg == 'get-process':
        Pwcmd.append(msg)

    elif msg == 'python --version' or msg == 'ping  192.157.65.78':
        cmd.append(msg)
        
    if platform.system() == 'win32':
        for i in DOScmd:
            return subprocess.Popen(i, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    
    if platform.system() == 'linux':
        for i in Lcmd:
            return subprocess.Popen(i, shell=True, stdout=subprocess.PIPE).stdout.read().decode()
    
    if platform.system() == 'darwin':
        for i in Pwcmd:
            return subprocess.Popen(i, shell=True, stdout=subprocess.PIPE).stdout.read().decode()"""


def reponse(msg):  # fonction de réponse
    if msg == 'OS':
        return getos()

    elif msg == 'RAM':
        return getram()

    elif msg == 'CPU':
        return getcpu()

    elif msg == 'IP':
        return getip()

    elif msg == 'Name':
        return getname()
    else:
        return 'Commande inconnue'


def getos():  # fonction qui renvoi le système d'exploitation
    return platform.system()


def getram():  # fonction qui renvoi la mémoire vive
    """return json.dumps({
            'total': str(psutil.virtual_memory().total),
            'used': str(psutil.virtual_memory().used),
            'free': str(psutil.virtual_memory().free)
        })"""
    ramtotal = psutil.virtual_memory().total/ 1024 / 1024 / 1024
    ramlibre = psutil.virtual_memory().free/ 1024 / 1024 / 1024
    ramutil = psutil.virtual_memory().used/ 1024 / 1024 / 1024
    return f"RAM totale: {round(ramtotal, 2)} Go, RAM libre: {ramlibre} Go, RAM utilisée: {ramutil} Go"


def getcpu():  # fonction qui renvoi l'utilisation du processeur
    return str(psutil.cpu_percent())


def getip():  # fonction qui renvoi l'adresse IP du serveur en fonction de son OS

    if sys.platform == 'win32':  # récupération de l'IP si l'OS est Windows
        ipconfig = subprocess.Popen(
            'ipconfig', shell=True, stdout=subprocess.PIPE).stdout.read().decode()
        ip = ipconfig.split('IPv4')[1].split(':')[1].split(' ')[1]
        return ip

    elif sys.platform == 'linux':  # récupération de l'IP si l'OS est Linux
        ip = subprocess.Popen(
            "ip a | grep inet | grep global | awk '{print $2}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode()
        ip = ip.split("\n")[:-1]
        return ip

    # récupération de l'IP si l'OS est Mac (Darwin)
    elif sys.platform == 'darwin':
        ip = subprocess.Popen(
            'ifconfig en0 | grep inet | awk \'$1=="inet" {print $2}\'', shell=True, stdout=subprocess.PIPE).stdout.read().decode()
        return ip  # trouvé sur internet pusique je n'ai pas de Mac pour tester la commande


def getname():  # fonction qui renvoi le nom du serveur
    return platform.node()


def main():
    mainserveur.Serveur()
