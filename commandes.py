import mainserveur
import platform
import psutil
import subprocess
import sys
import json  # sera utilisé si j'ai le temps une fois les principales fonctionnalités implémentées


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

    elif msg == 'getall':
        return getall()

    elif msg == 'disconnect':
        return ''

    elif msg == 'connexion information':
        return f"IP: {getip()}\nName: {getname()}"

    elif msg == 'kill':
        return ''

    elif msg == 'reset':
        return ''

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
    ramtotal = psutil.virtual_memory().total / 1024 / 1024 / \
        1024  # conversion en Go, on pourrait aussi diviser par 1 073 741 824.
    ramlibre = psutil.virtual_memory().free / 1024 / 1024 / 1024
    ramutil = psutil.virtual_memory().used / 1024 / 1024 / 1024
    return f"RAM totale: {round(ramtotal, 2)} Go, RAM libre: {round(ramlibre, 2)} Go, RAM utilisée: {round(ramutil, 2)} Go"


def getcpu():  # fonction qui renvoi l'utilisation du processeur
    cpu = str(psutil.cpu_percent())
    return f"Utilisation du processeur: {cpu}%"


def getip():  # fonction qui renvoi l'adresse IP du serveur en fonction de son OS

    # version en utilisant subprocess
    if sys.platform == 'win32':  # récupération de l'IP si l'OS est Windows
        ipconfig = subprocess.Popen(
            'ipconfig', shell=True, stdout=subprocess.PIPE).stdout.read().decode(errors='ignore')
        # mise en forme de l'adresse IP pour l'affichage
        ip = str(ipconfig.split('IPv4')[1].split(':')[1].split(' ')[1])
        return ip.rstrip()  # enlève le retour à la ligne

    elif sys.platform == 'linux':  # récupération de l'IP si l'OS est Linux
        ip = subprocess.Popen(
            "ip a | grep inet | grep global | awk '{print $2}'", shell=True, stdout=subprocess.PIPE).stdout.read().decode()
        # mise en forme de l'adresse IP pour l'affichage
        ip = ip.split("\n")[:-1]
        return ip

    # récupération de l'IP si l'OS est Mac (Darwin)
    elif sys.platform == 'darwin':
        ip = subprocess.Popen(
            'ifconfig en0 | grep inet | awk \'$1=="inet" {print $2}\'', shell=True, stdout=subprocess.PIPE).stdout.read().decode()
        return ip  # trouvé sur internet pusique je n'ai pas de Mac pour tester la commande

    # version en utilisant psutil

    """from socket import AF_INET
    from ipaddress import IPv4Network

    def get_ip():
        ipaddr = []    
        for nic, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                address = addr.address
                # Permet d'ignorer les adresses de type 169.254.x.x sur mon ordinateur
                if addr.family == AF_INET and not address.startswith("169.254"):
                    ipaddr.append(f"{address}/{IPv4Network('0.0.0.0/' +  addr.netmask).prefixlen}")
        return ipaddr"""


def getname():  # fonction qui renvoi le nom du serveur
    return platform.node()


def getall():  # fonction qui renvoi toutes les informations
    return f"OS: {getos()}\n RAM: {getram()}\n CPU: {getcpu()}\n IP: {getip()}\n Name: {getname()}"


# commandes libres
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

"""def getgraph(self):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from psutil import cpu_percent

    x = []
    y = []
    longueur = 200 
    figure = plt.figure(figsize=(10, 6)) # Création de la figure

    def graph(i):
        x.append(i)
        y.append(cpu_percent())
        
        if len(y) <= longueur:
            plt.cla()
            plt.plot(y, 'b' ,label='Utilisation du processeur') # Création du graphique
        
        else:
            plt.cla()
            plt.plot(y[-longueur:], 'b' ,label='Utilisation du processeur')

        plt.ylim(0, 100) # Limitation de l'axe des ordonnées
        plt.xlabel('Temps (s)') # Label de l'axe des abscisses
        plt.ylabel('Utilisation du processeur (%)') # Label de l'axe des ordonnées
        plt.legend(loc='upper right') # Affichage de la légende
        plt.tight_layout() # Ajustement de la figure


    ani = FuncAnimation(plt.gcf(), graph, interval=1000)

    plt.show()"""


def main():
    mainserveur.Serveur()
