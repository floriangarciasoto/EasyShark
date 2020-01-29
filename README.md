
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
La librairie ```pyshark``` va être au coeur de notre projet. Elle va permettre de simplifier énormement la capture de trame et surtout l'extraction des données sur chaque couche :
```python
import pyshark
```
Cette librairie interragit directement avec Wireshark, il doit donc être installé sur la machine.
Les paquets capturés pourront être décrits de manière textuelle avec un ```string``` qui va décrire tous les layers ou on pourra accéder à des informations plus précises en effectuant des requêtes sur l'objet généré par ```pyshark```.
#### Tkinter

Tout d'abord, afin que le logiciel ne soit pas affreux et qu'il puisse être utilisé par n'importe qui de la manière la plus simple possible, il est important qu'il soit graphique. Pour cela, on utilise la librairie ```tkinter``` :
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
On va donc pouvoir définir simplement l'interface sur laquelle on veut capturer ainsi que le nombre de paquets maximum que l'on veut obtenir (obligatoire) en rentrant deux arguments de plus.
Ces deux autres argument sont optionnels car ils définnisent ces variables qui ont chacune une valeur par défaut : 
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
Si la taille de ```sys.argv``` est cette fois-ci supérieure à 2, c'est que le troisième argument ```<nombre de paquets>``` a été saisi, on le traite donc de la même façon :
```python
if len(sys.argv) > 2:
	mx = int(sys.argv[2])
```
Ces paramètres étant saisis, on peut s'attaquer à la suite du programme.
#### Préparation à la capture
Afin de pouvoir capturer avec ```pyshark```, il est nécessaire d'indiquer une variable afin de pouvoir la parcourir. Cette variable va contenir les paquets un à un capturés.
Comme il s'agit d'une capture en temps réel, on utilise la fonction  ```LiveCapture()``` en précisant l'interface utilisée :
```python
capture = pyshark.LiveCapture(interface=interf)
```
Comme l'on vaut pouvoir accéder à tout moment à n'importe quelle trame puisque l'on pourra cliquer sur une liste déroulante, il faut stocker les trames capturées dans une variable :
```python
paquets = list()
```
Pour se qui est de la préparation de la capture, on a tout ce qu'il nous faut. On peut maintenant passer à la partie graphique.
#### Création de la fenêtre
De la même façon qu'avec ```pyshark```, on précise une variable qui va nous permettre d'interagir avec la fenêtre crée par ```Tkinter``` :
```python
fenetre = tk.Tk()
```
On précise ensuite le nom de la fenêtre :
```python
fenetre.title('EasyShark')
```
On choisi de la nommer EasyShark, le nom accrocheur de notre Wireshark simplifié pour les noobs en réseau !
On va ensuite ajouter un à un les éléments nécessaires. ```Tkinter``` par défaut ajoute les éléments sur la fenêtre de haut en bas de manière centrée, ce qui est très bien visuellement.
On ajoute donc d'abord une phrase indiquant les paramètres choisis par l'utilisateur :
```python
Label(fenetre, text='Capture de %d paquets sur l\'interface %s' % (mx,interf)).pack()
```
L'élément ```Label()``` va permettre de créer du texte directement intégrable dans la fenêtre et la fonction ```pack()``` va permettre de pouvoir directement l'ajouter à la fenêtre.
On ajoute ensuite l'élément ```Listebox()``` qui va permettre d'afficher en tant que liste déroulante les paquets capturés :
```python
liste = Listbox(fenetre, height=20, width=100)
```
On précise la fenêtre que l'on utilise ainsi que les dimensions de la liste, puisqu'il s'agit d'un espace de texte et non juste un texte. La hauteur et la largeur choisies ne sont absolument pas obligatoirement à ces valeurs là.
Le second but de cette liste est de pouvoir intéragir avec l'utilisateur lors d'un clique sur une des lignes. On va donc attribuer l'évenement du clique à la fonction qui s'en chargera :
```python
liste.bind('<<ListboxSelect>>', clicktrame)
```
L'obet ```'<<ListboxSelect>>'``` sera envoyé en tant qu'argument à la fonction ```clicktrame()```.
On ajoute ensuite de la même manière la liste à la fenêtre :
```python
liste.pack()
```
Il est intéressant de pouvoir suivre l'évolution de la capture, en pouvant visualiser en temps réel le nombre de trames capturées.
Pour cela on définit cette fois-ci une variable qui va contenir le ```Label()```, afin de pouvoir le modifier plus tard :
```python
nombre = Label(fenetre, text='Appuies sur le bouton en bas et tu verras.')
```
On l'ajoute ensuite de la même manière à la fenêtre :
```python
nombre.pack()
```

```python
details = ScrolledText(fenetre, height=10, width=100)
```

```python
details.pack()
```

```python
tk.Button(fenetre, text='Capture capture et tu verras', command=caps).pack()
```

```python
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

