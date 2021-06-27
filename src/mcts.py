import random
import copy
import math
from game import game

c = 1.4142   #exploration parameter for trade-off between exploration and exploitation
INF_VAL = 1e9  	#Very large Number
MAX_ITER = 1000  #Number of iterations to perform
MAX_DEPTH = 300 #Depth of each simulation

class node:
	'''Class to represent nodes of the Monte-Carlo-Search-Tree (MCTS)'''
	def __init__(self):
		#Initializes the node
		self.value = 0    #Value of each node
		self.n = 0         #Number of times the node has been visited
		self.children = [None,None,None,None]    #Children of the node

	def sigmoid(self,z,tot):
		'''Function to squash the score value'''
		if tot == 0:
			tot = 1
		return z/tot 

	def ugb(self,N,tot):
		'''Gives the (modified) Upper Confidence Bound'''
		assert self.n != 0
		return self.sigmoid(self.value/self.n,tot) + c*math.sqrt(math.log(N)/self.n) 

def selection(current_node,tree_path,my_game,N):
	'''Finds a leaft node and adds a child node to it'''
	tree_path.append(current_node) #Adds the visited nodes to tree_path
	possible_moves = my_game.check_possible_moves()   #Returns if node is terminal
	if not possible_moves:
		return
	ugb_scores = []         #Stores ucb scores of the children
	tot = 0				#Sum of ucb of all children 
	#Sums the ucb's
	for i in possible_moves:
		if current_node.children[i] == None or current_node.children[i].n == 0:
			tot += INF_VAL
		else:
			tot += current_node.children[i].value/current_node.children[i].n
	for i in possible_moves:
		if current_node.children[i] == None:
			ugb_scores.append([INF_VAL,i])
		else:
			ugb_scores.append([current_node.children[i].ugb(N,tot),i])
	assert ugb_scores
	#Finds the max ucb of the children
	mx =  ugb_scores[0][0]
	mx_ix = ugb_scores[0][1]
	for i in ugb_scores:
		if i[0] > mx:
			mx = i[0]
			mx_ix = i[1]
	next_move = mx_ix
	my_game.next_turn(next_move)
	#If node is leaf node then adds a new node it and returns
	if current_node.children[next_move] == None:
		next_node = node()
		current_node.children[next_move] = next_node
		tree_path.append(next_node)
		return
	#else it continues till it finds a leaf node
	selection(current_node.children[next_move],tree_path,my_game,N)

def simulation(next_node,my_game):
	'''Simulates a game by randomly playing'''
	iter_num = MAX_DEPTH   #Game continues till MAX_DEPTH turns
	while iter_num > 0 and not my_game.game_over:
		possible_moves = my_game.check_possible_moves()
		if not possible_moves:
			break
		my_game.next_turn(random.choice(possible_moves))   #Randomly chooses a possible move
		iter_num -= 1
	return my_game.current_score   #returns scores achieved in the simulation

def back_prop(tree_path,new_score):
	'''Updates the values of the nodes in tree_path'''
	for i in tree_path:
		i.n += 1
		i.value += new_score

def iteration(root_node,my_game,N):
	'''Performs an iteration: selection, expansion, simulation and backprop'''
	tree_path = []   #Holds the nodes visited 
	selection(root_node,tree_path,my_game,N)   #Finds a leaf node
	assert tree_path 
	new_score = simulation(tree_path[-1],my_game)   #Performs a simulation and returns the score achieved
	back_prop(tree_path,new_score)     #Backpropagates the score to visited nodes
	
def decide_next_move(board,score):
	'''Decides the next move of the AI'''
	my_game = game()    #Creates a new game instance
	root_node = node()    #Creates a root node for the MCTS
	N = 0
	for i in range(MAX_ITER):     #Performs the iteration step MAX_ITER times
		N += 1
		my_game.change_board(board)    #Restores the board to original position after each game simulation
		my_game.change_score(score)
		iteration(root_node,my_game,N)
	my_game.change_board(board)
	my_game.change_score(score) 
	possible_moves = my_game.check_possible_moves()
	assert possible_moves
	mx = possible_moves[0] 
	mx_ix = 0
	ls = []
	for i in possible_moves:       #chooses the move with best value
		if root_node.children[i]!=None and root_node.children[i].value/root_node.children[i].n > mx:

			ls.append(root_node.children[i].value/root_node.children[i].n)
			mx = root_node.children[i].value/root_node.children[i].n
			mx_ix = i
	return mx_ix