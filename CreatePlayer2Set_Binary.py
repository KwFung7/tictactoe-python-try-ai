#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 04:27:18 2017

@author: KwFung
"""

import numpy as np
import random

class createSet:
    
    def __init__(self):
        
        # Dataset records all possible states in all game -> training set
        self.__allPossibleStates = np.array([[]], dtype = int)
        # Record all game result
        self.__allP1 = []
        self.__allP2 = []
        self.__gameResult = []
        
    def runRandomGame(self):
        
        # checkWin: (win = 1) player 1 win, 
        #(win = 2) player 2 win, (win = 3) Draw
        def checkWin():
        
            win = 0
            # Check if player 1 win
            if (1 in p1) and (2 in p1) and (3 in p1):
                win = 1
            elif (4 in p1) and (5 in p1) and (6 in p1):
                win = 1
            elif (7 in p1) and (8 in p1) and (9 in p1):
                win = 1
            elif (1 in p1) and (4 in p1) and (7 in p1):
                win = 1
            elif (2 in p1) and (5 in p1) and (8 in p1):
                win = 1
            elif (3 in p1) and (6 in p1) and (9 in p1):
                win = 1
            elif (1 in p1) and (5 in p1) and (9 in p1):
                win = 1
            elif (3 in p1) and (5 in p1) and (7 in p1):
                win = 1
        
                # Check if player 2 win
            elif (1 in p2) and (2 in p2) and (3 in p2):
                win = 2
            elif (4 in p2) and (5 in p2) and (6 in p2):
                win = 2
            elif (7 in p2) and (8 in p2) and (9 in p2):
                win = 2
            elif (1 in p2) and (4 in p2) and (7 in p2):
                win = 2
            elif (2 in p2) and (5 in p2) and (8 in p2):
                win = 2
            elif (3 in p2) and (6 in p2) and (9 in p2):
                win = 2
            elif (1 in p2) and (5 in p2) and (9 in p2):
                win = 2
            elif (3 in p2) and (5 in p2) and (7 in p2):
                win = 2
            elif ((len(p1) + len(p2)) == 9) and (win == 0):
                win = 3
                
            return win
        
        def recordResult(winner):
            
            # Record the result
            self.__allP1.append(p1)
            self.__allP2.append(p2)
            self.__gameResult.append(1 if winner == 1 else 0)
            
            # Put into training set
            if (n == 0):
                self.__allPossibleStates = np.append(self.__allPossibleStates, singleGameStates)                
            else:
                # Each step/states in this game put into training set separately
                self.__allPossibleStates = np.vstack((self.__allPossibleStates, singleGameStates))
            
            for j in range(len(p1)):
                # Replay and record the game backward
                if winner == 1:
                    singleGameStates[(p1[len(p1) - j - 1]) - 1] = 0
                else:
                    singleGameStates[(p2[len(p2) - j - 1]) - 1] = 0
                self.__allPossibleStates = np.vstack((self.__allPossibleStates, singleGameStates))
                self.__allP1.append(p1)
                self.__allP2.append(p2)
                self.__gameResult.append(1 if winner == 1 else 0)
                    
                if (j != (len(p1) - 1)) or (winner != 1):
                    if winner == 1:
                        singleGameStates[(p2[len(p2) - j - 1]) - 1] = 0
                    else:
                        singleGameStates[(p1[len(p1) - j - 1]) - 1] = 0
                    self.__allPossibleStates = np.vstack((self.__allPossibleStates, singleGameStates))
                    self.__allP1.append(p1)
                    self.__allP2.append(p2)
                    self.__gameResult.append(1 if winner == 1 else 0)
            
        '''        
        def pValueCalculate ():
            
            # Calculate the pValue of all state in this game
            # Default pValue is 0.5
            previous = 0.5
            # Search any identical state, if true then take the exist pValue
            for k in range(len(self.__allPossibleStates) - 1):
                if (np.array_equal(self.__allPossibleStates[k], singleGameStates)):
                    previous = self.__pValue[k]
            current = self.__pValue[-2]
            calculation = previous + (0.5 * (current - previous))
            self.__pValue.append(calculation)
        '''
            
        for n in range(1500):
        
            # For recording states in single game, index 1 - 9 for position, 
            # 1 -> Cross, -1 -> Circle, 0 -> empty
            singleGameStates = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            # Record player 1, 2 move
            p1 = []
            p2 = []
            # Gameover or not
            gameOver = 0
            
            # Step 1 - 9
            for i in range(0, 9):
                
                if gameOver == 0:
                    # Random position 1 - 9
                    randomPosition = random.randrange(1, 10)
                    # While the position already occupied, generate new position again
                    while singleGameStates[randomPosition - 1] != 0:
                        randomPosition = random.randrange(1, 10)
                    # Record new random step
                    if i % 2 == 0:
                        p2.append(randomPosition)
                        singleGameStates[randomPosition - 1] = -1
                    else:
                        p1.append(randomPosition)
                        singleGameStates[randomPosition - 1] = 1
                    # if win then gameover
                    if (checkWin() == 1) or (checkWin() == 2):
                        gameOver = 1
            
            # Check any similar game
            if checkWin() == 3:
                pass
            elif (p1 in self.__allP1) and (p2 in self.__allP2):
                if (self.__allP1.index(p1) == self.__allP2.index(p2)):
                    pass
                else:
                    recordResult(checkWin())
            else:
                recordResult(checkWin())
        
        return self.__allPossibleStates, self.__gameResult, self.__allP1, self.__allP2
    