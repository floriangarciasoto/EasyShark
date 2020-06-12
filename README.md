# EasyShark

Projet de seconde année en R&T

GARCIA Florian<br/>
GUIRADO Adrien<br/>
BANULS Baptiste<br/>
ZHOU Yunhan

*Le texte en italique représente les annotations, elles ne seront plus présentes dans le rapport final.*

## Le projet en soi

*Introduction au projet dans un terme projet universitaire puis travail de groupe.*

### Objectifs demandés

// Consigne du projet ici \\\\

*Reformulation de la consigne avec nos mots.*

*Etablissement d'un cahier des charges en fonction de notre reformulation.*

### Dans quel but

*Explications de à qui et pourquoi, pourquoi est-ce que l'on a choisi ce projet et qu'est-ce qui nous motive à le réaliser.*

### Les solutions auxquelles nous avions pensé

*Explications des langages possibles en fonction des contraintes dues au cahier des charges.*

### La solution retenue

*Explications de pourquoi on a choisi Python ainsi que pourquoi il répond le mieux au cahier des charges.*

## Gestion du projet

*Explications de nos méthodes de travail, les outils que l'on utilise ainsi que la répartition du travail au sein du groupe.*

## Le code

Comme nous l'avons vu précédemment, nous avons décidé pour notre solution de fournir un logiciel codé en Python. Le code en question va se composer de deux parties majeures, l'inclusion des librairies nécessaires à son fonctionnement ainsi que la classe qui va permettre de démarrer l'application.

Le but de cette partie va donc être d'expliquer le programme ```main.py``` dans les moindres détails, en y expliquant et en y justifiant la présence de chaque ligne de code.

Note : il s'agit d'un travail de groupe mis en commun, aucun nom d'un des membres du groupe ne sera cité.

### Libraires utilisées

Python est un langage formidable avec lequel on peut faire énormément de choses. La meilleure d'entre elles est que l'on peut proposer son travail au profit des autres, c'est le but même d'une librairie. D'autres langages en bénéficient aussi, mais Python étant le plus connu, c'est très souvent chez lui que l'on retrouve celle qui sont les plus utiles et surtout les plus facile à utiliser.

S'affranchir de détails techniques quant à la capture de trame ou la gestion d'une interface graphique va nous permettre de nous concentrer sur ce pourquoi cette solution est là : la vulgarisation.

#### Pyshark

L'une des deux librairies les plus importantes, ```pyshark``` comme son nom l'indique assure la liaison entre Python et Wireshark. Ce n'est donc pas Python lui-même qui se charge de la capture, mais il fait appel à un tiers : Tshark. C'est pour cela qu'il est nécessaire d'installer les deux.

Cette librairie va donc nous permettre de récupérer les trames comme Tshark ou WireShark, sauf que cette fois-ci, on en fait ce que l'on veut. Chaque trame est donc récupérée sous la forme d'un objet, ce qui colle avec l'aspect OO de Python.

L'inclusion de pyShark se fait donc comme suit :
```python
import pyshark
```
Nous verrons plus tard en détails comment s'effectue la capture avec.

#### Tkinter

La deuxième plus importante, et la plus connue concernant l'aspect interface graphique en Python. Tkinter se veut avant tout simple d'utilisation, c'est donc pour cette raison que nous l'avons pris. Toutes les fonctionnalités demandées dans le cahier des charges ont pues être remplies grâce à cette dernière, nous verrons par la suite de quelles manières.

L'inclusion de Tkinter se fait en plusieurs étapes selon nos besoins.

Tout d'abord, on inclut Tkinter avec l'alias tk (de façon totalement arbitraire) :
```python
import tkinter as tk
```

Ensuite, on importe tous ses sous éléments :
```python
from tkinter import *
```
Cela va nous permettre d'utiliser ce que l'on appelle les widgets de Tkinter. Il s'agit en fait de tous les éléments qui seront présents sur la fenêtre.

Entre autres, cela va nous permettre :
- l'utilisation des méthodes ```.grid()``` et ```.bind()``` pour le placement des widgets et l'attribution d'événements
- l'ajout du widget ```Label()``` pour afficher du texte sur la fenêtre
- l'ajout du widget ```Button()``` pour mettre des déclencheurs d'événements
- l'ajout du widget ```Listbox()``` pour la liste des trames capturées

Cependant, il ne s'agit que des widgets principaux qui sont importés. Il va donc falloir indiquer à Python que l'on veut aussi obtenir certains éléments de Tkinter.

Pour se faire, on inclut aussi la partie ```ttk``` :
```python
from tkinter import ttk
```
Cela va permettre l'ajout du widget ```Combobox()``` permettant de proposer une liste déroulante pour le choix des interfaces.

Et pour terminer avec Tkinter, on inclut aussi la partie ```ScrolledText``` de la sous partie ```scrolledtext``` :
```python
from tkinter.scrolledtext import ScrolledText
```
Ce qui nous permettra l'ajout du widget ```ScrolledText()``` pour avoir une zone de texte dans laquelle on peut "scroller".

#### Thread

Sur une fenêtre Tkinter, lorsque l'on déclenche une fonction à partir d'un bouton (que nous verrons plus tard dans les détails), la fenêtre va cesser de fonctionner jusqu'à que la fonction soit terminée. On est donc pas du tout sur de l'aspect *Parallel Processing* comme on peut le rencontrer en JavaScript.

C'est donc très problématique lorsque l'on lance la capture, cette dernière qui n'est pas censée en théorie s'arrêter toute seule. La solution que nous avons trouvée pour pallier à ce problème : lancer la fonction de capture en sous processus.

Pour se faire, on inclut donc la librairie ```_thread``` :
```python
import _thread
```
Cette dernière existe aussi sur la deuxième version de Python, mais sur la troisième, on la note bien ```_thread```.

La gestion de sous processus en programmation peut s'avérer très complexe (parfois même dangereuse), Thread est donc là pour simplifier cet aspect-là. Comme nous le verrons par la suite, une seule commande suffira à lancer la capture en arrière-plan.

#### OS

Dans la première version d'EasyShark, le choix de l'interface réseau se faisait par ligne de commande, ce qui peut s'avérer particulièrement traumatisant pour celui ou celle qui n'a jamais ouvert une console. On va donc une fois de plus déléguer la tâche à la machine.

Pour obtenir l'ensemble des interfaces réseaux et savoir ensuite laquelle prendre par défaut, il faut bel et bien passer par cette console. Grâce à la commande UNIX ```ip```, il est possible d'obtenir toutes les informations dont on peut avoir besoin. Il nous faut donc enfin une liaison entre Python et le système d'exploitation.

C'est le rôle de la librairie ```os``` :
```python
import os
```
Cette dernière permet non seulement d'exécuter des commandes bash directement depuis Python, mais aussi d'en obtenir le flux de sortie. Les commandes commençantes par ```ip a``` sont utiles uniquement pour leur retour textuel sur la console, le flux de sortie en question.

Nous verrons donc par la suite comment avec ce flux on peut déterminer les interfaces réseau à choisir pour EasyShark.

### La classe EasyShark

Après l'inclusion du travail des autres, place au nôtre.

EasyShark va donc fonctionner à partir d'une classe Python. De manière générale, il s'agit d'une façon selon laquelle on va créer un objet. Ce dernier va donc pouvoir contenir des attributs qui seront comme des variables, mais uniquement propres à lui.

De cette façon, la classe ```EasyShark()``` va donc renvoyer un objet dans lequel on va pouvoir y stocker tout ce que l'on veut. Elle va être en quelque sorte l'instance de travail de notre application, là où s'opère la création et la modification de variables.

Mais pourquoi faire comme ceci ? Python est un langage orienté objet. Pour faire simple, tout est objet. Que ça soit un entier, une chaîne de caractères, une liste ou bien même une fonction, tous ces éléments sont représentés par des objets. Ces objets possèdent des attributs, ce qui permet de stocker des informations qui restent propres à eux-mêmes. Ce qui est donc intéressant, c'est de pouvoir s'affranchir de variables globales.

Pour ce qui est du contrôle de la capture (que l'on verra plus en détails), il est nécessaire d'utiliser une variable globale à l'instance permettant de savoir si la capture est en cours ou non. Si notre programme était (comme dans la première version) codé sans classe, nous devrions forcément faire appel à une variable globale. Nous verrons par la suite comment finalement est géré ces paramètres globaux à l'instance.

Un autre avantage est que c'est exactement de cette façon que sont codées les librairies en Python. Comme n'importe quelle d'entre elles donc, il serait possible d'importer la classe ```EasyShark()``` pour un autre programme. Cela pourrait aussi permettre de pouvoir lancer plusieurs EasyShark en même temps sans aucun problème de conflits, puisque les variables sont stockées dans des objets séparés. C'est certes inutile mais on se rapproche bien plus de ce qui se fait vraiment en Python pour des projets conséquents.

La déclaration de la classe se fait donc comme ceci :
```python
class EasyShark:
```
Nous allons donc voir plus en détails les éléments qui la compose.

#### Constructeur de la classe

Le constructeur d'une classe est la fonction directement exécutée lors de l'appel de la classe. Il permet de créer l'objet en question ainsi que de lui attribuer éventuellement des attributs. Dans notre cas, il va permettre d'initialiser les variables globales au programme ainsi que la fenêtre.

En Python, cet objet s'appelle avec le mot clé ```self```, et pour lui ajouter un attribut, on lui rajoute ce dernier comme ceci : ```self.attribut = valeur```. C'est donc de cette façon que seront créées puis modifiées toutes les variables nécessaires au fonctionnement du programme.

Mais l'utilité de cet objet ne s'arrête pas là, les méthodes (que nous verrons par la suite) contenues dans la classe EasyShark seront elles-mêmes spécifiées avec l'objet ```self```. Par exemple, la fonction ```capture()``` sera alors une méthode que l'on pourra appeler de la façon suivante : ```self.capture()```.

Soit, lorsque la classe est interprétée, l'objet self contient alors déjà toutes ces méthodes, puisqu'il s'agit de l'objet crée par la classe, et donc la seule façon permettant de s'adresser à la classe, une fois à l'intérieur de celle-ci. Le but du constructeur va être uniquement d'y ajouter des attributs, nos variables d'instance pour le programme.

Le constructeur se définit comme ceci :
```python
	def __init__(self):
```
De la même façon qu'une méthode spéciale en Python, il est entouré par deux tirets du bas.

Cette partie-là va donc en quelque sorte être l'initialisation de notre programme, la partie qui dans la version précédente n'était pas contenue dans une fonction.

##### Prise en compte des interfaces réseaux

Le but premier du programme étant d'être utilisé par des non-initiés au réseau, il doit être normal qu'ils ne doivent pas réfléchir à la façon avec laquelle ils choisissent l'interface réseau sur laquelle capturer, puisqu'ils ne savent sans doute même pas ce que c'est. Cela doit donc être fait de manière automatique.

C'est donc dans cette partie que l'on va faire appel à la librairie ```os```. C'est le système d'exploitation qui va tout nous dire sur les interfaces présentes sur la machine de l'utilisateur. Il s'agit d'une démarche non négligeable de portabilité pour EasyShark, puisque de cette façon, il pourra correctement s'exécuter peu importe les interfaces de l'utilisateur.

Passons donc au code qui va pouvoir remplir ces objectifs.

On commence par définir le tableau qui va contenir les interfaces réseaux :
```python
		self.interfaces = list()
```
Chaque interface sera stockée dans le tableau sous la forme ```[nomSysteme,nomEcran,interfaceActive]``` :
- Le nom système représente le nom de l'interface donné par l'OS, il sera utilisé comme paramètre pour la capture.
- Le nom écran représente celui qui sera présent dans la liste déroulante, c'est celui que l'on doit montrer à l'utilisateur.
- L'interface active permet de savoir si c'est une bonne idée de capturer ou non sur l'interface, on verra plus tard son utilité.

On définit ensuite une liste contenant toutes les simplifications possibles afin d'obtenir à partir des interfaces un nom plus parlant :
```python
		self.simplificationsInterfaces = {
			'Câble' : ['enp','eno','eth'],
			'Wifi' : ['wlp'],
			'Loopback' : ['lo']
		}
```
Chaque élément est sous la forme ```'Type' : [Premières lettres ...]``` :
- Le type comme son nom l'indique est le type d'interface, c'est lui qui sera montré à l'utilisateur sur la liste déroulante.
- Les premières lettres sont un ensemble de chaînes de caractères représentant chacune les premières lettres d'un nom d'interface que l'on peut retrouver sur Linux. La liste n'est bien évidement pas exhaustive.

Grâce à cette variable, il va être possible d'avoir un nom plus parlant pour l'utilisateur comme 'câble' plutôt qu'un nom d'interface système comme ```eno1```.

Il est maintenant temps de remplir la liste des interfaces, avec leurs trois attributs respectifs.

Pour commencer, on va boucler sur toutes les interfaces présentes sur la machine :
```python
		for nomSystemeInterface in os.popen('ip a | grep ^[0-9]*: | cut -d" " -f 2 | sed "s/.$//g"').read().split("\n")[:-1]:
```
On choisit donc un nom temporaire ```nomSystemeInterface``` qui va être égal à chaque fois au nom système de l'interface en cours.

Pour obtenir la liste des interfaces sous la forme qui nous arrange, on va donc utiliser la commande UNIX ```ip a``` :
```shell
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp0s25: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
    link/ether 54:ee:75:5a:ae:a9 brd ff:ff:ff:ff:ff:ff
3: wlp4s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 5c:e0:c5:c3:85:0c brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.105/24 brd 192.168.1.255 scope global dynamic noprefixroute wlp4s0
       valid_lft 79771sec preferred_lft 79771sec
    inet6 fe80::be4:6bab:5b9b:731c/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```
Les lignes contenants les noms des interfaces commencent toujours par un nombre suivit de deux points. Avec une expression régulière :
```shell
$ ip a | grep ^[0-9]*:
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
2: enp0s25: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN group default qlen 1000
3: wlp4s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
```
On sépare ensuite chaque terme par des espaces puis on choisit à chaque fois le deuxième champ qui est celui qui correspond bien au nom de l'interface :
```shell
$ ip a | grep ^[0-9]*: | cut -d" " -f 2
lo:
enp0s25:
wlp4s0:
```
Enfin, comme on aura besoin par la suite des noms des interfaces de façon correcte, on supprime les deux points devants en enlevant le dernier caractère avec aussi une expression régulière :
```shell
$ ip a | grep ^[0-9]*: | cut -d" " -f 2 | sed 's/.$//g'
lo
enp0s25
wlp4s0
```
Grâce à cela, nous avons donc notre liste d'interface séparée chacune par un retour à la ligne. Pour en obtenir une liste exploitable, il manque encore quelques étapes.

Afin d'obtenir ce flux de sortie, on utilise la méthode ```.popen()``` d'```os``` qui prend en argument la commande en question. Cette commande permet de renvoyer un objet contenant toutes les informations sur notre commande, dont son flux de sortie. Pour obtenir ce dernier, on lui applique la méthode ```.read()``` qui va nous le renvoyer sous la forme d'une chaîne de caractère.

Il suffit alors de la séparer correctement avec la méthode ```.split()``` qui va nous la renvoyer sous forme de liste, puis d'ignorer le dernier élément qui correspond au retour chariot avec ```[:-1]```.

Maintenant que l'on a notre liste de nom d'interfaces, on va donc pouvoir remplir notre variable ```self.interfaces```.

Tout d'abord, on attribue un nom d'écran par défaut pour notre interface :
```python
			nomEcran = 'Inconnue ('+nomSystemeInterface+')'
```
On parcourt ensuite les simplifications des interfaces :
```python
			for typeInterface in self.simplificationsInterfaces:
```
Puis chaque premières lettres pour chaque type :
```python
				for premieresLettres in self.simplificationsInterfaces[typeInterface]:
```
Et on vérifie donc si le début du nom de l'interface correspond aux premières lettres en question :
```python
					if nomSystemeInterface[:len(premieresLettres)] == premieresLettres:
```
La chaîne de caractère ```nomSystemeInterface[:len(premieresLettres)]``` correspond à tous les caractères de ```nomSystemeInterface``` jusqu'à un certain nombre ```len(premieresLettres)```. De cette façon, un nom d'interface comme ```eno1``` sera transformé en ```eno```, soit ses trois premières lettres, le nombre de premières lettres correspondant au nombre de lettre de ```eno```, l'une des premières lettres du type 'câble'.

Si c'est le cas, le nom qui sera affiché sera donc le type d'interface :
```python
						nomEcran = typeInterface
```

On va ensuite s'interreser à savoir l'activité de l'interface.

Par défaut, on met qu'elle n'est pas active :
```python
			interfaceActive = False
```
Puis on vérifie si elle l'est de la façon suivante :
```python
			if int(os.popen('ip a s '+nomSystemeInterface+' | head -n 1 | grep "state UP" | wc -l').read()) == 1:
```
On désigne donc cette fois-ci l'interface en cours avec ```ip a s``` :
```shell
$ ip a s wlp4s0
3: wlp4s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 5c:e0:c5:c3:85:0c brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.105/24 brd 192.168.1.255 scope global dynamic noprefixroute wlp4s0
       valid_lft 77411sec preferred_lft 77411sec
    inet6 fe80::be4:6bab:5b9b:731c/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```
L'état de l'interface se trouve toujours sur la première ligne :
```shell
$ ip a s wlp4s0 | head -n 1
3: wlp4s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
```
Si elle contient les termes 'state UP', c'est qu'elle est bien active :
```shell
$ ip a s wlp4s0 | head -n 1 | grep "state UP"
3: wlp4s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
```
Il suffit donc d'en obtenir le nombre de lignes :
```shell
$ ip a s wlp4s0 | head -n 1 | grep "state UP" | wc -l
1
```
Et de vérifier s'il est bien égal à 1, c'est plus simple de comparer des entiers que des chaînes de caractère.

Si c'est le cas, l'interface est donc bien considérée comme active :
```python
				interfaceActive = True
```

En fin de boucle, on ajoute donc les trois informations importantes pour la suite de chaque interface à la liste des interfaces :
```python
			self.interfaces.append([nomSystemeInterface,nomEcran,interfaceActive])
```

Il est temps de choisir maintenant laquelle va être présentée en première à l'utilisateur, le but étant toujours de lui simplifier la vie.

On définit donc l'index de l'interface sur laquelle sera efféctuée la capture. Cet index sera utilisé sur la liste des interfaces, l'index 0 correspondant à la première, le 1 à la deuxième ...
On choisit donc comme valeur par défaut l'index de la première interface soit 0 :
```python
		self.indexInterfaceCaptureEnCours = 0
```

On parcourt ensuite notre liste d'interface de façon à avoir l'index pour chaque itération :
```python
		for i in range(len(self.interfaces)):
```
Donc pour chaque interface, si elle est active :
```python
			if self.interfaces[i][2] == True:
```
Dans ce cas l'index sera celui de l'interface en cours :
```python
				self.indexInterfaceCaptureEnCours = i
```

Pour en finir avec l'initialisation des interfaces, on va devoir créer le tableau contenant le nom d'écran de chacune d'entre elles.

Pour se faire on crée la liste temporaire qui va les contenir :
```python
		listeInterfacesValeurs = list()
```
Puis pour chaque interface :
```python
		for i in self.interfaces:
```
On y ajoute son nom d'écran :
```python
			listeInterfacesValeurs.append(i[1])
```
Cette liste sera utile lors de la création de la liste déroulante permettant de choisir l'interface de capture.

##### Initialisation des variables utiles à la capture

Après les interfaces, la capture elle-même. Peu de paramètres seront nécessaires cette fois-ci.

Tout d'abord, on va définir le tableau qui va contenir les trames capturées :
```python
		self.trames = list()
```
Chaque trame sera stockée dans le tableau sous la forme ```[explicationsTrame,detailsTrame]``` :
- L'explicaiton de la trame sera sous la forme d'une chaîne de caractère représentant le texte vulgarisant la trame.
- Les détails de la trame seront sous la forme d'une chaîne de caractère représentant les différentes couches de la trame avec leurs paramètres.
Nous verrons ces deux aspects dans les détails par la suite.

On définit ensuite le booléen qui va nous permettre de savoir si la capture est en cours ou non :
```python
		self.captureEnCours = False
```
La capture n'étant pas lancée au début, on le définit sur ```False```.

Enfin, on définit le numéro de la dernière trame :
```python
		self.numeroDerniereTrame = 0
```
Il est défini sur 0 par défaut et est incrémenté à chaque trame capturée. Il permettra donc d'attribuer pour chaque ligne dans la liste des trames capturées un numéro, tout comme sur WireShark. Il s'agit donc de notre compteur de trames.

##### Création de la fenêtre

Après avoir initialisé les variables nécessaires au fonctionnement d'EasyShark, voyons maintenant la création de la fenêtre de ce dernier. C'est donc dans cette partie que vont être utilisés tous les éléments importés depuis Tkinter.

Tout d'abord, on crée la variable qui va contenir notre fenêtre :
```python
		self.fenetre = tk.Tk()
```
C'est sur elle que l'on va appliquer les ajouts de tous les éléments nécessaires à l'interface graphique d'EasyShark.

On définit donc le titre de la fenêtre :
```python
		self.fenetre.title('EasyShark')
```

Puis on y ajoute les éléments un par un avec la méthode ```.grid()```. Cette dernière va nous permettre de placer les widgets, soit les éléments de la fenêtre, comme sur une grille. De cette façon, les éléments seront ordonnés sur la fenêtre, contrairement à la méthode ```.pack()``` anciennement utilisée qui consistait simplement a rajouter les éléments à la ligne de façon centrée.

La méthode ```.grid()``` prend en paramètre la façon dont on souhaite placer le widget :
- le numéro de ligne sur la grille représenté par l'argument ```row```
- le numéro de colonne sur la grille représenté par l'argument ```column```
- le nombre de lignes que prend le widget sur la grille représenté par l'argument ```rowspan```
- le nombre de colonnes que prend le widget sur la grille représenté par l'argument ```columnspan```
- l'emplacement relatif du widget dans sa case représenté par l'argument ```sticky```, par défaut au centre

La grille qui sera formée par l'ajout successif de widget pour notre interface sera très simple, seulement 2 colonnes pour 7 lignes. Un élément sera donc placé à gauche avec l'argument ```row=0```, à droite avec ```row=1``` ou au centre avec ```row=0``` et ```columnspan=2``` afin qu'il prenne la place des deux colonnes. Le numéro de ligne sera quant à lui seulement incrémenté au fur et à mesure qu'une ligne est remplie.

Voyons donc le placement de nos widgets.

On ajoute d'abord par ajouter le texte qui sera situé à gauche de la liste déroulante :
```python
		Label(self.fenetre, text='Commences pas choisir l\'interface : ').grid(row=0, column=0, sticky=E)
```
Afin qu'il soit collé à la liste, il faut que son emplacement relatif aille vers cette dernière qui sera située à gauche. Pour cela, on le définit à l'Est, d'où l'argument ```sticky=E```.

On crée ensuite la fameuse liste déroulante des interfaces réseau à l'aide du widget ```Combobox()``` :
```python
		self.listeInterfaces = ttk.Combobox(self.fenetre, values=listeInterfacesValeurs)
```
Elle prend donc en compte avec l'argument ```values=listeInterfacesValeurs``` la liste des noms d'écran des interfaces définie précédemment.

On définit ensuite la première position sur laquelle elle sera en utilisant l'index de l'interface de capture vu précédemment :
```python
		self.listeInterfaces.current(self.indexInterfaceCaptureEnCours)
```

Puis on ajoute enfin la liste à la fenêtre, cette fois-ci vers l'Ouest pour être collée au texte :
```python
		self.listeInterfaces.grid(row=0, column=1, columnspan=2, sticky=W)
```

On attribut ensuite l'évènement qui se produit lors du changement de sa position ```'<<ComboboxSelected>>'``` avec la fonction ```changerInterface()``` :
```python
		self.listeInterfaces.bind('<<ComboboxSelected>>', self.changerInterface)
```
Lors d'un changement effectué sur la liste, l'objet ```ComboboxSelected``` sera envoyé à la fonction ```changerInterface()``` en tant que premier argument. On verra plus tard cela dans les détails.

On crée ensuite le bouton permettant de commencer et stopper la capture :
```python
		self.boutonCommencerStopper = tk.Button(self.fenetre, text='Capturer', command=self.commencerStopperCapture)
```
Son appuie sera donc attribué à la fonction qui se charge de cela avec l'argument ```command=self.commencerStopperCapture```.

Puis on l'ajoute à la fenêtre :
```python
		self.boutonCommencerStopper.grid(row=1,column=0, sticky=E)
```
Son ajout est fait en deux étapes afin d'avoir le bouton contenu dans la variable ```self.boutonCommencerStopper```, cela permettra de changer le texte du bouton en fonction de l'état de la capture.

On ajoute ensuite directement le bouton permettant de réinitialiser la capture :
```python
		tk.Button(self.fenetre, text='Réiniatiliser', command=self.reinitialiserCapture).grid(row=1, column=1, sticky=W)
```
Son appuie sera donc attribué à la fonction qui se charge de cela avec l'argument ```command=self.reinitialiserCapture```.

Les deux boutons sont aussi collés de la même façon.

On arrive donc à la liste des trames.

On ajoute d'abord un texte informatif au-dessus :
```python
		Label(self.fenetre, text='Liste des trames :').grid(row=2, columnspan=2)
```

Ensuite on crée la liste des trames à l'aide du widget ```Listbox()``` :
```python
		self.listeTrames = Listbox(self.fenetre, height=20, width=100)
```
Celle-ci n'est pas comme celle vue précédemment, elle est de la même forme que celle que l'on peut retrouver sur WireShark. Les dimensions définies sont totalement arbitraires.

On l'ajoute ensuite à la fenêtre :
```python
		self.listeTrames.grid(row=3, columnspan=2)
```
De la même façon, cela nous permettra de la contrôler avec la variable ```self.listeTrames```.

Tout comme la liste déroulante des interfaces, on attribut son changement de sélection ```'<<ListboxSelect>>'``` à la fonction ```clickSurTrame()``` :
```python
		self.listeTrames.bind('<<ListboxSelect>>', self.clickSurTrame)
```

On crée ensuite le texte en bas de cette liste qui va nous informer sur le nombre de trames capturées :
```python
		self.nombreTrames = Label(self.fenetre, text='Faut appuyer sur Capturer en fait')
```
On y met comme texte par défaut une suggestion pour commencer la capture.

On l'ajoute ensuite à la fenêtre :
```python
		self.nombreTrames.grid(row=4, columnspan=2)
```
Toujours en deux étapes, afin de pouvoir le contrôler par la suite.

On passe enfin aux deux champs de texte correspondants aux deux types d'informations pour chaque trame. C'est sur eux que l'on va pouvoir scroller.

Pour le texte des explications.

On ajoute d'abord le texte au-dessus pour signifier l'utilité de ce champ :
```python
		Label(self.fenetre, text='J\'t\'explique : ').grid(row=5, column=0)
```

Puis on crée le champ en question à l'aide du widget ```ScrolledText()``` :
```python
		self.champExplicationsTrame = ScrolledText(self.fenetre, height=10, width=50)
```
La hauteur définie est totalement arbitraire, la largeur cependant correspond à la moitié de celle de la liste des trames.

On l'ajoute ensuite à la fenêtre :
```python
		self.champExplicationsTrame.grid(row=6, column=0)
```

Pour le texte des détails.

De la même façon, on ajoute le texte :
```python
		Label(self.fenetre, text='Détails imbuvables, regardes pas si t\'es une âme sensible :').grid(row=5, column=1)
```

Puis le champ de texte :
```python
		self.detailsTrame = ScrolledText(self.fenetre, height=10, width=50)
```

Que l'on ajoute à la fenêtre :
```python
		self.detailsTrame.grid(row=6, column=1)
```

Tous les éléments de la fenêtre sont ainsi placés, il ne reste plus qu'a invoquer cette dernière.

Pour cela, on utilise la méthode ```.mainloop()``` sur la variable ```self.fenetre``` :
```python
		self.fenetre.mainloop()
```
Cela va faire apparaître la fenêtre avec tous les éléments placés au préalable. La fenêtre restera ouverte tant qu'on ne l'a pas fermée avec la croix, d'où la boucle ```mainloop()```.

#### Méthodes associées à la classe

Dans une classe en Python, après le constructeur il y a les méthodes. Elles ont exactement la même syntaxe de que simples fonctions, mais avec une particularité : elles prennent en compte un objet qu'elles renvoient automatiquement. Dans notre cas, il s'agit exactement du même objet qu'utilisé précédemment, puisque l'on traite toujours avec le même objet.

Une méthode va donc toujours prendre en premier argument l'objet ```self```, afin de le retourner en fin de fonction. Il va être donc très simple de modifier ses attributs afin de modifier les variables d'instance ainsi que les éléments sur la fenêtre.

L'intérêt de faire des fonctions comme celles-ci va permettre de prendre en compte les actions effectués par l'utilisateur. Comme nous avons pu le voir précédemment, des fonctions ont été attribuées au click de l'utilisateur sur différents widgets de la fenêtre.

Voyons donc ces méthodes en question.

##### Contrôle de la capture

Le contrôle de la capture correspond à la prise en compte du bouton permettant de démarrer et stopper la capture. Elle aura donc deux fonctionnements possibles, si la capture est en cours ou non.

La méthode se définie donc comme ceci :
```python
	def commencerStopperCapture(self):
```
On prend toujours en compte l'argument ```self```.

On vérifie donc si la capture est en cours ou non. Si ce n'est pas le cas :
```python
		if self.captureEnCours == False:
```
On signifie donc que c'est le cas :
```python
			self.captureEnCours = True
```
On change le texte sur le bouton cliqué afin d'y avoir un texte plus pertinent :
```python
			self.boutonCommencerStopper['text'] = 'Stopper'
```
Puis l'on démarre la capture en sous processus :
```python
			_thread.start_new_thread(self.capture,())
```
C'est donc le seul endroit où l'on fait appel à la librairie ```_thread```. On utilise la méthode ```.start_new_thread()``` qui prend comme argument :
- la fonction que l'on veut démarrer en sous processus, dans notre cas ```capture()```
- les arguments envoyés à cette fonction, dans notre cas on en envoi aucun : ```()```

Si en revanche la capture est en cours, on signifie que ce n'est plus le cas :
```python
			self.captureEnCours = False
```
On verra plus tard que cela permet d'arrêter proprement la capture.

On change le texte du bouton dans le même but :
```python
			self.boutonCommencerStopper['text'] = 'Reprendre'
```
Puis on rajoute un texte au nombre de trames capturées afin d'informer l'utilisateur que ça ne risque pas de changer si la capture est stoppée :
```python
			self.nombreTrames['text'] += ' (capture stoppée)'
```

Mis à part le démarrage de la capture, cela reste une fonction très simple.

##### Contrôle de l'interface réseau utilisée

Cette fonction va prendre en compte l'interface sélectionnée à l'aide de la liste déroulante. Nous allons donc voir comment se comporte une méthode qui prend en compte un événement.

La déclaration de la méthode cette fois-ci se fait comme ceci :
```python
	def changerInterface(self, event):
```
L'argument ```self``` est et sera toujours en premier. On a ensuite l'argument ```event```, c'est avec cette variable locale à la fonction que l'on va pouvoir se servir de l'objet ```'<<ComboboxSelected>>'``` renvoyé par la liste.

Cependant, il ne sera pas nécessaire d'utiliser directement l'objet ```event```. On peut directement interroger le widget sur la position à laquelle il se trouve :
```python
		self.indexInterfaceCaptureEnCours = self.listeInterfaces.current()
```
Cela n'est pas toujours possible, nous le verrons par la suite. La méthode ```.current()``` permet donc de renvoyer l'index de la sélection, comme il s'agit du même index qu'utilisé pour accéder à la même interface dans notre liste, on affecte donc directement l'index de l'interface de capture avec cette valeur.

##### La capture

On arrive donc au cœur du programme. C'est donc cette méthode qui va fonctionner en sous processus. Son rôle va être donc de remplir la liste des trames, que ça soit la nôtre ou celle de la fenêtre.

Nous allons donc y retrouver trois types d'informations pour chaque trame :
- les détails de la trame : ils seront directement récupérés à l'aide de pyshark, ce sont ces mêmes détails que l'on peut retrouver sur WireShark et qui vont nous permettre de créer les deux autres types d'informations
- le texte sur la ligne de la trame dans la liste de la fenêtre : il s'agit en quelque sorte du titre de la trame, il commencera toujours par le numéro de trame et nous verrons par la suite comment le compléter au maximum afin de différencier au plus possibles toutes les trames capturées.
- le texte explicatif de la trame : c'est là qu'intervient notre travail de vulgarisation, le rôle du texte explicatif sera comme son nom l'indique d'expliquer la trame sélectionnée avec des mots simples, c'est ça qui va permettre aux non-initiés de comprendre le trafic réseau qu'ils sont entrain de capturer

Pour résumé, nous avons trois types d'informations pour chaque trame qui vont chacune se placer au bon endroit de la fenêtre :

| Type d'information       | Emplacement dans la fenêtre                               |
| ------------------------ | --------------------------------------------------------- |
| Détails de la trame      | Champ de texte ```champExplicationsTrame```               |
| Ligne de la trame        | Ligne sur la liste des trames capturées ```listeTrames``` |
| Explications de la trame | Champ de texte ```detailsTrame```                         |

Voyons donc comment la fonction s'occupe de traiter ces informations.

De la même façon que pour les précédentes, on définit la méthode :
```python
	def capture(self):
```

Celle-ci étant plus conséquente, elle est divisée en plusieurs parties.

###### Initialisation de la capture

Avant de démarrer la boucle qui va concerner la capture de trames, on informe l'utilisateur que cette dernière va commencer.

On met donc à jour le texte en bas de liste :
```python
		self.nombreTrames['text'] = 'En attente de trafic ... PING un peu !'
```
Puis on met à jour la fenêtre :
```python
		self.fenetre.update_idletasks()
```
En effet, avec Tkinter, il n'est pas nécessaire de faire appel à la méthode ```.update_idletasks()```, puisque la mise à jour se fait de manière automatique en fin de fonction. Mais là est donc le problème, nous ne sommes pas en fin de fonction. Lors d'un faible trafic réseau, les trames peuvent mettre plusieurs secondes à arriver. Il faut donc pendant ce temps en informer l'utilisateur, au lieu de mettre un inutile '0 trames capturées'.

Une fois cela fait, il est temps de démarrer la boucle.

###### Boucle sur chaque trame

La capture va donc commencer ici. Il s'agit du seul endroit où l'on fait appel à la librairie ```pyshark```.

La boucle va donc fonctionner de la manière suivante :
```python
		for trame in pyshark.LiveCapture(interface=self.interfaces[self.indexInterfaceCaptureEnCours][0]).sniff_continuously(packet_count=10000):
```
Pour chaque itération, la variable ```trame``` va prendre comme valeur l'objet contenant tous les détails de la trame renvoyés par ```pyshark```.

En utilisant la méthode ```.LiveCapture()``` de ```pyshark```, nous allons pouvoir initialiser une capture sur l'interface de capture en cours que nous avons considéré en spécifiant l'argument ```interface=self.interfaces[self.indexInterfaceCaptureEnCours][0]```.

Nous utilisons l'index de l'interface de capture ```indexInterfaceCaptureEnCours``` pour piocher la bonne interface dans notre liste ```interfaces```, puis on prend la première valeur ```[0]``` afin d'avoir le nom système de l'interface. Bien évidemment, ce que demande ```pyshark``` comme interface, c'est bien le nom système.

En appliquant ensuite la méthode ```.sniff_continuously()```, nous permettons à la capture de démarrer. Par convention, pyshark demande un nombre maximal de trames capturées avec l'argument ```packet_count```, puisqu'il s'agit d'une boucle for dans laquelle est effectuée la capture, soit une boucle avec un début et une fin tous deux biens déterminés. Nous choisissons donc un grand nombre afin d'être tranquille.

Pour ce qui est de l'intérieur de la boucle donc.

Tout d'abord, nous vérifions si tout ce qui va être fait par la suite ne sera pas fait pour rien. On vérifie donc si la capture est bien censée être en cours :
```python
			if self.captureEnCours == False:
```
Si ce n'est pas le cas, on utilise la commande ```break``` permettant de mettre fin à la boucle ```for```. Nous verrons plus tard comment se comporte la fonction face à un arrêt de la capture après la boucle. Mettre une condition en début de boucle permet d'arrêter cette dernière même si elle a déjà démarré.

Si la capture est donc bien censée se faire, il se passe alors beaucoup de choses pour chaque itération.

Tout d'abord, on incrémente le compteur de trames :
```python
			self.numeroDerniereTrame += 1
```
Puis on l'utilise afin de commencer à remplir la chaîne de caractères ```ligneTrame``` qui sera utilisée pour la ligne de la trame dans la liste de la fenêtre :
```python
			ligneTrame = str(self.numeroDerniereTrame)+'    Sur : '+self.interfaces[self.indexInterfaceCaptureEnCours][1]+'    '
```
On spécifie en plus l'interface sur laquelle a été capturée la trame, en utilisant cette fois-ci le deuxième type d'information ```[1]``` que l'on possède sur l'interface.

On spécifie ensuite une explication par défaut pour la trame :
```python
			explicationsTrame = 'Ouais en fait non.'
```
Elle sera affichée dans le cas où la trame possède des informations qui ne se retrouvent pas dans les explications que nous avons établies.

###### Obtention des informations et établissement des explications

*Explications du remplissage de la ligne de la trame ainsi que ses explications. Toutes les lignes de code ne seront cette fois-ci pas expliquées, le but est simplement de comprendre le principe utilisé pour former ces deux informations.*

###### Application des informations obtenues

Après avoir correctement former les chaînes de caractères ```ligneTrame``` et ```explicationsTrame```, il est temps de les sauvegarder.

Pour ce qui est de la ligne de la trame, on l'insère tout simplement dans la liste :
```python
			self.listeTrames.insert(END, ligneTrame)
```
En utilisant la méthode ```.insert()``` sur celle-ci, on définit l'emplacement de la ligne, soit à la fin avec le mot clé ```END```, puis on spécifie notre variable ```ligneTrame```.

Pour ce qui est des deux autres informations, on les ajoute à notre liste de trames de la façon suivante :
```python
			self.trames.append([explicationsTrame,'Trame %d\n%s' % (self.numeroDerniereTrame,trame)])
```
Les explications de la trame étant déjà une chaîne de caractères, on l'ajoute comme telle. Pour ce qui est des détails, on les ajoute précédés du numéro de trame avec un retour à la ligne. La conversion avec le format de variable ```%s``` va permettre de convertir l'objet entier en chaîne de caractère, afin de pouvoir l'inscrire correctement dans le champ de texte en question.

Etant en fin de boucle, on peut afficher le nombre de trames capturées en mettant à jour le texte du bas :
```python
			self.nombreTrames['text'] = 'Trames capturées : %d' % self.numeroDerniereTrame
```
Puis en mettant à jour la fenêtre :
```python
			self.fenetre.update_idletasks()
```
La boucle n'étant jamais finie (en théorie), cela est nécessaire pour une mise à jour de la fenêtre en temps réel.

##### Réinitialisation de la capture

La réinitialisation de la capture va permettre une remise à zéro sur la liste des trames capturées, la nôtre ainsi que celle de la fenêtre. La capture ne sera cependant pas arrêtée, ce n'est pas à elle de le faire, et l'interface choisie ne changera pas. Ce rôle reste attribué à la liste déroulante et au bouton de contrôle de capture.

La définition de la méthode se fait comme les autres :
```python
	def reinitialiserCapture(self):
```

Tout d'abord, on vide la liste des trames de la fenêtre :
```python
		self.listeTrames.delete(0,len(self.trames)-1)
```
En utilisant la méthode ```.delete()``` sur celle-ci, on spécifie quelles lignes on veut supprimer de la liste, en précisant l'index de début et de fin 0 et ```END```, tous deux inclus.

On réinitialise ensuite le compteur de trames :
```python
		self.numeroDerniereTrame = 0
```
On vide notre liste de trames :
```python
		self.trames = list()
```
Puis on efface le champ des explications :
```python
		self.champExplicationsTrame.delete(1.0,END)
```
Ainsi que celui des détails :
```python
		self.detailsTrame.delete(1.0,END)
```
Le texte en bas renseigne l'utilisateur sur le fait que l'on compte à nouveau capturer :
```python
		self.nombreTrames['text'] = 'En attente de trafic à nouveau ...'
```
Et si la capture a en fait été arrêtée avant la réinitialisation :
```python
		if self.captureEnCours == False:
```
Dans ce cas on signifie à l'utilisateur qu'il faudrait reprendre la capture pour que ça bouge à nouveau :
```python
			self.nombreTrames['text'] += ' (faut appuyer sur Reprendre en fait)'
```

Ainsi, la réinitialisation a permis de vider les variables et les widgets sur lesquels on sauvegarde nos données au fur et à mesure.

##### Lors d'un clic sur une trame

Tout comme dans WireShark, il faut bien évidement que l'utilisateur puisse cliquer sur une trame dans la liste afin d'en savoir plus sur cette dernière. C'est donc le rôle de la méthode suivante.

Elle se définit de la même façon que pour la liste déroulante des interfaces :
```python
	def clickSurTrame(self, event):
```

De la même façon qu'avec le widget ```Combobox()```, l'argument ```event``` ne sera pas utilisé, on fera directement appel à la liste elle-même.

Sur une liste comme celle-ci, il est tout à fait possible de sélectionner plusieurs lignes. La sélection renvoyée par le widget ```Listbox()``` n'est donc pas un index, mais un tableau. Si l'on click hors de la liste sur la fenêtre, un événement va tout de même se produire, et le tableau renvoyé sera vide.

Il faut donc s'assurer d'abord si ce n'est pas le cas :
```python
		if len(self.listeTrames.curselection()) > 0:
```
Lorsque l'on applique la méthode ```.curselection()``` à notre widget, on obtient ce tableau. Seulement, vu qu'il n'y a qu'un seul champ pour les explications, et de même pour les détails, il est inutile de se préoccuper des autres sélections. On choisira donc toujours le premier index avec ```[0]```.

On récupère donc cet index avec une variable locale :
```python
			indexSelection = self.listeTrames.curselection()[0]
```

Afin d'y remplacer le contenu, on vide le champ des détails :
```python
			self.detailsTrame.delete(1.0,END)
```
En utilisant la méthode ```.delete()``` sur ce dernier, on précise que l'on souhaite supprimer tous les caractères qu'il contient avec les bornes ```1.0``` et ```END``` incluses. Il n'est pas possible d'utiliser l'index 0 pour désigner le début.

Après avoir vider le champ, on y insère notre texte :
```python
			self.detailsTrame.insert(END, '%s' % self.trames[indexSelection][1])
```
Il est obligatoire de spécifier une position ainsi que du texte formaté. Vu qu'il n'y a plus rien, on peut se permettre d'ajouter le texte à la fin. Ce dernier est bien évidement formaté avec le format ```%s``` qui correspond aux chaînes de caractères.

Pour obtenir le bon texte, on utilise donc l'index de sélection ```indexSelection``` pour correctement piocher notre trame. On choisit donc la deuxième information ```[1]``` sur la trame afin d'avoir les détails de la trame.

On procède donc exactement de la même façon pour les explications de la trame.

On vide le champ :
```python
			self.champExplicationsTrame.delete(1.0,END)
```
Puis on y met notre texte :
```python
			self.champExplicationsTrame.insert(END, '%s' % self.trames[indexSelection][0])
```

Cette fois-ci, pas besoin d'ordonner la mise à jour de la fenêtre, puisque cela se fera automatiquement en fin de fonction.

L'utilisateur est donc bel et bien en mesure d'obtenir les informations de la trame sur laquelle il a cliqué.

#### Démarrage de l'application

Notre application étant démarrée à partir d'une classe, il est judicieux de la démarrer correctement en vérifiant l'instance d'exécution du programme.

Pour se faire, on utilise la variable système ```__name__``` qui va nous renseigner sur l'état d'exécution du programme :
```python
if __name__ == '__main__':
	EasyShark()
```
Lorsqu'il est démarré directement, la variable ```__name__``` prend la valeur ```'__main__'```. Si ce n'est pas le cas, alors on ne préfère pas lancer la classe, puisque le programme aura surement été importé.

Cette logique d'importation est très importante lorsque l'on code une classe Python. Le programme qui importera notre classe va peut-être traiter avec plusieurs objets, et surtout uniquement à un certain instant. C'est donc pour cela que l'on utilise cette condition, cela permet de ne pas démarrer la classe à l'importation du programme.

## Fonctionnement

*Explications dans les détails de son fonctionnement, que ça soit en termes de ressources nécessaires, d'utilisation ainsi que des résultats observables à l'écran.*

### Prérequis

*Explication de l'OS nécessaire (Linux) ainsi que toute l'installation qui doit y être présente.*

### Utilisation

*Explication de l'ergonomie apportée avec l'interface graphique, on pourra aussi parler des éventuelles erreurs qui peuvent être causées par une mauvaise utilisation que l'on n'a pas réussi à résoudre.*

### Résultats

*Démonstration d'en quoi les résultats répondent en partie au cahier des charges, que ça soit en termes de simplicité d'utilisation ainsi qu'en informations faciles à comprendre pour l'utilisateur lambda.*

## Conclusion

### Objectifs remplis

*Résumé des objectifs ainsi que la manière dont ils ont été remplis.*

### Ce qu'a pu nous apporter ce projet

*Explications des connaissances ainsi que des méthodes de travail acquises grâce à ce projet.*

### Éventuelles améliorations

*Ouverture sur les améliorations qui pourraient être apportées lors d'une éventuelle poursuite du projet, notamment l'aspect graphique du logiciel avec des couleurs, des animations, etc ...*

## Sources

### Documentation

Librairie pyShark :<br/>
https://github.com/KimiNewt/pyshark

Librairie Tkinter :<br/>
https://docs.python.org/fr/3/library/tkinter.html

Librairie thread pour Python 3 :<br/>
https://docs.python.org/3/library/_thread.html

Utilisation de ListBox pour Tkinter :<br/>
http://tkinter.fdex.eu/doc/lbw.html

Utilisation de Grid pour Tkinter :<br/>
https://effbot.org/tkinterbook/grid.html

Utilisation de ScrolledText pour Tkinter :<br/>
https://docs.python.org/fr/3/library/tkinter.scrolledtext.html

### Forums

OpenClassroom - utilisation des classes en Python :<br/>
https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/232721-apprehendez-les-classes

OpenClassroom - utilisation de Tkinter avec une classe :<br/>
https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/234859-creez-des-interfaces-graphiques-avec-tkinter

Retour d'une commande Linux :<br/>
https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on

Configuration WireShark :<br/>
https://osqa-ask.wireshark.org/questions/7976/wireshark-setup-linux-for-nonroot-user
