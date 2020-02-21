from room import Room
from player import Player
from world import World

import sys
import random
from ast import literal_eval

sys.setrecursionlimit(1010)

class Maze:
    def __init__(self):

        # Load world
        self.world = World()


        # You may uncomment the smaller graphs for development and testing purposes.
        # self.map_file = "maps/test_line.txt"
        # self.map_file = "maps/test_cross.txt"
        # self.map_file = "maps/test_loop.txt"
        # self.map_file = "maps/test_loop_fork.txt"
        self.map_file = "maps/main_maze.txt"


        # Loads the map into a dictionary
        self.room_graph=literal_eval(open(self.map_file, "r").read())
        self.world.load_graph(self.room_graph)

        self.player = Player(self.world.starting_room)

        # Fill this out with directions to walk
        # traversal_path = ['n', 'n']
        self.traversal_path = []
        # List of visited rooms for Maze Runner to avoid infinite loops.
        self.path_markers = []
        self.return_path = []
        # Last room used for backtracking.
        self.last_room = self.world.starting_room




    def traversal_adder(self, current_room, neighbor):
        # Adds the instruction to reach the new room to our traversal path.
        if current_room.n_to == neighbor:
            self.traversal_path.append("n")
        if current_room.e_to == neighbor:
            self.traversal_path.append("e")
        if current_room.s_to == neighbor:
            self.traversal_path.append("s")
        if current_room.w_to == neighbor:
            self.traversal_path.append("w")

    def maze_runner(self, current_room):
        # print(f"Current Room: {current_room}")
        # print(f"Markers:      {self.path_markers}")
        # print(f"Neighbors:    {current_room.neighbors()}")
        # print(f"Return Path:  {self.return_path}")

         # Check if room hasn't been visited.S
        if len(self.return_path) > 1:
            prev_room = self.return_path[-1]
        elif len(self.return_path) == 1:
            prev_room = self.return_path[0]

        self.path_markers.append(current_room)


    # Ends the cycle if current room's neighbors are all explored and the current_room is the starting room.  Should only happen when all rooms are explored.
        if all(elem in self.path_markers for elem in current_room.neighbors()) and current_room == self.world.starting_room:
            return
        # Begins to back up if every neighbor has been visited.
        elif all(elem in self.path_markers for elem in current_room.neighbors()):
            # print("Back that ass up")
            # print(current_room.name)
            # print(self.return_path)
            # print(prev_room.name)
            self.return_path.pop()
            self.traversal_adder(current_room, prev_room)
            self.maze_runner(prev_room)
        # If there are neighbors that haven't been visited, recurse with the neighbor.
        else:
            for neighbor in current_room.neighbors():
                if neighbor not in self.path_markers:
                    # If the path continues, sets the last room to the current room.
                    self.return_path.append(current_room)
                    # print(self.return_path)

                    self.last_room = current_room
                    self.traversal_adder(current_room, neighbor)
                    # print("Going deeper")
                    # print(current_room.name)
                    self.maze_runner(neighbor)
                else:
                    pass

    def run(self):
        self.maze_runner(self.player.current_room)
        print(self.traversal_path)
        self.world.print_rooms()




        # TRAVERSAL TEST
        visited_rooms = set()
        self.player.current_room = self.world.starting_room
        visited_rooms.add(self.player.current_room)

        for move in self.traversal_path:
            self.player.travel(move)
            visited_rooms.add(self.player.current_room)

        if len(visited_rooms) == len(self.room_graph):
            print(f"TESTS PASSED: {len(self.traversal_path)} moves, {len(visited_rooms)} rooms visited")
        else:
            print("TESTS FAILED: INCOMPLETE TRAVERSAL")
            print(f"{len(self.room_graph) - len(visited_rooms)} unvisited rooms")

maze = Maze()

maze.run()

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
