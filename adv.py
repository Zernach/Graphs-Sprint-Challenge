from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # Y O U R # # # # C O D E # # # # H E R E # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# This will show the paths of the nearest rooms.
next_paths = []

# Instantiate an unexplored_rooms list as long as the number of total rooms.
unexplored_rooms = list(range(0,len(world.rooms)))

# Assign the first, root room as next_room for path exploration.
next_room = world.rooms[unexplored_rooms[0]]

# Remove the starting room from unexplored_rooms (room 0)
unexplored_rooms.remove(player.current_room.id)

# While there are still rooms in the unexplored_rooms list...
while len(unexplored_rooms) > 0:
    
    # Create a deque for the BFS and a set to save visited rooms.
    deque = deque()
    visited = set()

    # Add next room to a next_paths list and to the deque.
    next_paths.append(next_room)
    deque.append([next_room])

    # While this deque is not empty...
    while len(deque) > 0:

        # Pop the first -- first in, first out!
        path = deque.popleft()

        # Get the last room in the list of the path
        last_room = path[-1]

        # If last_room is an unexplored_rooms room, create list of directions.
        if last_room.id in unexplored_rooms:

            # First room in the path is current room to traverse.
            curr_room = path[0]

            # For all other rooms...
            for room in path[1:]:

                # Dictionary of rooms in fork: direction of that room from curr_room
                paths = {world.rooms[curr_room.id].get_room_in_direction(x).id:x for x in world.rooms[curr_room.id].get_exits()}

                # Append to the traversal_path that direction
                traversal_path.append(paths[room.id])

                # Set the current room as the room being explored right now in this loop.
                curr_room = room

            # Remove the last_room's id from unexplored_rooms
            unexplored_rooms.remove(last_room.id)

            # Next room to explore becomes last room.
            next_room = last_room
            break

        # If the last_room in the path is NOT in unexplored_rooms...
        else:

            # Add last_room.id to the visited set to not visit again.
            visited.add(last_room.id)
            
            for direction in world.rooms[last_room.id].get_exits():

                room_in_dir = last_room.get_room_in_direction(direction)

                # If that room isn't explored, add add to BFS to check for unexplored_rooms
                if room_in_dir.id not in visited:
                    deque.append(path+[room_in_dir])

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # Y O U R # # # # C O D E # # # # H E R E # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
#player.current_room.print_room_description(player)
#while True:
#    cmds = input("-> ").lower().split(" ")
#    if cmds[0] in ["n", "s", "e", "w"]:
#        player.travel(cmds[0], True)
#    elif cmds[0] == "q":
#        break
#    else:
#        print("I did not understand that command.")
