import tkinter as tk
from tkinter import PhotoImage, messagebox
from game import game
import mcts 
import copy
import random

#dict mapping cell values to background colors
bg_color = {
	0 : '#cc3300',
	2 : '#ff99ff',
	4 : '#ff6666',
	8 : '#ffff00',
	16 : '#ff9900',
	32 : '#ff5c33',
	64 : '#66ffff'
}

new_game = game() 

def update_board():
	'''Updates the board'''
	#iterates over whole board
	for i in range(new_game.board_size):
		for j in range(new_game.board_size):
			color_background = '#cc66ff'  #Default Color
			if new_game.board[i][j] in bg_color:
				color_background = bg_color[new_game.board[i][j]]
			board_var_list[i][j].configure(background=color_background)
			if new_game.board[i][j] == 0:
				board_var_list[i][j].configure(text='')
			else:
				board_var_list[i][j].configure(text=new_game.board[i][j])

def btn_start_new_game():
	'''Activates on clicking new game button
		Ends the current game and creates new game'''
	new_game.end_game()
	start_new_game()

def btn_reset_score():
	'''Activates on clicking reset score button
		Resets the current score to 0'''
	result = messagebox.askyesno("Warning!","Do you want to reset highest score to zero?") #Creates confirmation box
	if result:  #sets highest score to zero and restarts game
		new_game.highest_score = 0
		new_game.save_highest_score(new_game.highest_score)
		start_new_game()	

def AI_move():
	'''Performs the AI's next move and updates the board'''
	board = copy.deepcopy(new_game.board)
	user_input = mcts.decide_next_move(board,new_game.current_score) 
	new_game.next_turn(user_input)          #Plays the game with AI move
	new_game.display_board()
	update_board()            #Updates board
	score_var.set(f"Your Score:\n{new_game.current_score}")  #Updates the score
	highest_score_var.set(f"Highest Score:\n{new_game.highest_score}")   #Updates the highest score
	if new_game.game_over:        #If game is over displays game over message
		messagebox.showinfo("Game Over","Game Over!")
	else:
		window.after(100,AI_move)    #If game is not over calls itself again


def start_AI():
	'''Activates when AI button is pressed, starts game and lets AI play it'''
	start_new_game()
	window.after(100,AI_move)

window = tk.Tk()
window.resizable(False,False)

frame_grid = tk.Frame(master=window) #frame for containing the main grid of the game
frame_grid.grid(row=0,column=0) 

frame_side = tk.Frame(master=window,bg='white') #frame for containing side pan
frame_side.grid(row=0,column=1,sticky='nsew')

#creates a 3x3 grid for the game
board_var_list = []   #Stores all the cells
for i in range(new_game.board_size):
	row = [] 
	for j in range(new_game.board_size):
		#Creates the cells
		box = tk.Label(master=frame_grid,width=4,height=2,borderwidth=3,relief=tk.RIDGE,font=("Arial",35))
		row.append(box)
		box.grid(row=i,column=j)
	board_var_list.append(row)

score_var = tk.StringVar()
highest_score_var = tk.StringVar()

#Creates label for current score
label_your_score = tk.Label(master=frame_side,textvariable=score_var,bg='white',font = ('Arial',12,'bold'))  #Label showing the users current score
label_your_score.pack(pady=10,padx=5)

#Creates labels for highest scores
label_highest_score = tk.Label(master=frame_side,textvariable=highest_score_var,bg='white',font = ('Arial',12,'bold')) #Label showing the users highest score
label_highest_score.pack(padx=5)

#Creates button for resetting the highest score to 0
button_reset_score = tk.Button(master=frame_side,text="Reset Scores",command=btn_reset_score,bg='red',fg='white') #Button for creating a new game

button_reset_score.pack(side=tk.BOTTOM,padx=5,pady=10)

#Creates button for playing AI game
button_ai_game = tk.Button(master=frame_side,text="AI Game",command=start_AI,bg='red',fg='white') #Button for creating a new game
button_ai_game.pack(side=tk.BOTTOM,padx=5,pady=10)

#Button for restarting the game
button_new_game = tk.Button(master=frame_side,text="New Game",command=btn_start_new_game,bg='red',fg='white') #Button for creating a new game
button_new_game.pack(side=tk.BOTTOM,padx=5,pady=10)

def arrow_press(event):
	'''The functions is activated is an arrow keys is pressed
		and then updates the board'''
	if new_game.game_over:      #Pressing arrow doesn't do anything if game is over
		return
	#Dict mapping keys to user_inputs
	dict = {                   
		"Up" : 0,
		"Right" : 1,
		"Down" : 2,
		"Left" : 3
	}
	new_game.next_turn(dict[event.keysym])   #Performs the next turn of the game
	update_board()     #Updates the board
	score_var.set(f"Your Score:\n{new_game.current_score}")  #Updates the score
	highest_score_var.set(f"Highest Score:\n{new_game.highest_score}")   #Updates the highest score
	if new_game.game_over:        #If game is over displays game over message
		messagebox.showinfo("Game Over","Game Over!")

def on_closing():
	'''Activates when window is closed, saves the score and asks for confirmation'''
	if messagebox.askokcancel("Quit", "Do you want to quit?"):  #Exit confirmation
		window.destroy()
	new_game.end_game()   #Saves the highest score
	return

def start_new_game():
	'''Starts a new game'''
	global new_game
	new_game =	game() 
	score_var.set(f"Your Score:\n{new_game.current_score}")     #sets the score labels
	highest_score_var.set(f"Highest Score:\n{new_game.highest_score}")
	update_board()   #updates board

#arrow_press is called if arrow keys are pressed
window.bind("<Up>",arrow_press)
window.bind("<Down>",arrow_press)
window.bind("<Left>",arrow_press)
window.bind("<Right>",arrow_press)

window.protocol("WM_DELETE_WINDOW",on_closing)   #maps on_closing to closing window

start_new_game()
window.mainloop()    
