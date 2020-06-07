# apt update
# apt install python
# apt install python3-tk
# pip3 install pyshark

# sudo python3 main.py [<interface> <nombre de paquets>]

import pyshark
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import _thread
import sys
import os

def commencerCapture():
	global captureEnCours
	captureEnCours = True
	_thread.start_new_thread(capture,())

def changerInterface(event):
	global interfaceCaptureEnCours
	interfaceCaptureEnCours = interfaces[listeInterfaces.current()][0]

def capture():
	i = 0
	nombre['text'] = 'En attente de trafic ... PING un peu !'
	fenetre.update_idletasks()
	capture = pyshark.LiveCapture(interface=interfaceCaptureEnCours)
	for packet in capture.sniff_continuously(packet_count=100):
		print("BC")
		if captureEnCours == False:
			break
		i += 1
		trame = str(i)+'    '
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
		liste.insert(END, trame)
		paquets.append('Trame %d\n%s' % (i,packet))
		nombre['text'] = 'Trames capturées : %d' % i
		fenetre.update_idletasks()

def stopperCapture():
	global captureEnCours
	captureEnCours = False

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

interfaceCaptureEnCours = interfaces[0][0]
captureEnCours = False

listeInterfacesValeurs = list()
for i in interfaces:
	listeInterfacesValeurs.append(i[1])



fenetre = tk.Tk()

fenetre.title('EasyShark')

Label(fenetre, text='Commences pas choisir l\'interface').pack()

listeInterfaces = ttk.Combobox(fenetre, values=listeInterfacesValeurs)
listeInterfaces.current(0)
listeInterfaces.pack()
listeInterfaces.bind("<<ComboboxSelected>>", changerInterface)

tk.Button(fenetre, text='Capturer', command=commencerCapture).pack()

tk.Button(fenetre, text='Stopper', command=stopperCapture).pack()

Label(fenetre, text='Liste des trames :').pack()

liste = Listbox(fenetre, height=20, width=100)
liste.bind('<<ListboxSelect>>', clicktrame)
liste.pack()

nombre = Label(fenetre, text='Aucune trame capturée.')
nombre.pack()

Label(fenetre, text='Détails imbuvables :').pack()

details = ScrolledText(fenetre, height=10, width=100)
details.pack()

tk.mainloop()