# UVSQ : L2 Informatique
## Algorithmique de Graphes - Projet 2020 : Métro, c’est trop
Dos Santos Gabriel - #21807297   
Lin Raphaël - #21802498

## Contenu du fichier .zip
L'archive que vous avez reçu contient les fichiers suivants :
- le fichier README.md que vous êtes en train de lire,
- le rapport du projet "Rapport_DOSSANTOS_LIN.pdf",
- le fichier metro.py qui contient le code source de l'application
- le fichier metro.txt qui contient la liste des stations et des transitions du métro parisien
- le fichier Makefile permettant l'exécution du programme

## Description 
Le but de ce projet est  d'écrire un programme informatique permettant de déterminer le plus court itinéraire pour aller d’une station à une autre dans le métro Parisien. Pour ce faire, nous avons choisi de le programmer en Python. 
L’utilisateur doit saisir une station de départ et une station d'arrivée. L’itinéraire le plus court est alors calculé et son détail s’affiche dans le terminal.

## Utilisation
Le programme s'exécute simplement à l'aide du fichier Makefile en tapant la commande suivante dans le terminal :
```bash
make run
```
Vous pouvez également éxecuter le programme directement avec la commande depuis le dossier 'src':
```bash
python3 src/metro.py
```
Le programme vous demandera de saisir une station de départ et une station d'arrivée. N'hésitez pas à vous référer au fichier de configuration "metro.txt" pour le nom exact des stations (l'orthographe est importante).
