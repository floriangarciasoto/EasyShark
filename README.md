
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
Lors d'un clique sur une trame, il peut être intéressant de voir les détails affreux d'une trame, en affichant sur un champ de texte l'intégralité de la trame sous une chaîne de caractère. Cepandant, vu qu'il s'agit dans tous les cas de beaucoup de texte, il faut utiliser l'élément ```ScrolledText()``` qui va nous permettre d'avoir un champ sur lequel on pourra faire défiler toutes les informations de la trame en détails :
```python
details = ScrolledText(fenetre, height=10, width=100)
details.pack()
```
Le dernier élément que l'on ajoute est le bouton permettant de commencer la capture :
```python
tk.Button(fenetre, text='Capture capture et tu verras', command=caps).pack()
```
Ce bouton permettra de lancer la fonction ```caps()``` qui elle même lancera la fonction ```captures()``` en sous processus.
La dernière commande lancée en début de programme est celle qui va permettre d'afficher la fenêtre en question :
```python
tk.mainloop()
```
Cela va permettre de garder le programme en exécution tant que la fenêtre ne sera pas fermée.
Les commandes que nous avons vu sont donc seulement là pour préparer EasyShark. La capture et la fenêtre sont les seules choses nécessaire pour initialiser le logiciel. Nous allons maintenant voir la partie la plus importante, les fonctions.
### Les fonctions
Les fonctions sont le coeur du programme. Leur rôle va être de modifier la fenêtre en fonction de la capture et des actions effectuées par l'utilisateur.
#### Capture de trames
La fonction ```captures()``` va être le coeur du programme. C'est dans cette fonction que va s'effectuer la capture de trames.
##### Démarrage de la fonction en sous processus
L'utilisateur doit pouvoir effectuer des actions pendant que la capture est en cours. Or, si l'on déclenche la fonction ```captures()``` lors du clique, le programme ne prendra pas en compte ces actions puisqu'il va attendre que la fonction se termine.
Il va donc falloir la faire tourner en arrière plan, en utilisant ```_thread``` :
```python
def caps():
	_thread.start_new_thread(captures,())
```
On précise donc la fonction ```captures()``` sans envoyer d'arguments .
##### Initialisation de la fonction
On va donc bien pouvoir s'interesser à cette dernière. Cette fonction aura pour rôle de remplir la liste de la fenêtre avec les paquets capturés en temps réel. C'est elle qui va remplir la variable ```paquets```, qui va contenir sous forme de tableau l'ensemble des paquets sous forme de texte. Enfin, c'est elle qui va écrire ce qu'il faut sur chaque ligne de la liste, une description brève selon la trame que l'on va devoir définir.
On lance donc la fonction avec un itérateur ```i``` qui va nous permettre de numérotter les trames :
```python
def captures():
	i = 0
```
On avertit l'utilisateur que la capture a commencé en affichant que la capture est en cours :
```python
	nombre['text'] = 'En attente de trafic ... PING un peu !'
```
Cela permet de notifier l'utilisateur que la capture a bien commencée, ça le rassure. On modifie le même attribut ```text``` à l'élément ```Label()``` contenu dans la variable ```nombre```.
On met à jour la fenêtre qui est déjà démarée avec la commande suivante :
```python
	fenetre.update_idletasks()
```
On va donc pouvoir ajouter une ligne à la liste lorsqu'un paquet est capturé comme-ceci :
```python
	for packet in capture.sniff_continuously(packet_count=mx):
```
La variable ```pakcet``` sera la variable temporaire qui contient le paquet en cours de traitement. La fonction ```sniff_continuously()``` va renvoyer un tableau contenant toutes les trames capturées. On précise le nombre maximal de paquets que l'on veut capturer vu précedement.
Pour chaque paquet, on définit son numéro ainsi que la variable ```trame``` qui va contenir le texte qui sera affiché sur la ligne qui sera ajoutée :
```python
	for packet in capture.sniff_continuously(packet_count=mx):
		i += 1
		trame = str(i)+'    '
```
Le numéro de trame est donc la première information affichée pour chaque trame.
##### Obtention des informations sur chaque couches
Il va ensuite falloir vulgariser le plus possible la trame en fonction des couches qu'elle contient.
Pour cela, il va falloir essayer de prendre en compte tous les cas possibles. On part donc de la couche la plus basse et on affiche ce qu'il faut en fonction des types de couches.
Grâce à ```pyshark```, il est très facile de pouvoir accéder à ces informations, car la variable ```packet``` est en fait un objet contenant un ensemble informations sous la forme de ```key``` et ```value```. L'objet en question donne accès à énormément d'informations, mais dans le cas de ce projet, on s'intéresse uniquement aux couches de la trame.
Les couches sont contenus à la racine de l'objet, eux même sous forme d'objet. On peut donc facilement identifier le type de trame en vérifiant si la clé que l'on cherche existe dans l'objet.
Pour vérifier s'il s'agit d'une trame Ethernet :
```python
		if 'eth' in packet:
			trame += 'Ethernet    '
```
On vérifie si la clé ```eth``` existe dans l'objet ```packet```. Si c'est le cas, on ajoute à la chaîne de caractère ```trame``` de quoi s'agit la trame.
Si ce n'est pas le cas, il s'agit alors d'un type de trame que l'on a pas encore définit. Afin de ne pas ignorer des trames, on définit donc une information par défaut pour l'instant :
```python
		else:
			trame += 'Ah ben là C compliqué    '
```
L'utilisateur pourra toujours aller voir de quoi il s'agit dans les détails.
Dans le cas où il s'agit d'une trame de type Ethernet, on va pouvoir vérifier l'identité de la couche au dessus en regardant le type de la couche Ethernet.
Dans le cas de la couche IPv4 :
```python
			if packet.eth.type == '0x00000800':
				trame += 'IPv4    '
```
Dans celui d'IPv6 :
```python
			elif packet.eth.type == '0x000086dd':
				trame += 'IPv6     De %s    à    %s    (imbuvable.com)' % (packet.ipv6.src, packet.ipv6.dst)
```
Ou dans celui d'ARP :
```python
			elif packet.eth.type == '0x00000806':
				trame += 'ARP ma gueule !'
```
Et s'il s'agit d'un Ethernet non définit par nous, on laisse une information par défaut :
```python
			else:
				trame += 'IPBXv4'
```
Dans le cas oùil s'agit d'un paquet IPv4, on peut s'intéresser à la couche applicative située au dessus. On y accède en accèdant au type de protocole de la couche IP.
Dans le cas d'ICMP :
```python
				if packet.ip.proto == '1':
					trame += 'ICMP'
```
On peut donc s'interêsser s'il s'agit d'un PING, chose assez connue du grand public et donc nécessaire à vulgariser.
S'il s'agit d'un envoi PING :
```python
					if packet.icmp.type == '8':
						trame += ' PING'
```
Ou d'une réception PONG :
```python
					if packet.icmp.type == '0':
						trame += ' PONG'
```
On affiche le type d'ICMP. Bien entendu, ICMP ne contient pas que des PING, mais les autres types sont beaucoup moins simples à comprendre pour des non initiés, il est donc pas pour l'instant nécessaire d'en ajouter.
Comme il s'agit d'un paquet IP, on affiche simplement la source et la destination du paquet :
```python
					trame += '    De %s    à    %s' % (packet.ip.src, packet.ip.dst)
```
S'il ne s'agit pas d'une couche ICMP, on vérifie alors s'il s'agit de TCP :
```python
				elif packet.ip.proto == '6':
					trame += 'TCP    '
```
On sait que TCP peut contenir comme couche applicative HTTP. Il s'agit là aussi d'un protocole dont le nom est bien connu du grand pblique, on peut donc l'afficher.
On vérifie pour cela si le port de destination est bien celui utilisé par HTTP en règle générale, soit le port 80 :
```python
					if packet.tcp.dstport == '80':
						trame += 'HTTP    '
```
Cependant il peut s'agir simplement d'une connexion au site, il faut alors d'abord vérifier si c'est le cas en vérifiant la valeur du SYN :
```python
						if packet.tcp.flags_syn == '1':
							trame += 'Connexion au site : %s' % packet.ip.dst
```
Si ce n'est pas le cas, par précaution pour l'instant, on vérifie si la trame contient bien de l'HTTP en vérifiant si la clé ```http``` existe dans ```packet```  :
```python
		elif 'http' in packet:
```
Si c'est le cas, pour l'instant nous traitons seulement le cas où des informations sont envoyées via un formulaire, en vérifiant si la clé ```urlencoded-form``` existe dans ```packet``` :
```python
			if 'urlencoded-form' in packet:
```
Comme il s'agit d'HTTP, les paramètres sont envoyés en clair, il peut donc être intérêssant de vanner celui qui les a envoyés afin que cela parle à l'utilisateur :
```python
				trame += 'Regardes-moi le ce con il passe ses paramètres en clair :  '+arg(str(packet['urlencoded-form']))
```
On utilise la fonction ```arg()``` qui va nous renvoyer les paramètres passés en clair afin de les afficher sur la ligne qui sera ajoutée.
Nous avons donc vu toutes les informations que nous exploitons pour l'instant. Bien évidement, notre but sera d'en ajouter le plus possible, tout en restant dans un cadre simple à comprendre, le but ne sera pas non plus d'inonder l'utilisateur d'informations, ça n'est absolument pas l'interêt.
##### Rendu des informations obtenues
Après avoir formé la chaîne ```trame```, on l'ajoute donc à la liste :
```python
		liste.insert(END, trame)
```
On précise d'abord la position ```END``` afin de placer la ligne à la suite des autres et on précise ensuite le texte ```trame```.
On ajoute ensuite la trame obtenue dans la variable ```paquets``` que nous avons créé :
```python
		paquets.append('Trame %d\n%s' % (i,packet))
```
On précise le numéro de la trame avec l'objet ```packet``` qui sous cette forme sera traité comme une chaîne de caractère. Lorsque l'utilisateur cliquera sur une des lignes, ça sera cette chaîne de caractère qui sera affichée dans le champ ```details```.
On informe l'utilisateur du nombre de trames capturées en modifiant le ```text``` de la variable ```nombre``` :
```python
		nombre['text'] = 'Trames capturées : %d' % i
```
Et on met enfin à jour la fenêtre :
```python
		fenetre.update_idletasks()
```
La capture de trame interagit donc comme il faut avec la fenêtre, en donnant le maximum d'informations sans rentrer dans les détails qui pourraient nous rendre aveugle.
#### Clique sur une trame
La fonction ```clicktrame()``` sera appelée lorsque l'utilisateur va cliquer sur une des lignes de la liste. Son rôle est de remplir le champ ```details``` en sélectionnant le bon ```string``` dans la variable ```paquets``` suivant l'index choisi dans la liste.
Le fait de lier cette fonction au clique sur une trame ne prend en réalité pas seulement en compte le clique, mais plutôt le changement de la sélection dans la liste. Ce qui veut dire que la fonction peut être appelée lorsqu'une trame est sélectionée, mais aussi lorsqu'elle est désélectionnée. Dans ce dernier cas, aucun index n'est renvoyé, ou plutôt la liste des index renvoyée est vide.
Il faut donc d'abord vérifier si la liste des trames sélectionnées est plus grande que 0 :
```python
def clicktrame(evt):
	if len(evt.widget.curselection()) > 0:
```
Si elle est plus grande que 1, les autres index seront ignorés, on e regarde qu'une seule trame à la fois.
Comme le champ ```details``` n'est pas un ```Label()```, il faut d'abord vider son contenu avant d'en ajouter un autre :
```python
		details.delete(1.0,END)
		details.insert(END, '%s' % paquets[int(evt.widget.curselection()[0])])
```
On choisi bien le premier index de la liste renvoyée par ```evt.widget.curselection()```.
Il suffit de mettre ensuite à jour la fenêtre :
```python
		fenetre.update_idletasks()
```
Pour l'instant, la fonction ```clicktrame()``` ne sert qu'a afficher les détails d'une trame.
#### Récupération de paramètres GET et POST
Cette fois-ci, on s'intéresse à un cas très particulier, la récupération des paramètres passés par la méthode GET ou POST en HTTP.
Comme on l'a vu précedement, on récupère uniquement la couche ```urlencoded-form``` qui contient la chaîne de caractère suivante :
```
Layer URLENCODED-FORM:
	Form item: "pseudo" = "jack"
	Key: pseudo
	Value: jack
	Form item: "pass" = "lol"
	Key: pass
	Value: lol
```
Le rôle de la fonction ```arg()``` est de renvoyer une liste des paramètres sous forme de ```string``` à partir de cette chaîne.
Tout d'abord on sépare la chaîne avec comme délimiteur le retour à la ligne afin d'avoir un tableau contenant les lignes que l'on pourra parcourir :
```python
def arg(packet):
	packet = packet.split('\n')
```
On enlève ensuite la première ligne qui correspond à la ligne Layer ```URLENCODED-FORM:``` :
```python
	packet.pop(0)
```
Puis on initialise la chaîne de caractère qui sera renvoyée :
```python
	tx = ''
```
Comme on sait que chaque paramètre est définit sur 3 lignes :
```
	Form item: "pseudo" = "jack"
	Key: pseudo
	Value: jack
```
Il est judicieux de parcourir le tableau avec un pas de 3, afin d'obtetir à chaque pas le ```key``` et le ```value``` :
```python
	for i in range(0,len(packet)-1,3):
```
Pour chaque pas, on récupère le ```key``` sur la deuxième ligne et le ```value``` sur la troisième en ignorant le nombre de caractères suffisant à chaque fois :
```python
		tx += packet[i+1][6:]+' : '+packet[i+2][8:]+', '
```
Comme à chaque fois on rajoute une virgule et un espace, on ne renvoit pas les derniers :
```python
	return tx[:-2]
```
La fonction renvoit donc bien l'ensemble des paramètres sur une seule ligne :
```
pseudo : jack, pass : lol
```
Cette chaîne pourra donc bien être additionnée à une ligne de la liste des trames.
## Conclusion
Le logiciel EasyShark que nous avons développé est encore à un stage de développement, mais il est cependant fonctionnel. Nous pouvons considérer pour l'instant qu'il est au stade de Beta.
### Objectifs remplis
Nous avons réussi à proposer une interface graphique simple d'utilisation sur laquelle des trames s'affichent en temps réel. L'utilisateur peut aisément cliquer sur l'une d'entre elles afin d'en savoir plus sur elle.
Pour ce qui est des bases, les objectifs sont remplis.
### Problèmes qui devront être résolus
Sur certaines interfaces comme celle par défaut peut survenir des bug, ce qui entraîne un plantage du programme et donc un arrêt de la capture et de l'interaction de la fenêtre. Il faudra que nous nous penchions sur la prise en charge des trames de type non Ethernet.
D'après les test que nous avons pu effectuer, aucun autre bug n'est survenu. Nous ne prenons pas en compte les erreurs qui peuvent survenir dues à une mauvaise utilisation du logiciel.

### Améliorations possibles
Pour l'instant, l'utilisateur ne peut voir que du texte, il sera intéressant de pouvoir proposer des animations plus agréables à regarder que les affreux détails des trames.
Bien évidement, il faudra essayer de vulgariser un maximum de trames avec le maximum d'informations que l'on pourra donner sans partir trop loin dans les détails. Il faudra toujours rester dans l'optique que ça soit simple à comprendre.
Il sera aussi intéressant de pouvoir proposer plus d'interaction avec l'utilisateur, en premettant d'arrêter la capture puis de la recommencer. On pourra aussi proposer un menu déroulant pour choisir l'interface et le nombre de paquets, au lieu de l'horrible console pour un utilisateur lambda.
