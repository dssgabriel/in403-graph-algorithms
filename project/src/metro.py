import os
import sys
import math

#*****************#
#***** CLASS *****#
#*****************#

class MetroParisien:
# ATTRIBUTS
	# Liste des stations
	stations = []
	# Liste des transitions
	transitions = []


# CONSTRUCTEUR
	# Initialisation d'une instance de MetroParisien
	def __init__(self, filename):
		cfg = open(filename, 'r')

		# Lecture du fichier de configuration
		while (True):
			line = cfg.readline()
			line = line.rstrip()

			# Si on lit une station,
			# la découper en une liste (n° de la station, ligne, type et nom)
			# et ajouter celle-ci à la liste des stations
			if (line.startswith('V')):
				vertex = line
				vertex = vertex.strip("V ")
				vertex = vertex.split(' ', 3)
				self.stations.append(vertex)
				continue

			# Si on lit une transition,
			# la découper en une liste (n° de la station de départ, n° de celle d'arrivée, temps de trajet)
			# et ajouter celle-ci à la liste des transitionss
			if (line.startswith('E')):
				edge = line
				edge = edge.strip("E ")
				edge = edge.split(' ', 2)
				self.transitions.append(edge)
				continue

			# Si on lit une ligne vide, on arrête la boucle while ()
			if not line:
				cfg.close()
				break

		# Convertir le n° de la station en entier
		for i in range(len(self.stations)):
			self.stations[i][0] = int(self.stations[i][0])

		#Convertir toute la liste de transitions en entiers
		for i in range(len(self.transitions)):
			self.transitions[i][0] = int(self.transitions[i][0])
			self.transitions[i][1] = int(self.transitions[i][1])
			self.transitions[i][2] = int(self.transitions[i][2])


# METHODES
	# Déterminer la station dans la liste des sommets non vus du graphe 
	# avec la plus courte distance avec la station de départ
	def minDistance(self, distance, visited, unvisited):
        # Initialiser la distance minimum à l'infini et l'indice à -1
		minDist = math.inf
		minIndex = -1

		# Lire la distance de chaque sommet de la liste des sommets non vus
		# et garder en mémoire l'indice du sommet avec la distance minimale
		for i in unvisited:
			if (distance[i] < minDist):
				minDist = distance[i]
				minIndex = i
        
        # Supprimer la station ayant la distance minimale de la liste des sommets non vus
        # et l'ajouter à la liste des sommets vus 
		unvisited.remove(minIndex)
		visited.append(minIndex)
		return minIndex


	# Déterminer toutes les stations avec lesquelles la station courante à une transition commune
	def getNeighbours(self, currentStation):
		neighbours = []

		for i in range(len(self.transitions)):
			if (self.transitions[i][0] == currentStation or currentStation == self.transitions[i][1]):
				neighbours.append(self.transitions[i])

		# Vérifier si la station n'est pas à sens unique (portions sur les lignes 10 et 7B)
		for i in neighbours:
			if (currentStation == 34 and i[0] == 92):
				neighbours.remove(i)
			elif (currentStation == 248 and i[0] == 34):
				neighbours.remove(i)
			elif (currentStation == 280 and i[0] == 248):
				neighbours.remove(i)
			elif (currentStation == 92 and i[0] == 280):
				neighbours.remove(i)
			elif (currentStation == 145 and i[0] == 201):
				neighbours.remove(i)
			elif (currentStation == 196 and i[0] == 373):
				neighbours.remove(i)
			elif (currentStation == 259 and i[0] == 196):
				neighbours.remove(i)
			elif (currentStation == 36 and i[0] == 259):
				neighbours.remove(i)
			elif (currentStation == 52 and i[0] == 198):
				neighbours.remove(i)
			elif (currentStation == 201 and i[0] == 52):
				neighbours.remove(i)

		return neighbours


	# Récupérer la station d'arrivée pour le chemin le plus court
	def getFastestDest(self, dest, distance):
		destTry = []
		
		# Récupérer la liste des stations d'arrivées si elles sont le noeud de plusieurs de métro
		for i in range(len(self.stations)):
			if (self.stations[dest][3] == self.stations[i][3]):
				destTry.append(self.stations[i][0])
				while (self.stations[dest][3] == self.stations[i + 1][3]):
					destTry.append(self.stations[i + 1][0])
					i += 1

		# Récupérer la station d'arrivée avec la plus courte distance pour la station de départ
		destFinal = dest
		for i in range(len(destTry)):
			if (distance[destTry[i]] < distance[destFinal]):
				destFinal = destTry[i]

		return destFinal


	# Déterminer le trajet pour une station de départ et une station d'arrivée donnée
	def getTravel(self, start, dest, distance, prev, time):
		travel = []

		# Remplir la liste travel en traversant les pères de chaque station
		pere = dest
		travel.append(pere)
		while (pere != -1):
			pere = prev[pere]
			travel.append(pere)
		
		travel.reverse()

		return StockTravel(self, start, dest, travel, time)


	# Algorithme du plus court chemin (Dijkstra)
	def dijkstra(self, start, dest):
		# Initialiser la liste des sommets vus et des sommets non vus du graphe
		visited = []
		unvisited = [(i) for i in range(len(self.stations))]

		# Initialiser la distance de chaque sommet à l'infini
		# Initialiser la distance du sommet de départ à 0
		distance = [math.inf] * len(self.stations)
		distance[start] = 0

		# Initialiser la liste des sommets pères à -1
		prev = [-1] * len(self.stations)

		# Boucle principale de l'algorithme de Dijkstra
		while len(visited) < len(self.stations):
			currentStation = self.minDistance(distance, visited, unvisited)
			neighbours = self.getNeighbours(currentStation)

			# Pour chaque station voisine de la station courante
			# Si la distance à la station voisine est plus grande que la durée de transition 
			# entre la station courante et la station voisine
			# Alors, mettre à jour la distance de la station voisine et initialiser son père à la station courante
			for nextStation in range(len(neighbours)):
				if (neighbours[nextStation][0] == currentStation):
					if (distance[neighbours[nextStation][1]] > distance[currentStation] + neighbours[nextStation][2]):
						distance[neighbours[nextStation][1]] = distance[currentStation] + neighbours[nextStation][2]
						prev[neighbours[nextStation][1]] = currentStation
				if (neighbours[nextStation][1] == currentStation):
					if (distance[neighbours[nextStation][0]] > distance[currentStation] + neighbours[nextStation][2]):
						distance[neighbours[nextStation][0]] = distance[currentStation] + neighbours[nextStation][2]
						prev[neighbours[nextStation][0]] = currentStation

		# Récupérer la station d'arrivée pour le chemin le plus court
		destFinal = self.getFastestDest(dest, distance)
		
		# Récupérer le temps de trajet et le trajet
		time = getTime(distance, destFinal)
		return (self.getTravel(start, destFinal, distance, prev, time), time)


	# Déterminer la station terminus de la ligne avec deux numéros de station 
	# d'une même ligne en arguments, pour définir le sens du trajet,
	# plus le trajet entier qui permet d'analyser la direction a prendre sur la ligne 13
	def Terminus(self, previous6, current9, choice13):
		# previous6 est la station précédente, current9 est la station courante
		term = self.stations[current9][2]
		# La ligne 13 possède deux terminus dans un meme sens: il faut choisir
		# le bon terminus en fonction du trajet à parcourir.
		remove_direction = 0
		for i in range(len(choice13)-1):
			if (choice13[i] == 153 and choice13[i+1] == 131):
				remove_direction = 1
			if (choice13[i] == 153 and choice13[i+1] == 39):
				remove_direction = 2
		# Boucle qui se termine lorsqu'un terminus est trouvé
		while (term == "0"):
			neighbours = self.getNeighbours(self.stations[current9][0])
			# Liste des Indices des transitions dans neighbours à supprimer (1)
			delete = []
			for i in range(len(neighbours)):
				# On enlève les transitions avec les stations sur différentes lignes
				if (self.stations[current9][1] != self.stations[neighbours[i][0]][1] or
					self.stations[current9][1] != self.stations[neighbours[i][1]][1]):
					delete.append(i)
			delete.reverse()
			for i in range(len(delete)):
				neighbours.remove(neighbours[delete[i]])
			# Liste des Indices des transitions dans neighbours à supprimer (2)
			delete = []
			for i in range(len(neighbours)):
				# On enlève les transitions avec la station de laquelle on arrive
				if (self.stations[previous6][0] == neighbours[i][0] or
					self.stations[previous6][0] == neighbours[i][1]):
					delete.append(i)
			delete.reverse()
			for i in range(len(delete)):
				neighbours.remove(neighbours[delete[i]])
			# Si le trajet a parcourir va de La fourche vers Brochant,
			# on enlève la transition de La Fourche vers Guy Môquet,
			# et inversement si le trajet à parcourir va de La Fourche vers Guy Môquet
			if (remove_direction == 1):
				for i in range(len(neighbours)):
					if (current9 == 153):
						if (neighbours[i][0] == 39 or neighbours[i][1] == 39):
							neighbours.remove(neighbours[i])
							break
			if (remove_direction == 2):
				for i in range(len(neighbours)):
					if (current9 == 153):
						if (neighbours[i][0] == 131 or neighbours[i][1] == 131):
							neighbours.remove(neighbours[i])
							break
			# il ne reste plus qu'une seule transition dans la liste,
			# on utilise la nouvelle station comme station courante de la prochaine boucle
			previous6 = current9
			if (neighbours[0][0] == previous6):
				current9 = neighbours[0][1]
			elif (neighbours[0][1] == previous6):
				current9 = neighbours[0][0]
			term = self.stations[current9][2]
		#on retourne le nom de la station terminus
		return self.stations[current9][3]


#*********************#
#***** FUNCTIONS *****#
#*********************#

# Demander à l'utilisateur la station à laquelle il se trouve
def getStart(metro):
	start = input("\nStation de départ :\n\t>> ")
	metros_try = []
	
	# Rechercher dans la liste des stations si l'une d'elle correspond à celle donnée par l'utilisateur
	# Renvoie un tableau contenant toutes les instances de la station dans le fichier texte
	for i in range(len(metro.stations)):
		if (start == metro.stations[i][3]):
			metros_try.append(metro.stations[i])
			while (start == metro.stations[i+1][3]):
				metros_try.append(metro.stations[i+1])
				i+=1
		if (len(metros_try) > 0):
			return metros_try

	# Si la station n'est pas dans la liste
	print("\033[1m\x1b[31mLa station n'a pas été trouvée dans la base de données !\033[0m\x1b[39m")
	print("\033[1m\x1b[31mVérifiez que vous n'ayez pas fait de fautes de frappe.\033[0m\x1b[39m")
	return 1


# Demander à l'utilisateur la station à laquelle il souhaite se rendre
def getDestination(metro):
	dest = input("Station d'arrivée :\n\t>> ")

	# Rechercher dans la liste des stations si l'une d'elle correspond à celle donnée par l'utilisateur
	for i in range(len(metro.stations)):
		if (dest == metro.stations[i][3]):
			return metro.stations[i]

	# Si la station n'est pas dans la liste
	print("\033[1m\x1b[31mLa station n'a pas été trouvée dans la base de données !\033[0m\x1b[39m")
	print("\033[1m\x1b[31mVérifiez que vous n'ayez pas fait de fautes de frappe.\033[0m\x1b[39m")


# Transformer le temps de trajet en minutes-secondes
def getTime(distance, dest):
	time = []
	minutes = distance[dest] // 60
	time.append(minutes)
	seconds = distance[dest] - (minutes * 60)
	time.append(seconds)
	return time


# Stocker le trajet dans le tableau de String "realway"
def StockTravel(metro, start, dest, travel, time):
	realway = []
	realway.append("\033[96m\033[1m\nUn itinéraire a été trouvé !\033[0m")
	realway.append("Vous êtes à \033[1m{}\033[0m. Prenez la ligne \033[1m{}\033[0m, direction \033[1m{}\033[0m".format(metro.stations[start][3], metro.stations[start][1], metro.Terminus(travel[1], travel[2], travel)))
	i = 1
	# les commentaires entre triple guillemets représentent le code qui permet de voir
	# toutes les stations par lesquelles le trajet s'effectue
	while (i < (len(travel))):
		# newvalue = 0
		if (i >= 2):
			if (metro.stations[travel[i]][3] == metro.stations[travel[i-1]][3]):
				realway.append("Arrivé(e) à \033[1m{}\033[0m, prenez la ligne \033[1m{}\033[0m, direction \033[1m{}\033[0m".format(metro.stations[travel[i]][3], metro.stations[travel[i]][1], metro.Terminus(travel[i], travel[i+1], travel)))
				newvalue = 1
		# if (newvalue == 0):
		# 	realway.append("Vous passerez par la station \033[1m{}\033[0m (M{}).".format(metro.stations[travel[i]][3], metro.stations[travel[i]][1]))
		i -= -1
	realway.append("Vous arriverez à \033[1m{}\033[0m dans : \033[1m\033[32m{} min {} s\033[0m".format(metro.stations[dest][3], time[0], time[1]))
	return realway


# Stocke les chemins les plus courts des différentes lignes de métro de départ disponibles pour une station
# Affiche le chemin le plus court parmi ceux dans "Stationgroup"
def ShortestPath(metro, finalstart, finaldest):
	Stationgroup = []
	tempminutes = 9999
	tempseconds = 9999
	showvalue = 0
	# Stationgroup[i][0] est un tableau de String, retour de StockTravel
	# Stationgroup[i][1] est un tableau qui contient les minutes et les secondes, retour de getTime
	for i in range(len(finalstart)):
		Stationgroup.append(metro.dijkstra(finalstart[i][0], finaldest[0]))
		if (Stationgroup[i][1][0] < tempminutes):
			tempminutes = Stationgroup[i][1][0]
			tempseconds = Stationgroup[i][1][1]
			showvalue = i
		if (Stationgroup[i][1][0] == tempminutes):
			if (Stationgroup[i][1][1] < tempseconds):
				tempseconds = Stationgroup[i][1][1]
				showvalue = i
	for j in range( len(Stationgroup[showvalue][0]) ):
		print (Stationgroup[showvalue][0][j])


#*************************#
#***** FONCTION MAIN *****#
#*************************#

def main():
	cfgFile = "metro.txt"
	# Initialiser l'objet metro
	metro = MetroParisien(cfgFile)

	# Initialiser les stations de départ et d'arrivée
	Init_start = 0
	while (Init_start == 0):
		start = []
		while (start == []):
			start = getStart(metro)
			if (start != 1):
				Init_start = 1
	dest = None
	while (dest is None):
		dest = getDestination(metro)

	ShortestPath(metro, start, dest)


if __name__ == "__main__":
	main()
