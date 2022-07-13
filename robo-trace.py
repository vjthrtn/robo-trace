import robot_race_functions as rr
from collections import deque, Counter, namedtuple
from time import time, sleep

maze_file_name = 'maze_data_1.csv'
seconds_between_turns = 0.3
max_turns = 35

#initialize the robot race
maze_data = rr.read_maze(maze_file_name)
rr.print_maze(maze_data)
walls, goal, bots = rr.process_maze_init(maze_data)

#populate a deque of all robot commands for the maze
robot_moves = deque()
num_of_turns = 0
while not rr.is_race_over(bots) and num_of_turns < max_turns:
  #for every bot in the list of bots, if the bot has not reached the end, add a new move to the robot_moves deque
  for bot in bots:
    if bot.has_finished == False:
      robot_moves.append(rr.compute_robot_logic(walls, goal,bot))

  num_of_turns += 1

#count the number of moves based on the robot names
num_of_moves = Counter(move[0] for move in robot_moves)


#count the number of collisions by robot name
num_of_collisions = Counter(move[0] for move in robot_moves if move[2] == True)

#make a namedtuple to keep track of the robots points
BotScoreData = namedtuple('BotScoreData', ['name', 'num_moves', 'num_collisions', 'score'])

#calculate scores (moves + collisions) for each robot and append it to bot_scores 
bot_scores = []

for bot in bots:
  score = num_of_moves[bot.name] + num_of_collisions[bot.name]
  bot_scores.append(BotScoreData(bot.name,num_of_moves[bot.name],num_of_collisions[bot.name], score))

#populate a dict to keep track of the robot movements
bot_data = {}

for bot in bots:
  bot_data[bot.name] = bot


#move the robots and update the map based on the moves deque
while len(robot_moves) > 0:
  #make sure to pop moves from the front of the deque
  bot_name, move, hit_wall = robot_moves.popleft()
  bot_data[bot_name].process_move(move)

  #update the maze characters based on the robot positions and print it to the console
  rr.update_maze_characters(maze_data, bots)
  rr.print_maze(maze_data)
  sleep(seconds_between_turns - time() % seconds_between_turns)

#printing out the results
rr.print_results(bot_scores)
