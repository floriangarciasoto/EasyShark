Dans cette partie, nous allons détailler en quoi EasyShark répond aux critères décrits en début de rapport.

### Prérequis

Comme nous avons pu le voir lors de l'explication des librairies, une certaint installation est nécessaire au fonctionnement d'EasyShark, ce qui n'en fait donc pas du tout un programme portable. En réalité, il ne peut fonctionner que sur les systèmes d'exploitation permettant d'exécuter la version 3 de Python, mais nous allons considérer qu'il ne marche que sur Linux.

Il faut d'abord installer la version 3 de Python :
```
sudo apt install python
```
La 3e version de Python devrait être automatiquement selectionnée.

Il faut ensuite installer Wireshark :
```

```
Puis Tshark :





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




### Utilisation

*Explication de l'ergonomie apportée avec l'interface graphique, on pourra aussi parler des éventuelles erreurs qui peuvent être causées par une mauvaise utilisation que l'on n'a pas réussi à résoudre.*

### Résultats

*Démonstration d'en quoi les résultats répondent en partie au cahier des charges, que ça soit en termes de simplicité d'utilisation ainsi qu'en informations faciles à comprendre pour l'utilisateur lambda.*