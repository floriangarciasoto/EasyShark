# *****************************************
# *      * * * *  EasyShark  * * * *      *
# *        * * * Projet  RT2 * * *        *
# *                                       *
# *          * GARCIA  Florian *          *
# *          * GUIRADO  Adrien *          *
# *          * BANULS Baptiste *          *
# *            * ZHOU Yuhnan *            *
# *****************************************


# *****************************************
# *        Installation nécessaire        *
# *****************************************

# OS nécessaire : Linux

# Paquets à installer :
# - Python 3  : sudo apt install python
# - TKinter   : sudo apt install python3-tk
# - PIP 3     : sudo pip3 install pyshark
# - WireShark : sudo apt install wireshark
# - TShark    : sudo apt install tshark

# Configuration recommandée :
# - accorder l'accès aux interfaces
#   pour les non-super-utilisateurs
#   (si ce n'est pas le cas, il faudra être
#   super-utilisateur pour faire fonctionner
#   la capture)


# *****************************************
# *             Fonctionnement            *
# *****************************************

# Au choix :
# - Sur le terminal : python3 main.py
# - Utiliser le double click sur le fichier
#   si l'OS le permet.



# --- Libraires ---

import pyshark
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import _thread
import os



# --- Fonctions ---

def commencerCapture():
	global captureEnCours
	if captureEnCours == False:
		captureEnCours = True
		_thread.start_new_thread(capture,())

def changerInterface(event):
	global interfaceCaptureEnCours
	interfaceCaptureEnCours = interfaces[listeInterfaces.current()]

def capture():
	global numeroDerniereTrame
	nombre['text'] = 'En attente de trafic ... PING un peu !'
	fenetre.update_idletasks()
	for packet in pyshark.LiveCapture(interface=interfaceCaptureEnCours[0]).sniff_continuously(packet_count=10000):
		if captureEnCours == False:
			break
		numeroDerniereTrame += 1
		trame = str(numeroDerniereTrame)+'    Sur : '+interfaceCaptureEnCours[1]+'    '
		if 'eth' in packet:
			trame += 'Ethernet    '
			if packet.eth.type == '0x00000800':
				trame += 'IPv4    '
				if packet.ip.proto == '1':
					trame += 'ICMP'
					if packet.icmp.type == '8':
						trame += ' PING'
					if packet.icmp.type == '0':
						trame += ' PONG'
					trame += '    De %s    à    %s' % (packet.ip.src, packet.ip.dst)
				elif packet.ip.proto == '6':
					trame += 'TCP    '
					if packet.tcp.dstport == '80':
						trame += 'HTTP    '
						if packet.tcp.flags_syn == '1':
							trame += 'Connexion au site : %s' % packet.ip.dst
						elif 'http' in packet:
							if 'urlencoded-form' in packet:
								trame += 'Regardes-moi le ce con il passe ses paramètres en clair :  '+arg(str(packet['urlencoded-form']))
			elif packet.eth.type == '0x000086dd':
				trame += 'IPv6     De %s    à    %s    (imbuvable.com)' % (packet.ipv6.src, packet.ipv6.dst)
			elif packet.eth.type == '0x00000806':
				trame += 'ARP ma gueule !'
			else:
				trame += 'IPBXv4'
		else:
			trame += 'Ah ben là C compliqué    '
		listeTrames.insert(END, trame)
		paquets.append('Trame %d\n%s' % (numeroDerniereTrame,packet))
		nombre['text'] = 'Trames capturées : %d' % numeroDerniereTrame
		fenetre.update_idletasks()

def stopperCapture():
	global captureEnCours
	captureEnCours = False

def reinitialiserCapture():
	global paquets
	global numeroDerniereTrame
	listeTrames.delete(0,len(paquets)-1)
	numeroDerniereTrame = 0
	paquets = list()
	nombre['text'] = 'Aucune trame capturée.'

def clicktrame(event):
	if len(event.widget.curselection()) > 0:
		details.delete(1.0,END)
		details.insert(END, '%s' % paquets[int(event.widget.curselection()[0])])
		fenetre.update_idletasks()

def arg(packet):
	packet = packet.split('\n')
	packet.pop(0)
	tx = ''
	for i in range(0,len(packet)-1,3):
		tx += packet[i+1][6:]+' : '+packet[i+2][8:]+', '
	return tx[:-2]



# --- Initialisation d'EasyShark ---

interfaces = list()
paquets = list()

simplificationInterfaces = {
	'Câble' : ['enp','eno','eth'],
	'Wifi' : ['wlp'],
	'Loopback' : ['lo']
}

for nomSystemeInterface in os.popen('ip a | grep ^[0-9]*: | cut -d" " -f 2 | sed "s/.$//g"').read().split("\n")[:-1]:
	interfaces.append([nomSystemeInterface,'Inconnue ('+nomSystemeInterface+')'])

for i in range(len(interfaces)):
	for j in simplificationInterfaces:
		for n in simplificationInterfaces[j]:
			if interfaces[i][0][:len(n)] == n:
				interfaces[i][1] = j

interfaceCaptureEnCours = interfaces[0]
indexInterfaceCaptureEnCours = 0
for i in range(len(interfaces)):
	if int(os.popen('ip a s '+interfaces[i][0]+' | head -n 1 | grep "state UP" | wc -l').read()) == 1:
		interfaceCaptureEnCours = interfaces[i]
		indexInterfaceCaptureEnCours = i

captureEnCours = False
numeroDerniereTrame = 0

listeInterfacesValeurs = list()
for i in interfaces:
	listeInterfacesValeurs.append(i[1])



# --- Création de la fenêtre ---

fenetre = tk.Tk()

fenetre.title('EasyShark')

Label(fenetre, text='Commences pas choisir l\'interface : ').grid(row=0, column=0, columnspan=2)

listeInterfaces = ttk.Combobox(fenetre, values=listeInterfacesValeurs)
listeInterfaces.current(indexInterfaceCaptureEnCours)
listeInterfaces.grid(row=0, column=1, columnspan=2)
listeInterfaces.bind("<<ComboboxSelected>>", changerInterface)

tk.Button(fenetre, text='Capturer', command=commencerCapture).grid(row=1,column=0, sticky=E)

tk.Button(fenetre, text='Stopper', command=stopperCapture).grid(row=1,column=1)

tk.Button(fenetre, text='Réiniatiliser', command=reinitialiserCapture).grid(row=1,column=2, sticky=W)

Label(fenetre, text='Liste des trames :').grid(row=2, columnspan=3)

listeTrames = Listbox(fenetre, height=20, width=100)
listeTrames.bind('<<ListboxSelect>>', clicktrame)
listeTrames.grid(row=3, columnspan=3)

nombre = Label(fenetre, text='Aucune trame capturée.')
nombre.grid(row=4, columnspan=3)

Label(fenetre, text='Détails imbuvables, regardes pas si t\'es une âme sensible :').grid(row=5, columnspan=3)

details = ScrolledText(fenetre, height=10, width=100)
details.grid(row=6, columnspan=3)

tk.mainloop()