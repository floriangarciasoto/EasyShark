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
# - Tkinter   : sudo apt install python3-tk
# - PIP 3     : sudo pip3 install pyshark
# - WireShark : sudo apt install wireshark
# - TShark    : sudo apt install tshark

# Librairies à installer :
# - pyShark : pip3 install pyshark

# Configuration recommandée :
# - accorder l'accès aux interfaces pour les non-super-utilisateurs (si ce n'est pas le cas, il faudra être super-utilisateur pour faire fonctionner la capture)


# *****************************************
# *             Fonctionnement            *
# *****************************************

# Au choix :
# - Sur le terminal : python3 main.py
# - Utiliser le double click sur le fichier si l'OS le permet.



# --- Libraires ---

import pyshark
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import _thread
import os



# --- Fonctions ---

def commencerStopperCapture():
	global captureEnCours
	if captureEnCours == False:
		captureEnCours = True
		nombreTrames['text'] = 'Aucune trame capturée, en attente de trafic ...'
		boutonCommencerStopper['text'] = 'Stopper'
		_thread.start_new_thread(capture,())
	else:
		captureEnCours = False
		boutonCommencerStopper['text'] = 'Reprendre'

def changerInterface(event):
	global interfaceCaptureEnCours
	interfaceCaptureEnCours = interfaces[listeInterfaces.current()]

def capture():
	global numeroDerniereTrame
	nombreTrames['text'] = 'En attente de trafic ... PING un peu !'
	fenetre.update_idletasks()
	for packet in pyshark.LiveCapture(interface=interfaceCaptureEnCours[0]).sniff_continuously(packet_count=10000):
		if captureEnCours == False:
			break
		numeroDerniereTrame += 1
		ligneTrame = str(numeroDerniereTrame)+'    Sur : '+interfaceCaptureEnCours[1]+'    '
		explicationsTrame = 'Ouais en fait non.'
		if 'eth' in packet:
			ligneTrame += 'Ethernet    '
			if packet.eth.type == '0x00000800':
				ligneTrame += 'IPv4    '
				if packet.ip.proto == '1':
					ligneTrame += 'ICMP'
					if packet.icmp.type == '8':
						ligneTrame += ' PING'
					if packet.icmp.type == '0':
						ligneTrame += ' PONG'
					ligneTrame += '    De %s    à    %s' % (packet.ip.src, packet.ip.dst)
				elif packet.ip.proto == '6':
					ligneTrame += 'TCP    '
					if packet.tcp.dstport == '80':
						ligneTrame += 'HTTP    '
						if packet.tcp.flags_syn == '1':
							ligneTrame += 'Connexion au site : %s' % packet.ip.dst
						elif 'http' in packet:
							if 'urlencoded-form' in packet:
								ligneTrame += 'Regardes-moi le ce con il passe ses paramètres en clair :  '+arg(str(packet['urlencoded-form']))
			elif packet.eth.type == '0x000086dd':
				ligneTrame += 'IPv6     De %s    à    %s    (imbuvable.com)' % (packet.ipv6.src, packet.ipv6.dst)
			elif packet.eth.type == '0x00000806':
				ligneTrame += 'ARP ma gueule !'
			else:
				ligneTrame += 'IPBXv4'
		else:
			ligneTrame += 'Ah ben là C compliqué    '
		listeTrames.insert(END, ligneTrame)
		paquets.append([explicationsTrame,'Trame %d\n%s' % (numeroDerniereTrame,packet)])
		nombreTrames['text'] = 'Trames capturées : %d' % numeroDerniereTrame
		fenetre.update_idletasks()

def reinitialiserCapture():
	global paquets
	global numeroDerniereTrame
	listeTrames.delete(0,len(paquets)-1)
	numeroDerniereTrame = 0
	paquets = list()
	champExplicationsTrame.delete(1.0,END)
	detailsTrame.delete(1.0,END)
	nombreTrames['text'] = 'En attente de trafic à nouveau ...'
	if captureEnCours == False:
		nombreTrames['text'] += ' (faut appuyer sur Reprende en fait)'

def clickSurTrame(event):
	if len(event.widget.curselection()) > 0:
		champExplicationsTrame.delete(1.0,END)
		champExplicationsTrame.insert(END, '%s' % paquets[int(event.widget.curselection()[0])][0])
		detailsTrame.delete(1.0,END)
		detailsTrame.insert(END, '%s' % paquets[int(event.widget.curselection()[0])][1])
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

simplificationsInterfaces = {
	'Câble' : ['enp','eno','eth'],
	'Wifi' : ['wlp'],
	'Loopback' : ['lo']
}

for nomSystemeInterface in os.popen('ip a | grep ^[0-9]*: | cut -d" " -f 2 | sed "s/.$//g"').read().split("\n")[:-1]:
	interfaces.append([nomSystemeInterface,'Inconnue ('+nomSystemeInterface+')'])

for i in range(len(interfaces)):
	for j in simplificationsInterfaces:
		for n in simplificationsInterfaces[j]:
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

Label(fenetre, text='Commences pas choisir l\'interface : ').grid(row=0, column=0, sticky=E)

listeInterfaces = ttk.Combobox(fenetre, values=listeInterfacesValeurs)
listeInterfaces.current(indexInterfaceCaptureEnCours)
listeInterfaces.grid(row=0, column=1, columnspan=2, sticky=W)
listeInterfaces.bind("<<ComboboxSelected>>", changerInterface)

boutonCommencerStopper = tk.Button(fenetre, text='Capturer', command=commencerStopperCapture)
boutonCommencerStopper.grid(row=1,column=0, sticky=E)

tk.Button(fenetre, text='Réiniatiliser', command=reinitialiserCapture).grid(row=1, column=1, sticky=W)

Label(fenetre, text='Liste des trames :').grid(row=2, columnspan=2)

listeTrames = Listbox(fenetre, height=20, width=100)
listeTrames.bind('<<ListboxSelect>>', clickSurTrame)
listeTrames.grid(row=3, columnspan=2)

nombreTrames = Label(fenetre, text='Faut appuyer sur Capturer en fait.')
nombreTrames.grid(row=4, columnspan=2)

Label(fenetre, text='J\'t\'explique : ').grid(row=5, column=0)
champExplicationsTrame = ScrolledText(fenetre, height=10, width=50)
champExplicationsTrame.grid(row=6, column=0)

Label(fenetre, text='Détails imbuvables, regardes pas si t\'es une âme sensible :').grid(row=5, column=1)
detailsTrame = ScrolledText(fenetre, height=10, width=50)
detailsTrame.grid(row=6, column=1)

tk.mainloop()