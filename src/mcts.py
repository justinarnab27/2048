import random
import copy
import math
from game import game

'''
we have 4 steps selection, expansion, simulation, backup
'''

c = 1.4142 
INF_VAL = 1e9
MAX_ITER = 200
MAX_DEPTH = 300 

class node:

	def __init__(self):
		self.value = 0
		self.n = 0
		self.children = [None,None,None,None]

	def sigmoid(self,z,tot):
		if tot == 0:
			tot = 1
		return z/tot 

	def ugb(self,N,tot):
		assert self.n != 0
		return self.sigmoid(self.value/self.n,tot) + c*math.sqrt(math.log(N)/self.n) 

def selection(current_node,tree_path,my_game,N):
	tree_path.append(current_node)
	possible_moves = my_game.check_possible_moves()
	if not possible_moves:
		return
	ugb_scores = []
	tot = 0 
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
	mx =  ugb_scores[0][0]
	mx_ix = ugb_scores[0][1]
	for i in ugb_scores:
		if i[0] > mx:
			mx = i[0]
			mx_ix = i[1]
	next_move = mx_ix
	my_game.next_turn(next_move)
	if current_node.children[next_move] == None:
		next_node = node()
		current_node.children[next_move] = next_node
		tree_path.append(next_node)
		return
	selection(current_node.children[next_move],tree_path,my_game,N)

def simulation(next_node,my_game):
	iter_num = MAX_DEPTH
	while iter_num > 0 and not my_game.game_over:
		possible_moves = my_game.check_possible_moves()
		if not possible_moves:
			break
		my_game.next_turn(random.choice(possible_moves))
		iter_num -= 1
	return my_game.current_score

def back_prop(tree_path,new_score):
	for i in tree_path:
		i.n += 1
		i.value += new_score

def iteration(root_node,my_game,N):
	tree_path = []
	selection(root_node,tree_path,my_game,N)
	assert tree_path
	new_score = simulation(tree_path[-1],my_game)
	back_prop(tree_path,new_score)
	
def decide_next_move(board,score):
	my_game = game()
	root_node = node()
	N = 0
	for i in range(MAX_ITER):
		N += 1
		my_game.change_board(board)
		my_game.change_score(score)
		iteration(root_node,my_game,N)
	my_game.change_board(board)
	my_game.change_score(score) 
	possible_moves = my_game.check_possible_moves()
	assert possible_moves
	mx = possible_moves[0] 
	mx_ix = 0
	ls = []
	for i in possible_moves:
		if root_node.children[i]!=None and root_node.children[i].value/root_node.children[i].n > mx:

			ls.append(root_node.children[i].value/root_node.children[i].n)
			mx = root_node.children[i].value/root_node.children[i].n
			mx_ix = i
	return mx_ix
	

#new_game = game()
#it = 0
#while not new_game.game_over:
#	if it == 1000:
#		break
#	it += 1
#	board = copy.deepcopy(new_game.board)
#	user_input = decide_next_move(board,new_game.current_score) 
#	new_game.next_turn(user_input)
#	new_game.display_board()
#new_game.display_board()
#print(it,new_game.current_score)