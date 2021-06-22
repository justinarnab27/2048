import tkinter as tk

#####################################################
#The variables here should be imported from other files
score = 0
highest_score = 0


##########################################################################################################


window = tk.Tk()
window.resizable(False,False)

frame_grid = tk.Frame(master=window) #frame for containing the main grid of the game
frame_grid.grid(row=0,column=0) 

frame_side = tk.Frame(master=window) #frame for containing side pan
frame_side.grid(row=0,column=1,sticky='nsew')

#creates a 3x3 grid for the game
for i in range(3):
	for j in range(3):
		box = tk.Label(master=frame_grid,width=15,height=10,borderwidth=3,relief=tk.RIDGE)
		box.grid(row=i,column=j)

label_your_score = tk.Label(master=frame_side,text=f"Your Score: {score}")  #Label showing the users current score
label_your_score.pack(pady=10,padx=5)

label_highest_score = tk.Label(master=frame_side,text=f"Highest Score: {highest_score}") #Label showing the users highest score
label_highest_score.pack(padx=5)

button_new_game = tk.Button(master=frame_side,text="New Game") #Button for creating a new game
button_new_game.pack(side=tk.BOTTOM,padx=5,pady=10)


window.mainloop()