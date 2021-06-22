import random

board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]   #The game board
board_size = 4	#Size of the board i.e. numbers of rows and columns
current_score = 0  #Current score of the user
highest_score = 0  #Highest Score of the user
game_over = False   #Variable to indicate whether gane is over
has_moved = False    #Indicates if the board has changed due to a move

def spawn_new_cell():
	'''Spawns a new 2 in an empty cell
		if no empty cell is available game is over'''
	empty_cell_list = []   #List of empty cells
	#Iterates over all cells to find empty cell
	for i in range(board_size):
		for j in range(board_size):
			if board[i][j] == 0:
				empty_cell_list.append((i,j))
	if not empty_cell_list:		#if no empty cell, game_over is set to true
		global game_over
		game_over = True
	else:
		pair = empty_cell_list[random.randrange(len(empty_cell_list))]   #randomly chooses an empty cell and then assigns 2 to it
		board[pair[0]][pair[1]] = random.choices([2,4],weights=[9,1])[0]


def propagate(r_old,c_old,move_type):
	'''The propagate function takes the current cell and updates its adjacent cell.
	r_old,c_old coordinates of the cell to be propagated
	Movetype is the user input'''
	r = r_old  #The coordinates of the next adjacent cell 
	c = c_old 

	if move_type == 0:
		r -= 1
	elif move_type == 1:
		c += 1
	elif move_type == 2:
		r += 1
	else:
		c -= 1

	if r < 0 or c < 0 or r >= board_size or c >= board_size:   #if the cell is at the edge
		return
	else:
		global has_moved
		if board[r][c] == board[r_old][c_old]: #if the adjacent cell is equal to current cell
			global current_score
			current_score += board[r][c] + board[r_old][c_old]
			global highest_score
			highest_score = max(highest_score,current_score)
			board[r][c] += board[r_old][c_old] #add them
			board[r_old][c_old] = 0
			has_moved = True       #The board has changed
		elif board[r][c] == 0:    #if the adjacent cell is empty
			board[r][c] = board[r_old][c_old]   #propagate to next cell
			board[r_old][c_old] = 0
			propagate(r,c,move_type)
			has_moved = True           #The board has changed

def move(user_input):
	'''Performs the move the user has chosen.
	user_input is 0 up, 1 right, 2 down, 3 left '''
	#Iterates over each cell and propagates it if it is not empty
	if user_input == 0:
		for i in range(board_size):
			for j in range(board_size):
				if board[i][j] != 0:
					propagate(i,j,0)
	elif user_input == 1:
		for i in range(board_size-1,-1,-1):
			for j in range(board_size):
				if board[j][i] != 0:
					propagate(j,i,1)
	elif user_input == 2:
		for i in range(board_size-1,-1,-1):
			for j in range(board_size):
				if board[i][j] != 0:
					propagate(i,j,2)
	else:
		for i in range(board_size):
			for j in range(board_size):
				if board[j][i] != 0:
					propagate(j,i,3)



def display_board():
	'''Displats the board'''
	for i in board:
		for j in i:
			print(j,end=' ')
		print()

def get_highest_score():
	'''Gets the highest score from the highest_score.txt file'''
	file = open("highest_score.txt","r")
	x = int(file.read())
	file.close()
	return x

def save_highest_score(score):
	'''Saves score as highest score by writing it in the 
		highest_score.txt file'''
	file = open("highest_score.txt","w")
	file.write(str(score))
	file.close()

def play_game():
	'''The main game loop'''
	global game_over
	game_over = False        #Sets the gameover variable to false
	global current_score    
	current_score = 0   #Sets the current_score to 0
	global highest_score
	highest_score = get_highest_score()
	valid_moves = range(4)  #List of valid moves
	board[random.randrange(board_size)][random.randrange(board_size)] = 2   #randomly assign 2 to one cell
	while(1):
		if game_over:
			print("GAME OVER!")
			break
		display_board()   #Displays current board state
		global has_moved
		has_moved = False     #Resets has_moved to false at beginning of each turn
		user_input = int(input("Your next move: "))   #Takes users input
		if user_input == -1:  #Pressing -1 finishes the game
			break
		if user_input not in valid_moves:    #If users move is not valid then ignores the move
			print("Wrong Move!")
			continue	
		move(user_input)    #Performs the move
		if has_moved:           #Only spawns new cells if board has changed
			spawn_new_cell()
		print(f"Current Score {current_score}")  #Prints the current score
		print(f"Highest Score {highest_score}")  #Prints the current score
	save_highest_score(highest_score)


play_game()