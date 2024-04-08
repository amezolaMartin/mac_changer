#!/usr/bin/python3


"""MAC CHANGER
Author: Martin Amezola
Github: @amezolaMartin
Version: 1.0
"""

import argparse
import re
import socket
import subprocess
from termcolor import colored
import sys
import signal


def welcome():
    print(colored(r"""      ____  _                 _                               
     / ___|(_)_ __ ___  _ __ | | ___                          
     \___ \| | '_ ` _ \| '_ \| |/ _ \                         
      ___) | | | | | | | |_) | |  __/                         
     |____/|_|_| |_| |_| .__/|_|\___|                         
  __  __               |_|_ _                                 
 |  \/  | __ _  ___   / ___| |__   __ _ _ __   __ _  ___ _ __ 
 | |\/| |/ _` |/ __| | |   | '_ \ / _` | '_ \ / _` |/ _ \ '__|
 | |  | | (_| | (__  | |___| | | | (_| | | | | (_| |  __/ |   
 |_|  |_|\__,_|\___|  \____|_| |_|\__,_|_| |_|\__, |\___|_|   
                                              |___/
                By Martin Amezola
                Github: @amezolaMartin""", "red"))

def def_handler(sig, frame):
    print(colored("\n[!] Saliendo del programa... ", "red"))
    sys.exit(1)

# Asigna la función de manejo de señales al evento SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, def_handler)

def get_arguments():
    parser = argparse.ArgumentParser(description='Herramienta para cambiar la direccion MAC de una interfaz de red.')
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Nombre de la interfaz de red.")
    parser.add_argument("-m", "--mac", required=True, dest="mac_adress", help="Nueva direccion MAC para la interfaz de red.")

    return parser.parse_args() # Devuelvo los argumentos 

def validar(interface, mac_adress):
    # Con la libreria socket obtengo las interfaces de red.
    interface_list = socket.if_nameindex()

    existe_interfaz = any(interface in tupla for _,tupla in interface_list) # Compruebo si existe en la lista de interfaces
    existe_direccion_mac = re.match(r'^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}$', mac_adress)
    
    return existe_interfaz and existe_direccion_mac

    
def change_mac_adress(interface, mac_adress):
    if validar(interface, mac_adress): # Compruebo si son validos
        subprocess.run(["ifconfig", interface, "down"])
        subprocess.run(["ifconfig", interface, "hw", "ether", mac_adress])
        subprocess.run(["ifconfig", interface, "up"])

        print(colored(f"\n[OK] La MAC ha sido cambiada exitosamente!", "green"))
    else:
        print(colored(f"\n[ERROR] Los datos introducidos no son correctos.", "red"))
        
def main():
    args = get_arguments()
    change_mac_adress(args.interface, args.mac_adress)

if __name__ == '__main__':
    welcome()
    main()