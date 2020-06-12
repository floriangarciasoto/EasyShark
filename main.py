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
# - WireShark : sudo apt install wireshark
# - TShark    : sudo apt install tshark
# - Python 3  : sudo apt install python
# - Tkinter   : sudo apt install python3-tk

# Librairies à installer :
# - pyShark : pip3 install pyshark

# Configuration recommandée :
# - Permettre aux non-super-utilisateurs de capturer :
#   - sudo apt-get install wireshark
#   - sudo dpkg-reconfigure wireshark-common 
#   - sudo usermod -a -G wireshark $USER
#   - gnome-session-quit --logout --no-prompt
# - Si le programme doit marcher en super-utilisateurs :
#   - sudo pip3 install pyshark


# *****************************************
# *             Fonctionnement            *
# *****************************************

# Au choix :
# - Sur le terminal : python3 main.py
# - Utiliser le double clic sur le fichier si l'OS le permet.



# ***** Librairies *****

# *** pyShark ***
# Importation de pyshark pour la capture de trames avec Python
import pyshark

# *** Tkinter ***
# Utilisation de l'alias tk pour référer à tkinter
import tkinter as tk
# Importation de tous les sous éléments de la librairie pour l'utilisation des méthodes et des widgets
from tkinter import *
# Importation de la partie ttk pour la liste déroulante Combobox
from tkinter import ttk
# Importation de ScrolledText depuis la partie scrolledtext de tkinter
from tkinter.scrolledtext import ScrolledText

# *** Threading pour Python 3 ***
# Importation de _thread pour lancer en parallèle la fonction de capture de trames
import _thread

# *** Liaison avec l'OS ***
# Importation d'os pour le retour des commandes UNIX sur les interfaces réseaux
import os



# ***** EasyShark *****

# Définition de la classe EasyShark représentant l'instance de travail de l'application
class EasyShark:

	# **** Constructeur ****
	def __init__(self):

		# *** Prise en compte des interfaces réseaux ***

		# Tableau qui va contenir les interfaces réseaux
		self.interfaces = list()

		# Objet contenant la conversion des noms systèmes d'interfaces en nom à afficher à l'écran
		self.simplificationsInterfaces = {
			'Câble' : ['enp','eno','eth'],
			'Wifi' : ['wlp'],
			'Loopback' : ['lo']
		}

		# Pour chaque interface obtenue depuis la console
		for nomSystemeInterface in os.popen('ip a | grep ^[0-9]*: | cut -d" " -f 2 | sed "s/.$//g"').read().split("\n")[:-1]:

			# Nom par défaut qui sera affiché dans la liste déroulante
			nomEcran = 'Inconnue ('+nomSystemeInterface+')'
			# Pour chaque type d'inteface
			for typeInterface in self.simplificationsInterfaces:
				# Pour chaque commencement de chaque type
				for premieresLettres in self.simplificationsInterfaces[typeInterface]:
					# Si les premières lettres sont les mêmes
					if nomSystemeInterface[:len(premieresLettres)] == premieresLettres:
						# Le nom affiché à l'écran sera le type d'interface
						nomEcran = typeInterface

			# Boolean permettant de savoir si l'interface peut capturer ou non
			interfaceActive = False
			# Si l'OS nous dit que l'interface est active
			if int(os.popen('ip a s '+nomSystemeInterface+' | head -n 1 | grep "state UP" | wc -l').read()) == 1:
				# On spécifie la capacité de l'interface à capturer
				interfaceActive = True

			# Ajout au tableau des interfaces le nom système, le nom pour l'affichage et la capacité de capture de l'interface
			self.interfaces.append([nomSystemeInterface,nomEcran,interfaceActive])

		# Définition de l'index par défaut pour la liste déroulante
		self.indexInterfaceCaptureEnCours = 0
		# Pour chaque interface
		for i in range(len(self.interfaces)):
			# Si l'interface est active
			if self.interfaces[i][2] == True:
				# On remplace l'index par celui de celle qui correspond
				self.indexInterfaceCaptureEnCours = i

		# Tableau qui va contenir tous les noms des interfaces à afficher à l'écran
		listeInterfacesValeurs = list()
		# Pour chaque interface
		for i in self.interfaces:
			# On ajoute au tableau le nom à afficher à l'écran
			listeInterfacesValeurs.append(i[1])


		# *** Initialisation des variables utiles à la capture ***

		# Tableau qui va contenir les trames capturées
		self.trames = list()

		# Boolean permettant de savoir si la capture est en cours
		self.captureEnCours = False

		# Entier permettant de numéroter les trames capturées, le compteur de trames
		self.numeroDerniereTrame = 0


		# *** Création de la fenêtre ***

		# Création de la variable globale fenêtre afin d'y ajouter nos éléments
		self.fenetre = tk.Tk()

		# Ajout du titre de la fenêtre
		self.fenetre.title('EasyShark')

		# Création et ajout du texte à côté de la liste déroulante des interfaces
		Label(self.fenetre, text='Commences pas choisir l\'interface : ').grid(row=0, column=0, sticky=E)

		# Création du widget Combobox permettant de créer la liste déroulante
		self.listeInterfaces = ttk.Combobox(self.fenetre, values=listeInterfacesValeurs)
		# Choix par défaut de la liste en fonction de l'interface de capture choisie
		self.listeInterfaces.current(self.indexInterfaceCaptureEnCours)
		# Ajout de la liste à la fenêtre
		self.listeInterfaces.grid(row=0, column=1, columnspan=2, sticky=W)
		# Liaison de l'événement lors du changement de la liste avec la fonction de changement d'interface
		self.listeInterfaces.bind('<<ComboboxSelected>>', self.changerInterface)

		# Création du bouton déclencheur de la capture
		self.boutonCommencerStopper = tk.Button(self.fenetre, text='Capturer', command=self.commencerStopperCapture)
		# Ajout du bouton à la fenêtre à côté du texte
		self.boutonCommencerStopper.grid(row=1,column=0, sticky=E)

		# Création et ajout du bouton déclencheur de la réiniatilisation de la capture
		tk.Button(self.fenetre, text='Réiniatiliser', command=self.reinitialiserCapture).grid(row=1, column=1, sticky=W)

		# Création et ajout du texte au-dessus de la liste des trames
		Label(self.fenetre, text='Liste des trames :').grid(row=2, columnspan=2)

		# Création de la liste des trames
		self.listeTrames = Listbox(self.fenetre, height=20, width=100)
		# Ajout de la liste des trames
		self.listeTrames.grid(row=3, columnspan=2)
		# Liaison de l'événement lors d'un clic sur la liste avec la fonction du clic sur une trame
		self.listeTrames.bind('<<ListboxSelect>>', self.clickSurTrame)

		# Création du texte en bas de la liste des trames
		self.nombreTrames = Label(self.fenetre, text='Faut appuyer sur Capturer en fait')
		# Ajout du texte à la fenêtre
		self.nombreTrames.grid(row=4, columnspan=2)

		# Création et ajout du texte en haut des explications
		Label(self.fenetre, text='J\'t\'explique : ').grid(row=5, column=0)
		# Création du champ d'explications de la trame
		self.champExplicationsTrame = ScrolledText(self.fenetre, height=10, width=50)
		# Ajout du champ à la fenêtre
		self.champExplicationsTrame.grid(row=6, column=0)

		# Création et ajout du texte en haut des détails
		Label(self.fenetre, text='Détails imbuvables, ne regardes pas si tu es nature fragile et sensible :').grid(row=5, column=1)
		# Création du champ d'explications des détails de la trame
		self.detailsTrame = ScrolledText(self.fenetre, height=10, width=50)
		# Ajout du champ à la fenêtre
		self.detailsTrame.grid(row=6, column=1)

		# Mise en route de la fenêtre
		self.fenetre.mainloop()


	# **** Contrôle de la capture ****
	def commencerStopperCapture(self):
		# Si la capture n'est pas en cours
		if self.captureEnCours == False:
			# On indique qu'elle l'est maintenant
			self.captureEnCours = True
			# Modification du texte du bouton enclenché
			self.boutonCommencerStopper['text'] = 'Stopper'
			# Lancement en arrière-plan de la fonction de capture
			_thread.start_new_thread(self.capture,())
		# Si la capture est en cours
		else:
			# On indique qu'elle ne l'est plus
			self.captureEnCours = False
			# Modification du texte du bouton enclenché
			self.boutonCommencerStopper['text'] = 'Reprendre'
			# Ajout d'un texte informatif en bas de la liste des trames
			self.nombreTrames['text'] += ' (capture stoppée)'


	# **** Contrôle de l'interface réseau ****
	def changerInterface(self, event):
		# Remplacement de l'index de l'interface en cours d'utilisation par celui de la nouvelle
		self.indexInterfaceCaptureEnCours = self.listeInterfaces.current()


	# **** Contrôle de la capture ****
	def capture(self):

		# *** Initialisation de la capture ***

		# Remplacement du texte en bas signifant l'attente d'éventuelles trames
		self.nombreTrames['text'] = 'En attente de trafic ... PING un peu !'
		# Mise à jour de la fenêtre
		self.fenetre.update_idletasks()


		# *** Boucle sur chaque trame ***

		# Pour chaque trame capturée sur l'interface spécifiée
		for trame in pyshark.LiveCapture(interface=self.interfaces[self.indexInterfaceCaptureEnCours][0]).sniff_continuously(packet_count=10000):
			# Si la capture n'est pas censée être en cours
			if self.captureEnCours == False:
				# On stoppe la boucle
				break
			# Incrémentation du compteur de trames
			self.numeroDerniereTrame += 1
			# Début par défaut pour la chaîne de caractères présente sur la ligne de la trame dans la liste des trames
			ligneTrame = str(self.numeroDerniereTrame)+'    Sur : '+self.interfaces[self.indexInterfaceCaptureEnCours][1]+'    '
			# Texte explicatif par défaut au cas où les explications ne sont pas fournies pour la trame
			explicationsTrame = 'Ouais en fait non.'


			# *** Obtention des informations et établissement des explications ***

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
									parametresURL = str(trame['urlencoded-form']).split('\n')[1:]
									for i in range(0,len(parametresURL)-1,3):
										ligneTrame += parametresURL[i+1][6:]+' : '+parametresURL[i+2][8:]+', '
				elif trame.eth.type == '0x000086dd':
					ligneTrame += 'IPv6     De %s    à    %s    (imbuvable.com)' % (trame.ipv6.src, trame.ipv6.dst)
				elif trame.eth.type == '0x00000806':
					ligneTrame += 'ARP ma gueule !'
				else:
					ligneTrame += 'IPBXv4'
			else:
				ligneTrame += 'Ah ben là C compliqué    '


			# *** Application des explications obtenues ***

			# Insertion de la ligne de texte de la trame formée dans la liste des trames
			self.listeTrames.insert(END, ligneTrame)
			# Ajout du texte explicatif ainsi que des détails obtenus au tableau des trames
			self.trames.append([explicationsTrame,'Trame %d\n%s' % (self.numeroDerniereTrame,trame)])
			# Mise à jour du texte en bas signifiant le nombre de trames capturées
			self.nombreTrames['text'] = 'Trames capturées : %d' % self.numeroDerniereTrame
			# Mise à jour de la fenêtre
			self.fenetre.update_idletasks()


	# **** Réinitialisation de la capture ****
	def reinitialiserCapture(self):
		# Suppression de toutes les lignes dans la liste des trames
		self.listeTrames.delete(0,END)
		# Remise à 0 du compteur de trames
		self.numeroDerniereTrame = 0
		# Vidage du tableau contenant les trames
		self.trames = list()
		# Effacement du champ des explications
		self.champExplicationsTrame.delete(1.0,END)
		# Effacement du champ des détails
		self.detailsTrame.delete(1.0,END)
		# Remplacement du texte en bas de la liste des trames
		self.nombreTrames['text'] = 'En attente de trafic à nouveau ...'
		# Si la capture n'est pas en cours
		if self.captureEnCours == False:
			# On spécifie à l'utilisateur de la réactiver
			self.nombreTrames['text'] += ' (faut appuyer sur Reprende en fait)'


	# **** Lors d'un clic sur une trame ****
	def clickSurTrame(self, event):
		# Si au moins une trame est seléctionnée
		if len(self.listeTrames.curselection()) > 0:
			# Utilisation d'un index temporaire pour la seléction de la trame
			indexSelection = self.listeTrames.curselection()[0]
			# Effacement du champ des explications afin d'y remplacer le contenu
			self.detailsTrame.delete(1.0,END)
			# Remplissage du champ avec les explications de la trame correspondante
			self.detailsTrame.insert(END, '%s' % self.trames[indexSelection][1])
			# Effacement du champ des détails afin d'y remplacer le contenu
			self.champExplicationsTrame.delete(1.0,END)
			# Remplissage du champ avec les détails de la trame correspondante
			self.champExplicationsTrame.insert(END, '%s' % self.trames[indexSelection][0])


# **** Démarrage de l'application ****

# Si le programme n'est pas importé depuis un autre programme
if __name__ == '__main__':
	# Démarrage de l'instance de l'application
	EasyShark()
