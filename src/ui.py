import tkinter as tk
from tkinter import messagebox
import game

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


def update_board():
	'''Updates the board'''
	#iterates over whole board
	for i in range(game.board_size):
		for j in range(game.board_size):
			color_background = '#cc66ff'  #Default Color
			if game.board[i][j] in bg_color:
				color_background = bg_color[game.board[i][j]]
			board_var_list[i][j].configure(background=color_background)
			if game.board[i][j] == 0:
				board_var_list[i][j].configure(text='')
			else:
				board_var_list[i][j].configure(text=game.board[i][j])
			

window = tk.Tk()
window.resizable(False,False)

frame_grid = tk.Frame(master=window) #frame for containing the main grid of the game
frame_grid.grid(row=0,column=0) 

frame_side = tk.Frame(master=window,bg='white') #frame for containing side pan
frame_side.grid(row=0,column=1,sticky='nsew')

#creates a 3x3 grid for the game
board_var_list = []   #Stores all the cells
for i in range(game.board_size):
	row = [] 
	for j in range(game.board_size):
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
button_reset_score = tk.Button(master=frame_side,text="Reset Scores") #Button for creating a new game
button_reset_score.pack(side=tk.BOTTOM,padx=5,pady=10)

#Button for restarting the game
button_new_game = tk.Button(master=frame_side,text="New Game") #Button for creating a new game
button_new_game.pack(side=tk.BOTTOM,padx=5,pady=10)

def arrow_press(event):
	'''The functions is activated is an arrow keys is pressed
		and then updates the board'''
	if game.game_over:      #Pressing arrow doesn't do anything if game is over
		return
	global score
	score_var.set(f"Your Score:\n{game.current_score}")  #Updates the score
	highest_score_var.set(f"Highest Score:\n{game.highest_score}")   #Updates the highest score
	#Dict mapping keys to user_inputs
	dict = {                   
		"Up" : 0,
		"Right" : 1,
		"Down" : 2,
		"Left" : 3
	}
	game.next_turn(dict[event.keysym])   #Performs the next turn of the game
	update_board()     #Updates the board
	if game.game_over:        #If game is over displays game over message
		messagebox.showinfo("Game Over","Game Over!")

def on_closing():
	'''Activates when window is closed, saves the score and asks for confirmation'''
	if messagebox.askokcancel("Quit", "Do you want to quit?"):  #Exit confirmation
		window.destroy()
	game.end_game()   #Saves the highest score
	return

#arrow_press is called if arrow keys are pressed
window.bind("<Up>",arrow_press)
window.bind("<Down>",arrow_press)
window.bind("<Left>",arrow_press)
window.bind("<Right>",arrow_press)

game.init_game()       #Initializes the game
score_var.set(f"Your Score:\n{game.current_score}")     #sets the score labels
highest_score_var.set(f"Highest Score:\n{game.highest_score}")
update_board()   #updates board
window.protocol("WM_DELETE_WINDOW",on_closing)   #maps on_closing to closing window
window.mainloop()    
