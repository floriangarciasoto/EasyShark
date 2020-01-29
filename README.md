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

#### Prise en compte des arguments



#### Création de la fenêtre



### Les fonctions

#### Capture de trames


#### Clique sur une trame


#### Récupération de paramètres GET et POST


## Conclusion

### Objectifs remplis

### Problèmes qui devront être résolus

### Améliorations possibles

