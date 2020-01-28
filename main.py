# apt update
# apt install python
# apt install python3-tk
# pip3 install pyshark

# sudo python3 main.py

import pyshark
import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import _thread

capture = pyshark.LiveCapture(interface='lo')
paquets = list()

def caps():
	_thread.start_new_thread(captures,())

def captures():
	i = 0
	nombre['text'] = 'En attente de trafic ... PING un peu !'
	fenetre.update_idletasks()
	for packet in capture.sniff_continuously(packet_count=100):
		i += 1
		trame = str(i)+'    '
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
			trame += 'IPv6    '
			trame += 'De %s    à    %s    (imbuvable.com)' % (packet.ipv6.src, packet.ipv6.dst)
		elif packet.eth.type == '0x00000806':
			trame += 'ARP'
		else:
			trame += 'IPBXv4'
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
	params = list()
	for i in range(0,len(packet)-1,3):
		params.append([packet[i+1][6:],packet[i+2][8:]])
	tx = ''
	for i in range(len(params)):
		tx += params[i][0]+' : '+params[i][1]
		if i < len(params)-1:
			tx += ', '
	return tx


fenetre = tk.Tk()
fenetre.title('EasyShark')
liste = Listbox(fenetre, height=20, width=100)
liste.bind('<<ListboxSelect>>', clicktrame)
liste.pack()
nombre = Label(fenetre, text='Appuies sur le bouton en bas et tu verras.')
nombre.pack()
details = ScrolledText(fenetre, height=10, width=100)
details.pack()
tk.Button(fenetre, text='Capture capture et tu verras', command=caps).pack()
tk.mainloop()