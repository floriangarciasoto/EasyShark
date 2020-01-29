# apt update
# apt install python
# apt install python3-tk
# pip3 install pyshark

# sudo python3 main.py [<interface> <nombre de paquets>]

import pyshark
import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import _thread
import sys

interf = 'any'
mx = 100
if len(sys.argv) > 1:
	interf = str(sys.argv[1])
if len(sys.argv) > 2:
	mx = int(sys.argv[2])

capture = pyshark.LiveCapture(interface=interf)
paquets = list()

def caps():
	_thread.start_new_thread(captures,())

def captures():
	i = 0
	nombre['text'] = 'En attente de trafic ... PING un peu !'
	fenetre.update_idletasks()
	for packet in capture.sniff_continuously(packet_count=mx):
		i += 1
		trame = str(i)+'    '
		if 'eth' in packet:
			trame += 'Ethernet    '
			if packet[0].type == '0x00000800':
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
			elif packet[0].type == '0x000086dd':
				trame += 'IPv6     De %s    à    %s    (imbuvable.com)' % (packet.ipv6.src, packet.ipv6.dst)
			elif packet[0].type == '0x00000806':
				trame += 'ARP ma gueule !'
			else:
				trame += 'IPBXv4'
		else:
			trame += 'Ah ben là C compliqué    '
		liste.insert(END, trame)
		paquets.append('Trame %d\n%s' % (i,packet))
		nombre['text'] = 'Trames capturées : %d' % i
		fenetre.update_idletasks()

def clicktrame(evt):
	if len(evt.widget.curselection()) > 0:
		details.delete(1.0,END)
		details.insert(END, '%s' % paquets[int(evt.widget.curselection()[0])])
		fenetre.update_idletasks()

def arg(packet):
	packet = packet.split('\n')
	packet.pop(0)
	tx = ''
	for i in range(0,len(packet)-1,3):
		tx += packet[i+1][6:]+' : '+packet[i+2][8:]+', '
	return tx[:-2]

fenetre = tk.Tk()
fenetre.title('EasyShark')
Label(fenetre, text='Capture de %d paquets sur l\'interface %s' % (mx,interf)).pack()
liste = Listbox(fenetre, height=20, width=100)
liste.bind('<<ListboxSelect>>', clicktrame)
liste.pack()
nombre = Label(fenetre, text='Appuies sur le bouton en bas et tu verras.')
nombre.pack()
details = ScrolledText(fenetre, height=10, width=100)
details.pack()
tk.Button(fenetre, text='Capture capture et tu verras', command=caps).pack()
tk.mainloop()