import pyshark
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import _thread
import os
import sys


class EasyShark:
	def __init__(self):

		self.interfaces = list()
		self.paquets = list()

		self.simplificationsInterfaces = {
			'Câble' : ['enp','eno','eth'],
			'Wifi' : ['wlp'],
			'Loopback' : ['lo']
		}

		for nomSystemeInterface in os.popen('ip a | grep ^[0-9]*: | cut -d" " -f 2 | sed "s/.$//g"').read().split("\n")[:-1]:
			self.interfaces.append([nomSystemeInterface,'Inconnue ('+nomSystemeInterface+')'])

		for i in range(len(self.interfaces)):
			for typeInterface in self.simplificationsInterfaces:
				for premieresLettres in self.simplificationsInterfaces[typeInterface]:
					if self.interfaces[i][0][:len(premieresLettres)] == premieresLettres:
						self.interfaces[i][1] = typeInterface

		self.interfaceCaptureEnCours = self.interfaces[0]
		self.indexInterfaceCaptureEnCours = 0
		for i in range(len(self.interfaces)):
			if int(os.popen('ip a s '+self.interfaces[i][0]+' | head -n 1 | grep "state UP" | wc -l').read()) == 1:
				self.interfaceCaptureEnCours = self.interfaces[i]
				self.indexInterfaceCaptureEnCours = i

		self.captureEnCours = False
		self.numeroDerniereTrame = 0

		self.listeInterfacesValeurs = list()
		for i in self.interfaces:
			self.listeInterfacesValeurs.append(i[1])


		self.fenetre = tk.Tk()

		self.fenetre.title('EasyShark')

		Label(self.fenetre, text='Commences pas choisir l\'interface : ').grid(row=0, column=0, sticky=E)

		self.listeInterfaces = ttk.Combobox(self.fenetre, values=self.listeInterfacesValeurs)
		self.listeInterfaces.current(self.indexInterfaceCaptureEnCours)
		self.listeInterfaces.grid(row=0, column=1, columnspan=2, sticky=W)
		self.listeInterfaces.bind("<<ComboboxSelected>>", self.changerInterface)

		self.boutonCommencerStopper = tk.Button(self.fenetre, text='Capturer', command=self.commencerStopperCapture)
		self.boutonCommencerStopper.grid(row=1,column=0, sticky=E)

		tk.Button(self.fenetre, text='Réiniatiliser', command=self.reinitialiserCapture).grid(row=1, column=1, sticky=W)

		Label(self.fenetre, text='Liste des trames :').grid(row=2, columnspan=2)

		self.listeTrames = Listbox(self.fenetre, height=20, width=100)
		self.listeTrames.bind('<<ListboxSelect>>', self.clickSurTrame)
		self.listeTrames.grid(row=3, columnspan=2)

		self.nombreTrames = Label(self.fenetre, text='Faut appuyer sur Capturer en fait')
		self.nombreTrames.grid(row=4, columnspan=2)

		Label(self.fenetre, text='J\'t\'explique : ').grid(row=5, column=0)
		self.champExplicationsTrame = ScrolledText(self.fenetre, height=10, width=50)
		self.champExplicationsTrame.grid(row=6, column=0)

		Label(self.fenetre, text='Détails imbuvables, regardes pas si t\'es une âme sensible :').grid(row=5, column=1)
		self.detailsTrame = ScrolledText(self.fenetre, height=10, width=50)
		self.detailsTrame.grid(row=6, column=1)

		self.fenetre.mainloop()


	def commencerStopperCapture(self):
		if self.captureEnCours == False:
			self.captureEnCours = True
			self.boutonCommencerStopper['text'] = 'Stopper'
			_thread.start_new_thread(self.capture,())
		else:
			self.captureEnCours = False
			self.boutonCommencerStopper['text'] = 'Reprendre'
			self.nombreTrames['text'] += ' (capture stoppée)'

	def changerInterface(self, event):
		self.interfaceCaptureEnCours = self.interfaces[self.listeInterfaces.current()]

	def capture(self):
		self.nombreTrames['text'] = 'En attente de trafic ... PING un peu !'
		self.fenetre.update_idletasks()
		for trame in pyshark.LiveCapture(interface=self.interfaceCaptureEnCours[0]).sniff_continuously(packet_count=10000):
			if self.captureEnCours == False:
				break
			self.numeroDerniereTrame += 1
			ligneTrame = str(self.numeroDerniereTrame)+'    Sur : '+self.interfaceCaptureEnCours[1]+'    '
			explicationsTrame = 'Ouais en fait non.'
			if 'eth' in trame:
				ligneTrame += 'Ethernet    '
				if trame.eth.type == '0x00000800':
					ligneTrame += 'IPv4    '
					if trame.ip.proto == '1':
						ligneTrame += 'ICMP'
						if trame.icmp.type == '8':
							ligneTrame += ' PING'
						if trame.icmp.type == '0':
							ligneTrame += ' PONG'
						ligneTrame += '    De %s    à    %s' % (trame.ip.src, trame.ip.dst)
					elif trame.ip.proto == '6':
						ligneTrame += 'TCP    '
						if trame.tcp.dstport == '80':
							ligneTrame += 'HTTP    '
							if trame.tcp.flags_syn == '1':
								ligneTrame += 'Connexion au site : %s' % trame.ip.dst
							elif 'http' in trame:
								if 'urlencoded-form' in trame:
									ligneTrame += 'Regardes-moi le ce con il passe ses paramètres en clair :  '
									argumentsHTTP = str(trame['urlencoded-form']).split('\n')[1:]
									for i in range(0,len(argumentsHTTP)-1,3):
										ligneTrame += argumentsHTTP[i+1][6:]+' : '+argumentsHTTP[i+2][8:]+', '
				elif trame.eth.type == '0x000086dd':
					ligneTrame += 'IPv6     De %s    à    %s    (imbuvable.com)' % (trame.ipv6.src, trame.ipv6.dst)
				elif trame.eth.type == '0x00000806':
					ligneTrame += 'ARP ma gueule !'
				else:
					ligneTrame += 'IPBXv4'
			else:
				ligneTrame += 'Ah ben là C compliqué    '
			self.listeTrames.insert(END, ligneTrame)
			self.paquets.append([explicationsTrame,'Trame %d\n%s' % (self.numeroDerniereTrame,trame)])
			self.nombreTrames['text'] = 'Trames capturées : %d' % self.numeroDerniereTrame
			self.fenetre.update_idletasks()

	def reinitialiserCapture(self):
		self.listeTrames.delete(0,len(self.paquets)-1)
		self.numeroDerniereTrame = 0
		self.paquets = list()
		self.champExplicationsTrame.delete(1.0,END)
		self.detailsTrame.delete(1.0,END)
		self.nombreTrames['text'] = 'En attente de trafic à nouveau ...'
		if self.captureEnCours == False:
			self.nombreTrames['text'] += ' (faut appuyer sur Reprende en fait)'

	def clickSurTrame(self, event):
		if len(event.widget.curselection()) > 0:
			self.champExplicationsTrame.delete(1.0,END)
			self.champExplicationsTrame.insert(END, '%s' % self.paquets[int(event.widget.curselection()[0])][0])
			self.detailsTrame.delete(1.0,END)
			self.detailsTrame.insert(END, '%s' % self.paquets[int(event.widget.curselection()[0])][1])
			self.fenetre.update_idletasks()

if(len(sys.argv)>1 and sys.argv[1]=='-i'):	
	app = tk.Tk()
	app.geometry('400x200')
	lab=tk.Label(app,text="\n\n\n\nNon mais arrête c'est pas l'heure de te DPKG -i là !",wraplength=400,justify=tk.LEFT)
	lab.pack()
	app.mainloop()

else:
	if __name__ == '__main__':
		EasyShark()
