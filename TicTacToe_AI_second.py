import numpy as np
import random as rd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from keras.models import load_model

# Set FrontEnd style
root = Tk()
root.title("TicTacToe - Artificial Neural Network")
root.configure(background='lightgrey')
style = ttk.Style()
style.theme_use("classic")

# ------------------------------------ Model ------------------------------------------

def gameStart():
    
    global aiStep, playerStep, singleGameStep, AI_model
    aiStep = [] # AI selected
    playerStep = [] # Player selected
    
    # Record single game
    singleGameStep = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype = int)
    
    # Load AI model
    AI_model = load_model('Player2_Model_Binary.h5')
    
    global bu1, bu2, bu3, bu4, bu5, bu6, bu7, bu8, bu9, la1
    # Add Buttons
    bu1 = ttk.Button(root, text = " ")
    bu1.grid(row=0, column=0, sticky="snew", ipadx=40, ipady=40)
    bu1.config(command=lambda: buttonClick(1))
    
    bu2 = ttk.Button(root, text = " ")
    bu2.grid(row=0, column=1, sticky="snew", ipadx=40, ipady=40)
    bu2.config(command=lambda: buttonClick(2))
    
    bu3 = ttk.Button(root, text = " ")
    bu3.grid(row=0, column=2, sticky="snew", ipadx=40, ipady=40)
    bu3.config(command=lambda: buttonClick(3))
    
    bu4 = ttk.Button(root, text = " ")
    bu4.grid(row=1, column=0, sticky="snew", ipadx=40, ipady=40)
    bu4.config(command=lambda: buttonClick(4))
    
    bu5 = ttk.Button(root, text = " ")
    bu5.grid(row=1, column=1, sticky="snew", ipadx=40, ipady=40)
    bu5.config(command=lambda: buttonClick(5))
    
    bu6 = ttk.Button(root, text = " ")
    bu6.grid(row=1, column=2, sticky="snew", ipadx=40, ipady=40)
    bu6.config(command=lambda: buttonClick(6))
    
    bu7 = ttk.Button(root, text = " ")
    bu7.grid(row=2, column=0, sticky="snew", ipadx=40, ipady=40)
    bu7.config(command=lambda: buttonClick(7))
    
    bu8 = ttk.Button(root, text = " ")
    bu8.grid(row=2, column=1, sticky="snew", ipadx=40, ipady=40)
    bu8.config(command=lambda: buttonClick(8))
    
    bu9 = ttk.Button(root, text = " ")
    bu9.grid(row=2, column=2, sticky="snew", ipadx=40, ipady=40)
    bu9.config(command=lambda: buttonClick(9))
    
    buRestart = ttk.Button(root, text = "Restart")
    buRestart.grid(row=3, column=4, sticky="snew", ipadx=30, ipady=5)
    buRestart.config(command=lambda: gameStart())
    
    # Add Labels
    la1 = ttk.Label(root, text = " ")
    la1.grid(row=0, column=4, sticky="snew", rowspan=3)

# ------------------------------------ Controls -----------------------------------------

# Return highest win rate and position
def modelPrediction():
    
    max_aiPrediction = 0 # max win rate
    aiPrediction = 0 
    best_position = 0
        
    for i in range(9):
            
        if singleGameStep[0, i] == 0:
            singleGameStep[0, i] = 1
            aiPrediction = AI_model.predict(singleGameStep)
            # Find best step
            if aiPrediction > max_aiPrediction:
                max_aiPrediction = aiPrediction
                best_position = i
            singleGameStep[0, i] = 0
                
    return max_aiPrediction, best_position

# AI turn with predict position
def aiTurn():
    
    aiPrediction, bestPosition = modelPrediction()
    setLayout(bestPosition + 1, "X")
    # record the move
    aiStep.append(bestPosition + 1)
    singleGameStep[0, bestPosition] = 1
    la1.config(text="---------- Game Data ---------- \nAI = {}\nPlayer = {}\nAI_predict = {:1.3f}  ".format(aiStep, playerStep, aiPrediction[0, 0]))
    checkWin()
    
# Press Buttons
def buttonClick(id):

    setLayout(id, "O")
    playerStep.append(id)
    singleGameStep[0, id - 1] = -1
    if checkWin() == 0:
        aiTurn()

def checkWin():
    
    win = 0
    # Check if player 1 win
    if (1 in aiStep) and (2 in aiStep) and (3 in aiStep):
        win = 1
    elif (4 in aiStep) and (5 in aiStep) and (6 in aiStep):
        win = 1
    elif (7 in aiStep) and (8 in aiStep) and (9 in aiStep):
        win = 1
    elif (1 in aiStep) and (4 in aiStep) and (7 in aiStep):
        win = 1
    elif (2 in aiStep) and (5 in aiStep) and (8 in aiStep):
        win = 1
    elif (3 in aiStep) and (6 in aiStep) and (9 in aiStep):
        win = 1
    elif (1 in aiStep) and (5 in aiStep) and (9 in aiStep):
        win = 1
    elif (3 in aiStep) and (5 in aiStep) and (7 in aiStep):
        win = 1

        # Check if player 2 win
    elif (1 in playerStep) and (2 in playerStep) and (3 in playerStep):
        win = 2
    elif (4 in playerStep) and (5 in playerStep) and (6 in playerStep):
        win = 2
    elif (7 in playerStep) and (8 in playerStep) and (9 in playerStep):
        win = 2
    elif (1 in playerStep) and (4 in playerStep) and (7 in playerStep):
        win = 2
    elif (2 in playerStep) and (5 in playerStep) and (8 in playerStep):
        win = 2
    elif (3 in playerStep) and (6 in playerStep) and (9 in playerStep):
        win = 2
    elif (1 in playerStep) and (5 in playerStep) and (9 in playerStep):
        win = 2
    elif (3 in playerStep) and (5 in playerStep) and (7 in playerStep):
        win = 2
    elif ((len(aiStep) + len(playerStep)) == 9) and (win == 0):
        win = 3

    if win == 1:
        messagebox.showinfo(title="GameOver!", message="AI is the winner!\nPress 'OK' to restart")
        gameStart()
    elif win == 2:
        messagebox.showinfo(title="Congrat!", message="Player is the winner!\nPress 'OK' to restart")
        gameStart()
    elif win == 3:
        messagebox.showinfo(title="Try again.", message="Draw!\nPress 'OK' to restart")
        gameStart()
        
    return win

# ------------------------------------- Views -------------------------------------------

# Show Symbols
def setLayout(id, playerSymbol):
    if id == 1:
        bu1.config(text=playerSymbol)
        bu1.state(['disabled'])
    elif (id == 2):
        bu2.config(text=playerSymbol)
        bu2.state(['disabled'])
    elif id == 3:
        bu3.config(text=playerSymbol)
        bu3.state(['disabled'])
    elif id == 4:
        bu4.config(text=playerSymbol)
        bu4.state(['disabled'])
    elif id == 5:
        bu5.config(text=playerSymbol)
        bu5.state(['disabled'])
    elif id == 6:
        bu6.config(text=playerSymbol)
        bu6.state(['disabled'])
    elif id == 7:
        bu7.config(text=playerSymbol)
        bu7.state(['disabled'])
    elif id == 8:
        bu8.config(text=playerSymbol)
        bu8.state(['disabled'])
    elif id == 9:
        bu9.config(text=playerSymbol)
        bu9.state(['disabled'])

# ----------------- Execute ------------------
gameStart()
root.mainloop()