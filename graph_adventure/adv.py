from room import Room
from player import Player
from world import World

import random
from queue import Queue

from roomgraph import roomGraph

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
world.loadGraph(roomGraph)
world.printRooms()
player = Player("Name", world.startingRoom)



def breadthfirstsearch(dictionary, room):
    visited = set()
    queue= Queue()
    path = [room]
    queue.put([room])
    while queue.empty() is False:
        # get list of room id's
        p = queue.get()
        # get first item off list of id's
        v = p[0]

        if v == '?':
            path = p[1:]
            break

        if v not in visited:
            visited.add(v)
            for e in dictionary[v]:
                node = dictionary[v][e]
                c = p.copy()
                # put node in list
                c.insert(0, node)
                # add list to queue
                queue.put(c)

    directions = []
    # go backwards
    while len(path) > 1:
        # get the last room in the path
        location = path.pop()
        # find the direction that'll take you to the new last room in the path and append to directions
        for route in dictionary[location]:
            if dictionary[location][route] == path[-1]:
                directions.append(route)

    return directions

# --- HELPERS ---


def the_other_side(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'w':
        return 'e'
    elif direction == 'e':
        return 'w'


# FILL THIS IN
walkingPath = ['n', 's']


# create dictionary for visited
visited = {}
count = 0
while len(visited) < len(roomGraph):
    room = player.currentRoom.id
    if room not in visited:
        visited[room] = {
            direction: '?' for direction in player.currentRoom.getExits()}
    unexplored = [direction for direction in visited[room]
                  if visited[room][direction] == '?']

    if len(unexplored):
        # go down a random pathway
        direction = unexplored[(random.randint(0, len(unexplored)-1))]
        player.travel(direction)

        walkingPath.append(direction)
        current_room = player.currentRoom.id
        visited[room][direction] = current_room

        # if current_room is not in visited, add it.:
        if current_room not in visited:
            visited[current_room] = {
                direction: '?' for direction in player.currentRoom.getExits()}
        # update current_room entry with old room data (the direction of the old room):
        op_dir = the_other_side(direction)
        visited[current_room][op_dir] = room

    else:
        # generate a list of directions to get to the nearest unexplored node using a breadthfirstsearch, loop through and send the player in those directions in order.
        directions = breadthfirstsearch(visited, room)
        walkingPath = walkingPath + directions
        for direction in directions:
            player.travel(direction)


# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom)
for move in walkingPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom)

if len(visited_rooms) == len(roomGraph):
    print(
        f"TESTS PASSED: {len(walkingPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")