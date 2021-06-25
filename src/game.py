import random

class game:
	board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]   #The game board
	board_size = 4	#Size of the board i.e. numbers of rows and columns
	current_score = 0  #Current score of the user
	highest_score = 0  #Highest Score of the user
	game_over = False   #Variable to indicate whether gane is over
	has_moved = False    #Indicates if the board has changed due to a move
	valid_moves = range(4)  #List of valid moves

	def change_board(new_board):
		'''Changes the board to new board'''
		board = new_board.deepcopy()

	def is_game_on(self):
		'''Returns true if at least one move is possible'''
		flag = False
		for i in range(4):
			flag = flag or self.move(i,True)    #flag becomes true if move i is possible
		return flag


	def spawn_new_cell(self):
		'''Spawns a new 2 in an empty cell
			if no empty cell is available game is over'''
		empty_cell_list = []   #List of empty cells
		#Iterates over all cells to find empty cell
		for i in range(self.board_size):
			for j in range(self.board_size):
				if self.board[i][j] == 0:
					empty_cell_list.append((i,j))
		pair = empty_cell_list[random.randrange(len(empty_cell_list))]   #randomly chooses an empty cell and then assigns 2 to it
		self.board[pair[0]][pair[1]] = random.choices([2,4],weights=[9,1])[0]


	def can_propagate(self,r_old,c_old,move_type):
		'''The functions check if by using a move move_type can the cell be moved
			Returns true if can be moved'''
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

		if r < 0 or c < 0 or r >= self.board_size or c >= self.board_size:   #if the cell is at the edge
			return
		else:
			if self.board[r][c] == self.board[r_old][c_old]: #if the adjacent cell is equal to current cell
				return True
			elif self.board[r][c] == 0:    #if the adjacent cell is empty
				return True
		return False



	def propagate(self,r_old,c_old,move_type):
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

		if r < 0 or c < 0 or r >= self.board_size or c >= self.board_size:   #if the cell is at the edge
			return
		else:
			if self.board[r][c] == self.board[r_old][c_old]: #if the adjacent cell is equal to current cell
				self.current_score += self.board[r][c] + self.board[r_old][c_old]
				self.highest_score = max(self.highest_score,self.current_score)
				self.board[r][c] += self.board[r_old][c_old] #add them
				self.board[r_old][c_old] = 0
				self.has_moved = True       #The board has changed
			elif self.board[r][c] == 0:    #if the adjacent cell is empty
				self.board[r][c] = self.board[r_old][c_old]   #propagate to next cell
				self.board[r_old][c_old] = 0
				self.propagate(r,c,move_type)
				self.has_moved = True           #The board has changed

	def move(self,user_input,dont_change = False):
		'''Performs the move the user has chosen.
		user_input is 0 up, 1 right, 2 down, 3 left 
		if dont_change is True it only checks if by using 
		move user_input the board can be changed. Returns true if
		it is possible'''
		#Iterates over each cell and propagates it if it is not empty
		flag = False   #flag denotes whether board can be changed
		if user_input == 0:
			for i in range(self.board_size):
				for j in range(self.board_size):
					if self.board[i][j] != 0:
						if dont_change:
							flag = flag or self.can_propagate(i,j,0)   #flag becomes true if at least one cell can be moved
						else:
							self.propagate(i,j,0)
		elif user_input == 1:
			for i in range(self.board_size-1,-1,-1):
				for j in range(self.board_size):
					if self.board[j][i] != 0:
						if dont_change:
							flag = flag or self.can_propagate(j,i,1)
						else:
							self.propagate(j,i,1)

		elif user_input == 2:
			for i in range(self.board_size-1,-1,-1):
				for j in range(self.board_size):
					if self.board[i][j] != 0:
						if dont_change:
							flag = flag or self.can_propagate(i,j,2)
						else:
							self.propagate(i,j,2)
		else:
			for i in range(self.board_size):
				for j in range(self.board_size):
					if self.board[j][i] != 0:
						if dont_change:
							flag = flag or self.can_propagate(j,i,3)
						else:
							self.propagate(j,i,3)

		return flag


	def display_board(self):
		'''Displats the board'''
		for i in self.board:
			for j in i:
				print(j,end=' ')
			print()

	def get_highest_score(self):
		'''Gets the highest score from the highest_score.txt file'''
		file = open("highest_score.txt","r")
		x = int(file.read())
		file.close()
		return x

	def save_highest_score(self,score):
		'''Saves score as highest score by writing it in the 
			highest_score.txt file'''
		file = open("highest_score.txt","w")
		file.write(str(score))
		file.close()

	def __init__(self):
		'''Initializes the game'''
		self.game_over = False        #Sets the gameover variable to false
		self.current_score = 0   #Sets the current_score to 0
		self.highest_score = self.get_highest_score()
		for i in range(self.board_size):
			for j in range(self.board_size):
				self.board[i][j] = 0
		self.board[random.randrange(self.board_size)][random.randrange(self.board_size)] = 2   #randomly assign 2 to one cell

	def end_game(self):
		'''Ends the game and saves the data'''
		self.save_highest_score(self.highest_score)

	def next_turn(self,user_input):
		'''The main game loop'''
		self.has_moved = False     #Resets has_moved to false at beginning of each turn
		#.user_input = int(input("Your next move: "))   #Takes users input
		if user_input == -1:  #Pressing -1 finishes the game
			self.end_game()
			return
		if user_input not in self.valid_moves:    #If users move is not valid then ignores the move
			print("Wrong Move!")
		self.move(user_input)    #Performs the move
		if self.has_moved:           #Only spawns new cells if board has changed
			self.spawn_new_cell()

		if not self.is_game_on():   #If no move can change the board then game is over
			self.end_game()
			self.game_over = True
