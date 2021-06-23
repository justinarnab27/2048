import tkinter as tk
from tkinter import messagebox
import game

#####################################################
#The variables here should be imported from other files
highest_score = game.get_highest_score()
 

##########################################################################################################
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
	for i in range(game.board_size):
		for j in range(game.board_size):
			color_background = '#cc66ff'
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

frame_side = tk.Frame(master=window) #frame for containing side pan
frame_side.grid(row=0,column=1,sticky='nsew')

#board_var_list = []
#for i in range(game.board_size):
#	row = []
#	for j in range(game.board_size):
#		board_var = tk.StringVar()
#		row.append(board_var)
#	board_var_list.append(row)

#update_board()

#creates a 3x3 grid for the game
board_var_list = []
for i in range(game.board_size):
	row = [] 
	for j in range(game.board_size):
		box = tk.Label(master=frame_grid,width=4,height=2,borderwidth=3,relief=tk.RIDGE,font=("Arial",35))
		row.append(box)
		box.grid(row=i,column=j)
	board_var_list.append(row)

score_var = tk.StringVar()
score_var.set(f"Your Score:\n\n{game.current_score}")

label_your_score = tk.Label(master=frame_side,textvariable=score_var)  #Label showing the users current score
label_your_score.pack(pady=10,padx=5)

label_highest_score = tk.Label(master=frame_side,text=f"Highest Score:\n\n{highest_score}") #Label showing the users highest score
label_highest_score.pack(padx=5)

button_new_game = tk.Button(master=frame_side,text="New Game") #Button for creating a new game
button_new_game.pack(side=tk.BOTTOM,padx=5,pady=10)

def arrow_press(event):
	if game.game_over:
		print("GG")
		return
	global score
	#score = 30
	score_var.set(f"Your Score:\n\n{game.current_score}")
	dict = {
		"Up" : 0,
		"Right" : 1,
		"Down" : 2,
		"Left" : 3
	}
	game.next_turn(dict[event.keysym])
	update_board()
	print(id(game.game_over))
	if game.game_over:
		messagebox.showinfo("Game Over","Game Over!")
	#print(dict[event.keysym])

window.bind("<Up>",arrow_press)
window.bind("<Down>",arrow_press)
window.bind("<Left>",arrow_press)
window.bind("<Right>",arrow_press)

game.init_game()
update_board()
window.mainloop()
