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

capture = pyshark.LiveCapture(interface='wlp4s0')
paquets = list()

def caps():
	_thread.start_new_thread(captures,())

def captures():
	i = 0
	nombre['text'] = 'Capture en cours ...'
	fenetre.update_idletasks()
	for packet in capture.sniff_continuously(packet_count=100):
		i += 1
		trame = str(i)+'    '
		if packet[0].type == '0x00000800':
			trame += 'IPv4    '
			if packet.ip.proto == '1':
				trame += 'ICMP'
				if packet.icmp.type == '8':
					trame += ' PING'
				if packet.icmp.type == '0':
					trame += ' PONG'
				trame += '    '
			trame += 'De %s    à    %s' % (packet.ip.src, packet.ip.dst)
		elif packet[0].type == '0x000086dd':
			trame += 'IPv6    '
			trame += 'De %s    à    %s    (imbuvable)' % (packet.ipv6.src, packet.ipv6.dst)
		else:
			trame += 'PABXv4'
		liste.insert(END, trame)
		paquets.append('Trame '+str(i)+'\n'+str(packet))
		nombre['text'] = 'Trames capturées : %d' % i
		fenetre.update_idletasks()

def clicktrame(evt):
	if len(evt.widget.curselection()) > 0:
		details.delete(1.0,END)
		details.insert(END, '%s' % paquets[int(evt.widget.curselection()[0])])
		fenetre.update_idletasks()

fenetre = tk.Tk()
fenetre.title('Easyshark')
liste = Listbox(fenetre, height=20, width=100)
liste.bind('<<ListboxSelect>>', clicktrame)
liste.pack()
nombre = Label(fenetre, text='Appuies sur le bouton en bas et tu verras.')
nombre.pack()
details = ScrolledText(fenetre, height=10, width=100)
details.pack()
tk.Button(fenetre, text='Captures captures et tu verras', command=caps).pack()
tk.mainloop()