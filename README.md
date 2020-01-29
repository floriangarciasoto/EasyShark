# EasyShark
Projet RT2 sur un Wireshark simplifié
## Introduction
### But du projet
Le but de notre projet est de proposer un Wireshark simplifié. Nous devons proposer un logiciel qui soit simple d'utilisation et compréhensible par des étudiants qui arrivent en première année.
### Objectifs demandés
L'objectif de notre projet est de faire un programme permettant de visualiser de manière graphique les paquets circulant sur un réseau informatique. La différence avec les logiciels déjà existant est que cela doit être compréhensible par tout le monde, même les gens non initiés.
### Solution proposée
Pour réaliser notre projet, nous avions principalement le choix entre deux langages de programmation possibles : C et Python. Nous avons choisi la deuxième option car nous sommes plus familier avec Python. Ensuite, il a fallu trouver une bibliothèque permettant de faire de la capture de trames. Après quelques recherches, nous avons fini par trouver la librairie Python "PyShark". Celle-ci permet de capturer ainsi que d'analyser en détails chaque paquet, comme le ferait Wireshark. Pour l'instant, nous arrivons bien à capturer les paquets et à en extraire les informations sur les différentes couches.
## Le programme : EasyShark
EasyShark est le programme que nous avons commencé à développer et qui sera toujours dispobible sur ce dépôt Git.
Ce programme codé en Python utilise deux librairies principales qui définnissent les deux enjeux majeurs du programme.
### Les libraires utilisées

#### Pyshark


#### Tkinter

Tout d'abord, afin que le logiciel ne soit pas affreux et qu'il puisse être utilisé par n'importe qui de la manière la plus simple possible, il est important qu'il soit graphique. Pour cela, on utilise la librairie ```tkinter```.
```python
import tkinter as tk
```
Cette librairie va nous permettre de créer très facilement une fenêtre programmable sur laquelle on va pouvoir placé la liste des paquets capturés avec des champs de texte pour des explications ou des détails. On utilise l'alias ```tk``` afin d'avoir une utilisaton plus légère au niveau du code avec la librairie.
On importe ensuite toutes les fonctionnalitées que la librairie de base a afin de ne pas avoir à s'occuper de quelles fonctions on doit importer à chaque fois :
```python
from tkinter import *
```
Enfin, il nous faut importer depuis la sous librairie ```scrolledtext``` l'élément ```ScrolledText``` afin d'avoir une liste déroulante sur laquelle on peut cliquer sur chaque ligne :
```python
from tkinter.scrolledtext import ScrolledText
```
Pour ce qui est de l'aspect graphique, nous avons pour l'instant tout ce qu'il nous faut.
#### Thread
La librairie ```thread``` va nous permettre de pouvoir lancer une fonction en sous processus :
```python
import _thread
```
Elle va donc permettre d'executer en parrallèle la fonction qui va capturer les paquets.
#### Sys
La dernière librairie nécessaire pour l'instant est celle qui permet d'interagir avec le système d'exploitation :
```python
import sys
```
Elle va nous permettre de pouvoir donner des arguments lors de l'execution du programme en ligne de commande :
```bash
$ sudo python3 main.py <interface> <nombre de paquets>
```
Afin de pouvoir capturer sur une interface, un droit root est nécessaire.

### Début du programme
Le début du programme correspond aux commandes qui vont premièrement être exécutées.
#### Prise en compte des arguments

La prise en compte des arguments se fait avec la librairie ```sys```, on utilise l'array ```sys.argv``` qui contient tous les éléments après la commande ```python3``` :
```bash
$ sudo python3 main.py <interface> <nombre de paquets>
```
Comme on peut le voir, le premier argument sera toujours le nom du programme ```main.py``` .
Les deux autres argument sont optionnels car ils définnisent des variables qui ont des valeurs par défaut : 
```python
interf = 'any'
mx = 100
```
La taille de ```sys.argv``` sera toujours au minimum de 1. Si elle est supérieure, c'est que le deuxième argument ```<interface>``` a été donné.
On traite donc le deuxième argument dans ce cas : 
```python
if len(sys.argv) > 1:
	interf = str(sys.argv[1])
```

#### Préparation à la capture

```python
capture = pyshark.LiveCapture(interface=interf)
paquets = list()
```

#### Création de la fenêtre

```python
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
```

### Les fonctions

#### Capture de trames

```python
def captures():
	i = 0
	nombre['text'] = 'En attente de trafic ... PING un peu !'
	fenetre.update_idletasks()
	for packet in capture.sniff_continuously(packet_count=mx):
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
```

#### Clique sur une trame

```python
def clicktrame(evt):
	if len(evt.widget.curselection()) > 0:
		details.delete(1.0,END)
		details.insert(END, '%s' % paquets[int(evt.widget.curselection()[0])])
		fenetre.update_idletasks()
```

#### Récupération de paramètres GET et POST

```python
def arg(packet):
	packet = packet.split('\n')
	packet.pop(0)
	tx = ''
	for i in range(0,len(packet)-1,3):
		tx += packet[i+1][6:]+' : '+packet[i+2][8:]+', '
	return tx[:-2]
```

## Conclusion

### Objectifs remplis

### Problèmes qui devront être résolus

### Améliorations possibles

