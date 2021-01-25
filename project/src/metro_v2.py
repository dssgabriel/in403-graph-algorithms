import os
import sys
import math

class Metro:
	stations = []
	transitions = []

	def __init__(self, filename):
		cfg = open(filename, 'r')
		
		while (True):
			line = cfg.readline()
			line = line.rstrip()
			if (line.startswith('V')):
				vertex = line.strip("V ").split(' ', 3)
				self.stations.append(vertex)
				continue
			if (line.startswith('E')):
				edge = line.strip("E ").split(' ', 2)
				self.transitions.append(edge)
				continue
			if not line:
				cfg.close()
				break
		
		for i in range(len(self.stations)):
			self.stations[i][0] = int(self.stations[i][0])
		
		for i in range(len(self.transitions)):
			self.transitions[i][0] = int(self.transitions[i][0])
			self.transitions[i][1] = int(self.transitions[i][1])
			self.transitions[i][2] = int(self.transitions[i][2])


	def min_distance(self, distance, unvisited):
		min_dist = math.inf
		min_index = -1

		for i in unvisited:
			if (distance[i] < min_dist):
				min_dist = distance[i]
				min_index = i
		
		return min_index


	def get_neighbours(self, current_station):
		neighbours = []
		
		for i in range(len(self.transitions)):
			if (self.transitions[i][0] == current_station or self.transitions[i][1] == current_station):
				neighbours.append(self.transitions[i])

		for i in neighbours:
			if (current_station == 34 and i[0] == 92):
				neighbours.remove(i)
			if (current_station == 248 and i[0] == 34):
				neighbours.remove(i)
			if (current_station == 280 and i[0] == 248):
				neighbours.remove(i)
			if (current_station == 92 and i[0] == 280):
				neighbours.remove(i)
			if (current_station == 145 and i[0] == 201):
				neighbours.remove(i)
			if (current_station == 196 and i[0] == 373):
				neighbours.remove(i)
			if (current_station == 259 and i[0] == 196):
				neighbours.remove(i)
			if (current_station == 36 and i[0] == 259):
				neighbours.remove(i)
			if (current_station == 52 and i[0] == 198):
				neighbours.remove(i)
			if (current_station == 201 and i[0] == 52):
				neighbours.remove(i)
		
		return neighbours


	def get_fastest(self, arrival, distance):
		trial = []
		for i in range(len(self.stations)):
			if (self.stations[arrival][3] == self.stations[i][3]):
				trial.append(self.stations[i][0])
				while (self.stations[arrival][3] == self.stations[i + 1][3]):
					trial.append(self.stations[i + 1][0])
					i += 1

		for i in range(len(trial)):
			if (distance[trial[i]] < distance[arrival]):
				arrival = trial[i]
		return arrival


	def get_travel(self, start, dest, distance, prev, time):
		travel = []
		father = dest
		travel.append(father)
		while (father != -1):
			father = prev[father]
			travel.append(father)
		travel.reverse()
		return store_travel(self, start, dest, travel, time)


	def dijkstra(self, departure, arrival):
		visited = []
		unvisited = [(i) for i in range(len(self.stations))]
		distance = [math.inf] * len(self.stations)
		distance[departure] = 0
		prev = [-1] * len(self.stations)

		while len(visited) < len(self.stations):
			stop_time = 30
			current = self.min_distance(distance, unvisited)
			unvisited.remove(current)
			visited.append(current)

			neighbours = self.get_neighbours(current)
			
			for n in range(len(neighbours)):
				if (neighbours[n][0] == current):
					if (distance[neighbours[n][1]] > distance[current] + neighbours[n][2]):
						distance[neighbours[n][1]] = distance[current] + neighbours[n][2] + stop_time
						prev[neighbours[n][1]] = current

				if (neighbours[n][1] == current):
					if (distance[neighbours[n][0]] > distance[current] + neighbours[n][2]):
						distance[neighbours[n][0]] = distance[current] + neighbours[n][2] + stop_time
						prev[neighbours[n][0]] = current

		smart_arrival = self.get_fastest(arrival, distance)
		time = get_time(distance, smart_arrival)

		return (self.get_travel(departure, smart_arrival, distance, prev, time), time)


	def terminus(self, previous6, current9, choice13):
		term = self.stations[current9][2]
		remove_direction = 0
		for i in range(len(choice13)-1):
			if (choice13[i] == 153 and choice13[i+1] == 131):
				remove_direction = 1
			if (choice13[i] == 153 and choice13[i+1] == 39):
				remove_direction = 2
		while (term == "0"):
			neighbours = self.get_neighbours(self.stations[current9][0])
			delete = []
			for i in range(len(neighbours)):
				if (self.stations[current9][1] != self.stations[neighbours[i][0]][1] or
					self.stations[current9][1] != self.stations[neighbours[i][1]][1]):
					delete.append(i)
			delete.reverse()
			for i in range(len(delete)):
				neighbours.remove(neighbours[delete[i]])
			delete = []
			for i in range(len(neighbours)):
				if (self.stations[previous6][0] == neighbours[i][0] or
					self.stations[previous6][0] == neighbours[i][1]):
					delete.append(i)
			delete.reverse()
			for i in range(len(delete)):
				neighbours.remove(neighbours[delete[i]])
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
			previous6 = current9
			if (neighbours[0][0] == previous6):
				current9 = neighbours[0][1]
			elif (neighbours[0][1] == previous6):
				current9 = neighbours[0][0]
			term = self.stations[current9][2]
		return self.stations[current9][3]

def get_station(metro):
	matches = []
	while (True):
		entry = input("Please input a station:\n")
		for i in range(len(metro.stations)):
			if (entry == metro.stations[i][3]):
				matches.append(metro.stations[i])
		if matches:
			break
		else:
			print("\033[1;31mStation was not found in database.\033[0m")
	return matches

def get_time(distance, dest):
	time = []
	minutes = distance[dest] // 60
	time.append(minutes)
	seconds = distance[dest] - (minutes * 60)
	time.append(seconds)
	return time

def store_travel(metro, start, dest, travel, time):
	realway = []
	realway.append("\033[96m\033[1m\nUn itinéraire a été trouvé !\033[0m")
	realway.append("Vous êtes à \033[1m{}\033[0m. Prenez la ligne \033[1m{}\033[0m, direction \033[1m{}\033[0m".format(metro.stations[start][3], metro.stations[start][1], metro.terminus(travel[1], travel[2], travel)))
	i = 1
	while (i < (len(travel))):
		if (i >= 2):
			if (metro.stations[travel[i]][3] == metro.stations[travel[i-1]][3]):
				realway.append("Arrivé(e) à \033[1m{}\033[0m, prenez la ligne \033[1m{}\033[0m, direction \033[1m{}\033[0m".format(metro.stations[travel[i]][3], metro.stations[travel[i]][1], metro.terminus(travel[i], travel[i+1], travel)))
				newvalue = 1
		i -= -1
	realway.append("Vous arriverez à \033[1m{}\033[0m dans : \033[1m\033[32m{} min {} s\033[0m".format(metro.stations[dest][3], time[0], time[1]))
	return realway

def shortest_path(metro, departures, arrivals):
	station_group = []
	minutes = math.inf
	seconds = math.inf
	showvalue = 0
	for i in range(len(departures)):
		station_group.append(metro.dijkstra(departures[i][0], arrivals[0][0]))
		if (station_group[i][1][0] < minutes):
			minutes = station_group[i][1][0]
			seconds = station_group[i][1][1]
			showvalue = i
		if (station_group[i][1][0] == minutes):
			if (station_group[i][1][1] < seconds):
				seconds = station_group[i][1][1]
				showvalue = i
	for j in range(len(station_group[showvalue][0])):
		print(station_group[showvalue][0][j])

def main():
	db = "metro-database.txt"
	metro = Metro(db)

	print("\nDeparture:")
	departure = get_station(metro)
	print("\nArrival:")
	arrival = get_station(metro)

	shortest_path(metro, departure, arrival)

if __name__ == "__main__":
	main()
