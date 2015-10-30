from Tkinter import *
import tkFont
import random
import copy
import os
import time
from time import gmtime
from time import strftime
import threading

class Cone():

	def __init__(self, number):

		self.number = number
		self.checkers = 0
		self.enemy = False
		self.selected = False

	def select(self):

		for cone in coneList:
			cone.deselect()

		self.selected = True

	def deselect(self):

		self.selected = False

	def removePiece(self):

		self.checkers-=1

	def addPiece(self):

		self.checkers+=1

class Window(Frame):


	def __init__(self, parent):

		Frame.__init__(self, parent)
		self.parent = parent
		self.parent.title("Backgammon")
		self.pack(fill=BOTH, expand=1)

	def canvas(self):

		global canvas
		global enemyTurnGraphics
		
		canvas = Canvas( self, bg="black", highlightthickness=0)
		canvas.pack(fill=BOTH, expand=1)


		#draw back squares

		canvas.create_rectangle(0,0,238,300, fill="#222222")
		canvas.create_rectangle(646,0,884,300, fill="#222222")



		#dice

		global diceButton; diceButton = Button(self, text="Roll", command= lambda: pressButton())
		diceButton.place(x=100, y=5)

		#draw cones
		for x in range(1,25):

			xpnts = [0 + 32 * x + x * 2, 16 + 32 * x + x * 2, 32 + 32 * x + x * 2]

			conePoints = [xpnts[0], 300, xpnts[1], 150, xpnts[2], 300]

			#normal colors
			if x % 2 == 0:
				color = "#AA0000"
			else:
				color = "#55524F"				

			#Canvas draw cone
			canvas.create_polygon(conePoints, fill=color)

		self.updateCanvas()

	def updateCanvas(self):
		global enemyTurnGraphics
		global diceButton

		for i in deleteInUpdate:
			canvas.delete(i)

		#change button text
		if(turnPhase == 0):
			diceButton["text"] = "roll dice"
		elif(turnPhase >= 5):
			diceButton["text"] = "enemy move"
		else:
			diceButton["text"] = "do random move"
			
		#guide text

		deleteInUpdate.append(canvas.create_text(350, 16, anchor=W, fill="white", text=enemyChat, font=("FixedSys", 15)))

		#Draw checkers
			
		for x in range(0,26):
			try:
				if enemyTurnGraphics == False:
					#normal screen
					xpnts = [0 + 32 * x + x * 2, 32 + 32 * x + x * 2]
				else:
					xpnts = [884 - 32 * x - x * 2 - 2, 852 - 32 * x - x * 2 - 2]

				checkers = coneList[x].checkers

				#color according to player
				if enemyTurnGraphics == False:
					#normal colors
					if coneList[x].enemy == False:
						playerColor = "#FFFFFF"				
					else:
						playerColor = "#FF0000"	
					#selection change color
					if coneList[x].selected == True:
						playerColor = "#999999"
						
				else:
					if coneList[x].enemy == False:
						playerColor = "#FF0000"
					else:
						playerColor = "#FFFFFF"
					#selection change color
					if coneList[x].selected == True:
						playerColor = "#990000"

				counter = 0

				while counter < checkers:
					ypnts = [270 - counter * 30, 300 - counter * 30]		
					#Canvas draw checkers
					deleteInUpdate.append(canvas.create_oval(xpnts[0], ypnts[0], xpnts[1], ypnts[1], fill=playerColor, width = 0))
					counter+=1
			except IndexError:
				pass

		#Do dice values


		color1 = "#FFFFFF"
		color2 = "#FFFFFF"
		color3 = "#FFFFFF"
		color4 = "#FFFFFF"

		for x in xrange (0, len(impossibleMoves), 2):
			if impossibleMoves[x] == 0:
				if impossibleMoves[x + 1] == 0:
					color1 = "#FF0000"
				elif impossibleMoves[x + 1] == 1:
					color1 = "#FFFF00"
				elif impossibleMoves[x + 1] == 2:
					color1 = "#00FF00"

			if impossibleMoves[x] == 1:
				if impossibleMoves[x + 1] == 0:
					color2 = "#FF0000"
				elif impossibleMoves[x + 1] == 1:
					color2 = "#FFFF00"
				elif impossibleMoves[x + 1] == 2:
					color2 = "#00FF00"

			if impossibleMoves[x] == 2:
				if impossibleMoves[x + 1] == 0:
					color3 = "#FF0000"
				elif impossibleMoves[x + 1] == 1:
					color3 = "#FFFF00"
				elif impossibleMoves[x + 1] == 2:
					color3 = "#00FF00"

			if impossibleMoves[x] == 3:

				if impossibleMoves[x + 1] == 0:
					color4 = "#FF0000"
				elif impossibleMoves[x + 1] == 1:
					color4 = "#FFFF00"
				elif impossibleMoves[x + 1] == 2:
					color4 = "#00FF00"


		canvas.create_rectangle(280,5, 305, 30, outline=color1)
		canvas.create_rectangle(310,5, 335, 30, outline=color2)

		diceDotPoints = self.fetchDiceDotPoints(diceValue[0])
		dice2DotPoints = self.fetchDiceDotPoints(diceValue[1])

		for xdot, ydot in zip( diceDotPoints[0::2], diceDotPoints[1::2] ):

			deleteInUpdate.append(canvas.create_oval(xdot + 279, ydot + 4, xdot + 282, ydot + 7, fill=color1))

		for xdot, ydot in zip( dice2DotPoints[0::2], dice2DotPoints[1::2]):

			deleteInUpdate.append(canvas.create_oval(xdot + 309, ydot + 4, xdot + 312, ydot + 7, fill=color2))

		#if double
		if diceValue[2] != 0:

			deleteInUpdate.append(canvas.create_rectangle(280,35, 305, 60, outline=color3))
			

			for xdot, ydot in zip( diceDotPoints[0::2], diceDotPoints[1::2] ):

				deleteInUpdate.append(canvas.create_oval(xdot + 279, ydot + 34, xdot + 282, ydot + 37, fill=color3))


		if diceValue[3] != 0:
		
			deleteInUpdate.append(canvas.create_rectangle(310,35, 335, 60, outline=color4))
			
			for xdot, ydot in zip( dice2DotPoints[0::2], dice2DotPoints[1::2]):

				deleteInUpdate.append(canvas.create_oval(xdot + 309, ydot + 34, xdot + 312, ydot + 37, fill=color4))



	def mousePress(self, event):
		global enemyChat
		global turnPhase

		#bugfix
		if turnPhase == 0 or turnPhase == 5:
			diceButton.place(x=100, y=5)

		#if clicked at cones
		if event.y > 130:
			if turnPhase > 0 and turnPhase < 5:
				click = event.x / 34
				coneClicked = coneList[click]

				if coneClicked.enemy == False:
					coneClicked.select()
					if enemyChat == "hey! Those are mine!":
						enemyChat = "yeah, that's more like it!"
				else:
					enemyChat = "hey! Those are mine!"
			elif turnPhase == 0:
				enemyChat = "roll the dice first!"

			else:
				enemyChat = "dude, It's my turn!"
				
		self.updateCanvas()

	def mouseRelease(self, event):

		if event.y > 130:
			try:
				release = event.x / 34
				coneReleased = coneList[release]
				if turnPhase < 5:
					for cone in coneList:

						if cone.selected == True:

							moveChecker(cone, coneReleased)
							cone.deselect()
			except IndexError:
				pass


		else:
			if turnPhase < 5:
				for cone in coneList:
					cone.deselect()

		self.updateCanvas()


	def fetchDiceDotPoints(self, amount):
		#Fetches the coordinates for all the points in the dice
		if amount == 0:
			#at the start
			dicePoints = [0,-100]
		elif amount == 1:
			dicePoints = [12,12]
		elif amount == 2:
			dicePoints = [6,18,18,6]
		elif amount == 3:
			dicePoints = [6,18,18,6,12,12]
		elif amount == 4:
			dicePoints = [6,6,6,18,18,6,18,18]
		elif amount == 5:
			dicePoints = [6,6,6,18,18,6,18,18,12,12]
		else:
			dicePoints = [6,6,6,18,18,6,18,18,6,12,18,12]

		return dicePoints
		
def pressButton():
	global enemyTurnGraphics
	global totalTurns;
	
	checkWinCondition()

	if(turnPhase == 0):
		reverseGame()
		enemyTurnGraphics = False
		rollDice(True)
		totalTurns+=1
		
	elif(turnPhase < 5):
		executeRandomTurn()
		
	elif(turnPhase == 5):
		reverseGame()
		rollDice(False)
		enemyTurnGraphics = True
		ViktorZeGloriousAI()
		totalTurns+=1
		
	else:
		executeEnemyTurn()
		
def rollDice(playerTurn):
	global turnPhase
	global enemyPhase
	
	if (turnPhase == 0 and playerTurn == True) or (turnPhase == 5 and playerTurn == False):
		
		diceValue[0] = random.randint(1,6)
		diceValue[1] = random.randint(1,6)
		
		#test code here
		#if turnPhase < 5:
		#	diceValue[0] = 1
		#	diceValue[1] = 3
		#if turnPhase >= 5:
		#	diceValue[0] = 1
		#	diceValue[1] = 2
		#diceValue[0] = 1
		#diceValue[1] = 2
		#diceValue[1] = diceValue[0]
			
		del impossibleMoves[:]
		del possibleMoves[:]

		if diceValue[0] == diceValue[1]:
			diceValue[3] = diceValue[0]
			diceValue[2] = diceValue[0]
						
			if playerTurn == True:
				turnPhase = 1
			else:
				turnPhase = 6
				enemyPhase = 0
				
			checkLegalMoves(4)
		else:
			#just bugfixes
			diceValue[2] = 0
			diceValue[3] = 0
			
			if playerTurn == True:
				turnPhase = 3
			else:
				turnPhase = 8
				enemyPhase = 4
				
			checkLegalMoves(2)		

def checkLegalMoves(amount):		
	global turnPhase
	global enemyPhase
	
	imgCones = copy.deepcopy(coneList)
	
	if amount == 2:
	
		#x = dice1
		#y = dice2
		
		x = False
		y = False
		xy = False
		yx = False
	
		#go through moves starting with dice1
		dice1moves = []
		#if there are captured checkers
		if coneList[0].checkers > 0:
			for endingCone in coneList:
				if diceValue[0] == endingCone.number:
					if checkEnemy(endingCone) == True:
						dice1moves = [coneList[0], endingCone]
		else:
			dice1moves = diceLegalMoves(imgCones, 0)
		
		#then go all moves for the 2nd dice after dice 1		
		a = 0
		while a < len(dice1moves):
			x = True
			imgCones[dice1moves[a].number].removePiece()
			imgCones[dice1moves[a + 1].number].addPiece()
			imgCones[dice1moves[a + 1].number].enemy = False
			
			dice2moves = []
			#if there is still checkers captured
			if imgCones[0].checkers > 0:
				for endingCone in imgCones:
					if diceValue[1] == endingCone.number:
						if checkEnemy(endingCone) == True:
							dice2moves = [imgCones[0], endingCone]
			else:
				dice2moves = diceLegalMoves(imgCones, 1)
				
			
			b = 0
			while b < len(dice2moves):
				xy = True
				possibleMoves.extend((0, 0, 0, 0, dice1moves[a], dice1moves[a + 1], dice2moves[b], dice2moves[b + 1]))
				
				b += 2
				
			
			imgCones = copy.deepcopy(coneList)
			a += 2
			
		imgCones = copy.deepcopy(coneList)
		
		#go through moves starting with dice2
		dice2moves = []
		#if there are captured checkers
		if coneList[0].checkers > 0:
			for endingCone in coneList:
				if diceValue[1] == endingCone.number:
					if checkEnemy(endingCone) == True:
						dice2moves = [coneList[0], endingCone]
		else:
			dice2moves = diceLegalMoves(imgCones, 1)
			
		#then go all moves for the 2nd dice after dice 1		
		a = 0
		while a < len(dice2moves):
			y = True
			imgCones[dice2moves[a].number].removePiece()
			imgCones[dice2moves[a + 1].number].addPiece()
			imgCones[dice2moves[a + 1].number].enemy = False
			
			dice1moves = []
			#if there is still checkers captured
			if imgCones[0].checkers > 0:
				for endingCone in imgCones:
					if diceValue[0] == endingCone.number:
						if checkEnemy(endingCone) == True:
							dice1moves = [imgCones[0], endingCone]
			else:
				dice1moves = diceLegalMoves(imgCones, 0)
			
			b = 0
			while b < len(dice1moves):
				yx = True
				possibleMoves.extend((0, 0, 0, 0, dice2moves[a], dice2moves[a + 1], dice1moves[b], dice1moves[b + 1]))
				
				b += 2
				
			
			imgCones = copy.deepcopy(coneList)
			a += 2
			
		#exceptions
		
		if x == False and yx == False:
			#dice 1, 0 moves
			impossibleMoves.extend((0,0))
			turnPhase+=1
			enemyPhase+=2
			
		if x == False and yx == True:
			#dice1, possible moves after y
			impossibleMoves.extend((0,1))
		
		if y == False and xy == False:
			#dice 2, 0 moves
			impossibleMoves.extend((1,0))
			turnPhase+=1
			enemyPhase+=2
			
		if y == False and xy == True:
			#dice2, possible moves after x
			impossibleMoves.extend((1,1))
			
		if x == True and y == False and xy == False:
		
			a = 0
			
			while a < len(dice1moves):
				possibleMoves.extend((0,0,0,0,0,0,dice1moves[a], dice1moves[a + 1]))
				a += 2
	
	
		if y == True and x == False and yx == False:
		
			a = 0
			
			while a < len(dice2moves):
				possibleMoves.extend((0,0,0,0,0,0, dice2moves[a], dice2moves[a + 1]))
				a += 2
			
		if x == True and y == True and xy == False and yx == False:
			
			turnPhase+=1
			enemyPhase+=2
			a = 0
			
			if diceValue[0] > diceValue[1]:
				#dice 2, 0 moves
				impossibleMoves.extend((1,0))
				
				while a < len(dice1moves):
					possibleMoves.extend((0,0,0,0,0,0, dice1moves[a], dice1moves[a + 1]))
					
					a+=2
					
			else:
				#dice 1, 0 moves
				impossibleMoves.extend((0,0))
				while a < len(dice2moves):
					possibleMoves.extend((0,0,0,0,0,0, dice2moves[a], dice2moves[a + 1]))
					
					a+=2
		
		if x == True and xy == True and y == True and yx == False:
			
			#dice 2, can be ruined
			impossibleMoves.extend((1,2))	
		
		if x == True and xy == False and y == True and yx == True:
			
			#dice 2, can be ruined
			impossibleMoves.extend((1,2))
			
	if amount == 4:	
		
		fourDice(imgCones)
			
def fourDice(imgCones):
	global turnPhase
	global enemyPhase
	
	#check how many dices can be used of 4
	#pass as value, don't use global
	
	emptyConeList = copy.deepcopy(coneList)
	for cone in emptyConeList:
		cone.checkers = 0
		
	imgCones = [copy.deepcopy(coneList), copy.deepcopy(emptyConeList), copy.deepcopy(emptyConeList), copy.deepcopy(emptyConeList), copy.deepcopy(emptyConeList)]
	
	possibleMovesTemp = []
	fourDiceRecursion(imgCones, 0, [0] * 8, possibleMovesTemp, emptyConeList)
		
	#check the most moves possible
	zeroCount = 8
	
	#check zeros in the ends
	for route in possibleMovesTemp:
		if route.count(0) < zeroCount:
			zeroCount = route.count(0)
		
	#color dices to red if you can't move all (YAY RED DICES)
	for dice in range (0, zeroCount, 2):
		impossibleMoves.extend((dice / 2, 0))
		turnPhase+=1
		enemyPhase+=2
	
	#change the zeros to other side because the code just works that way and I don't want to rebuild shit
	for route in possibleMovesTemp:
		for x in range(0, route.count(0)):
			route.pop()
			route.insert(0, 0)
	
	
	for route in possibleMovesTemp:
		if route.count(0) == zeroCount:
			possibleMoves.extend(route)
			

		
def fourDiceRecursion(imgCones, recursionAmount, route, possibleMovesTemp, emptyConeList):
	
	#if there are checkers captured
	diceMoves = []
	if imgCones[recursionAmount][0].checkers > 0:
		for endingCone in imgCones[recursionAmount]:
			if diceValue[0] == endingCone.number:
				if checkEnemy(endingCone) == True:
					diceMoves = [imgCones[recursionAmount][0], endingCone]
	else:
		diceMoves = diceLegalMoves(imgCones[recursionAmount], 0)
	
	for move in range(0, len(diceMoves), 2):
		
		#the new imgCones and route shall be copy of the old ones for the recursion
		imgCones[recursionAmount + 1] = copy.deepcopy(imgCones[recursionAmount])
		route = copy.deepcopy(route)
		
		#move the pieces
		for cone in imgCones[recursionAmount + 1]:
			if cone.number == diceMoves[move].number:		
				cone.removePiece()
				route[recursionAmount * 2] = cone
				
			elif cone.number == diceMoves[move + 1].number:
				
				cone.addPiece()
				cone.enemy = False
				route[recursionAmount * 2 + 1] = cone
		
		#as long as the 4 moves aren't full
		if recursionAmount != 3:
			fourDiceRecursion(imgCones, recursionAmount + 1, route, possibleMovesTemp, emptyConeList)
		else:
			#otherwise add the route to possibleMoves
			possibleMovesTemp.append(route)
			
	if len(diceMoves) == 0:	
		possibleMovesTemp.append(route)
	
	
def diceLegalMoves(imgCones, diceNo):
	
	#find legal moves
	startingCones = []
	diceMoves = []

	
	for cone in imgCones:

		if cone.enemy == False:
			if cone.checkers > 0:
				startingCones.append(cone)

					
	for cone1 in startingCones:
		for cone2 in imgCones:
		
			if cone1.number + diceValue[diceNo] == cone2.number:
			
				if checkEnemy(cone2) == True:
				
					diceMoves.extend((cone1, cone2))
	
	return diceMoves;

#Move checkers around
def moveChecker(startingCone, endingCone):
	global turnPhase
	global enemyChat
	global enemyTurnGraphics
			
	if checkObvious(startingCone, endingCone) == True or turnPhase >= 5:
		
		#Enemy move
		if turnPhase >= 5:
			
			lineSaid = False
			startingCone.removePiece()

			
			if endingCone.number != 25:
				#Enemy eats
				if endingCone.enemy == True and endingCone.checkers == 1:
					eatEnemy(endingCone)
					line = random.randint(1,5)
					if line == 1:
						enemyChat = "Gotcha!"
					elif line == 2:
						enemyChat = "OMNOMNOM!"
					elif line == 3:
						enemyChat = "Delicious!"
					elif line == 4:
						enemyChat = "That tasted good"
					elif line == 5:
						enemyChat = "Didn't see that one coming huh?"
					lineSaid = True
				
				
				endingCone.addPiece()
				endingCone.enemy = False
				
			turnPhase += 1
			
			if turnPhase == 10:
				turnPhase = 0
				
			if endingCone.number - startingCone.number == diceValue[3]:
				diceValue[3] = 0

			elif endingCone.number - startingCone.number == diceValue[2]:
				diceValue[2] = 0
				
			elif endingCone.number - startingCone.number == diceValue[1]:
				diceValue[1] = 0

			elif endingCone.number - startingCone.number == diceValue[0]:
				diceValue[0] = 0
				
			if lineSaid == False:
				line = random.randint(1,5)
				if line == 1:
					enemyChat = "Check this out"
				elif line == 2:
					enemyChat = "I will annihilate you..."
				elif line == 3:
					enemyChat = "You are no match"
				elif line == 4:
					enemyChat = "I shall be viktorious. Get it?"
				elif line == 5:
					enemyChat = "Watch out for me"
				elif line == 6:
					enemyChat = "This is going to be easy"
				elif line == 7:
					enemyChat = "Watch me"
				elif line == 8:
					enemyChat = "Look how it's done"
				elif line == 9:
					enemyChat = "Are you sure you can handle this?"
				elif line == 10:
					enemyChat = "Behold my true power!"
				elif line == 11:
					enemyChat = "This is how a real player moves!"
		
		#Player move
		else:
			a = 0
			while a < len(possibleMoves):
				try:
					if (
						startingCone.number == possibleMoves[a + (turnPhase - 1) * 2].number and 
						endingCone.number == possibleMoves[a + (turnPhase - 1) * 2 + 1].number
						):
						#Move is legal
						lineSaid = False
						startingCone.removePiece()
						
						if endingCone.number != 25:	
							if endingCone.enemy == True and endingCone.checkers == 1:
				
								#Player eats
								eatEnemy(endingCone)
								line = random.randint(1,5)
								if line == 1:
									enemyChat = "No! What have you done!?"
								elif line == 2:
									enemyChat = "NOO! SASHA! anyone but you!"
								elif line == 3:
									enemyChat = "Why you..."
								elif line == 4:
									enemyChat = "Hmph. This won't end here"
								elif line == 5:
									enemyChat = "Playing tough?"
								lineSaid = True
					

							endingCone.addPiece()
							endingCone.enemy = False
						
						turnPhase+=1;				
						
						#check which dice to reset
						if endingCone.number - startingCone.number == diceValue[3]:
							diceValue[3] = 0

						elif endingCone.number - startingCone.number == diceValue[2]:
							diceValue[2] = 0
							
						elif endingCone.number - startingCone.number == diceValue[1]:
							diceValue[1] = 0

						elif endingCone.number - startingCone.number == diceValue[0]:
							diceValue[0] = 0
																	
						if lineSaid == False:
							line = random.randint(1,5)
							if line == 1:
								enemyChat = "hmm... Interesting..."
							elif line == 2:
								enemyChat = "nice move..."
							elif line == 3:
								enemyChat = "aha..."
							elif line == 4:
								enemyChat = "you are making this far too easy..."
							elif line == 5:
								enemyChat = "best you can do?"
							elif line == 6:
								enemyChat = "Ha! Wrong move comrade"
							elif line == 7:
								enemyChat = "have you even played this game before?"
							elif line == 8:
								enemyChat = "nice move... not"
							elif line == 9:
								enemyChat = "did you even think that move through?"
							elif line == 10:
								enemyChat = "oh I see, next level tactics."
							elif line == 11:
								enemyChat = "maybe you should learn to play first."
								
						break
				except AttributeError:
					pass
				except IndexError:
					pass
				a+=8
	#move random move button out of screen so it can't be pressed
	global diceButton; 
	
	if testModeOn == False:
		if turnPhase < 5 and turnPhase != 0:
			diceButton.place(x=100, y=-100)
		else:
			diceButton.place(x=100, y=5)
		

def checkObvious(startingCone,endingCone):
	global enemyChat

	b = endingCone.number
	a = startingCone.number
	
	if b == a:
		enemyChat = "move the checker by dragging it"
		return False
	elif b < a:
		enemyChat = "wrong direction comrade!"
		return False
	elif b - a != diceValue[0] and b - a != diceValue[1]:
		enemyChat = "are you sure you can count?"
		return False

	elif checkEnemy(endingCone) == False:
		enemyChat = "nu-uh, got over 2 units on that one"
		return False
		
	elif coneList[0].checkers > 0 and startingCone.number != 0:
		enemyChat = "don't you have a captured checker?"
		return False	

	else:
		return True

def checkWinCondition():
	global enemyChat
	global turnPhase
	
	playerEmpty = True
	enemyEmpty = True
	
	for cone in coneList:
		if cone.enemy == False:
			if cone.checkers > 0:
				playerEmpty = False
		else:
			if cone.checkers > 0:
				enemyEmpty = False
				
	if playerEmpty == True or enemyEmpty == True:
		#quit the gui
		global gameEnded
		global testModeOn
		
		if testModeOn == True:
			global enemyWins
			global playerWins
		
		
		if testModeOn == False:
			global root
			root.destroy()
		
		gameEnded = True
		
		
		if turnPhase < 6 and turnPhase != 0:
			
			if testModeOn == False:
				print "\n\n Viktor: Well well, congratulations... You won\n "
				
			else:
				playerWins += 1
				print "\r games simulated: %s" % (playerWins + enemyWins),
				sys.stdout.flush(),
				
		else:
			if testModeOn == False:
				print "\n\n Viktor: Easy game, I win\n "
			else:
				enemyWins += 1
				print "\r games simulated: %s" % (playerWins + enemyWins),
				sys.stdout.flush()

		#write statistics

		line = ""
		
		#add day and time
		
		line += strftime("%d.%m.%y %H:%M -- ", gmtime())
		
		#add winner name
		
		if turnPhase < 6 and turnPhase != 0:
			line += "Player"
		else:
			line += "Viktor"
		
		#add game length
		
		global totalTurns
		global startTime
		gameLengthTime = time.time() - startTime
		gameLengthMinutes = int(gameLengthTime / 60)
		gameLengthSeconds = gameLengthTime % 60
		
		#Formating
		seconds = "%.0f" % (gameLengthSeconds)
		if gameLengthSeconds < 10:
			seconds = "0" + str(seconds)
		
		
		line += " -- length: time %s:%s, turns %s. " % (gameLengthMinutes, seconds, totalTurns)
	
		#and \n
		
		line += "\n"
		
			
		#start opening file
		pyfilepath = os.path.dirname(__file__)
		txtfilepath = "statistics.txt"
		completepath = os.path.join(pyfilepath, txtfilepath)
		
		#Hopefully this works if you are not using Windows.
		#if it doesn't work on linux uncomment the line down below
		#completepath = "(write some path here)"
		
		#creates file if it doesn't exist and starts appending
		with open(completepath, 'a') as statistics:
			statistics.write(line)
		#opens it and reads it
		
		if testModeOn == False:
			mainMenu()
			
def checkEnemy(cone):
	#Returns True if valid move
	if cone.enemy == True:
		#check if you can home checkers
		if cone.number == 25:
			for cone in coneList[0:19]:
				if cone.enemy == False and cone.checkers > 0:
					return False
					
			return True
			
		
		if cone.checkers == 0:
			return True

		if cone.checkers == 1:
			return True

		if cone.checkers > 1:
			return False
	else:
		return True

def eatEnemy(cone):
	cone.enemy = False
	cone.checkers-=1
	coneList[25].checkers+=1

def reverseGame():
	
	#save cone owners
	coneOwners = []
	for cone in coneList:
		if cone.enemy == True:
			coneOwners.append(False)
		else:
			coneOwners.append(True)
			
	#save checkers amounts
	checkerAmounts = []
	
	for cone in coneList:
		checkerAmounts.append(cone.checkers)
	
	#deposit checker amounts and cone owners
	for i in range(0, len(coneList)):
		coneList[i].checkers = checkerAmounts[len(checkerAmounts) - 1 - i]
		coneList[i].enemy = coneOwners[len(coneOwners) - 1 - i]
		
def executeEnemyTurn():
	global turnPhase
	global enemyPhase
	global bestRoute
		
	try:
		#select cone
		if enemyPhase % 2 == 0:
			for cone in coneList:
				if cone.number == bestRoute[enemyPhase].number:
					cone.select()
					
		else:
			for cone1 in coneList:
				for cone2 in coneList:
					if cone1.number == bestRoute[enemyPhase - 1].number and cone2.number == bestRoute[enemyPhase].number:
						moveChecker(cone1, cone2)
			for cone in coneList:
				cone.deselect()
		
		enemyPhase += 1
	except (TypeError, IndexError) as e:
		turnPhase = 0
	
def executeRandomTurn():
	global turnPhase
	
	if len(possibleMoves) > 0:
		randomNumber = random.randint(0, len(possibleMoves) - 1) / 8
			
		randomRoute = possibleMoves[(randomNumber * 8):(randomNumber * 8 + 8)]
		
				
		for i in range(0, len(randomRoute), 2):
			if randomRoute[i] != 0:
				for cone1 in coneList:
					for cone2 in coneList:
						if cone1.number == randomRoute[i].number and cone2.number == randomRoute[i + 1].number:
							moveChecker(cone1, cone2)
	
	turnPhase = 5


def ViktorZeGloriousAI():
	#gets the best route
	global bestRoute
	global turnPhase
	
	routes = []
	
	#do lists of all possible routes
	for i in range(0, len(possibleMoves), 8):
		routes.append(possibleMoves[i:i+8])
		
	
	#calculate the next move for motherland
	#points for each move
	bestRoute = calculateBestRoute(routes)
	
	if bestRoute == None:
		turnPhase = 0
	
def calculateBestRoute(routes):	
	
	#5 points for eating enemy
	#2 points for getting to friendly cone
	#-2 points for each second 1 checker cone
	#do also thing with how many enemies are in next 6 squares
	#find move with best score
	
	scores = []
	for route in routes:
		#calculates the scores
		score = calculateScoreRecursion(route, copy.deepcopy(coneList), 0, 0)
		scores.append(score)
	try:
		largestScore = max(scores)
		largestScoreIndex = scores.index(largestScore)
		return routes[largestScoreIndex]
		
	except ValueError:
		pass
				
def calculateScoreRecursion(route, imgCones, recursionAmount, score):
	#takes 8 value score
	#if all values went through
	if recursionAmount == 8:
		return score		
	
	else:
	
		#if there is no move (2 moves instead of 4 etc)
		if route[recursionAmount] == 0:
			pass
		else:
			#check what cone is it that you move to
			for cone in imgCones:
				if route[recursionAmount + 1].number == cone.number:
					#if you can eat enemy the score depends on distance
					if cone.enemy == True and cone.checkers == 1:
						score+=20
						scoreBonus = (25 - cone.number) * 5
						score+=scoreBonus
					#if you can home a checker DO IT!
					if cone.number == 25:
						score+=1000
					#if the ending position has a friend
					elif cone.enemy == False and cone.checkers > 0:
						score+=20
						#if you even secure another checker in process!
						if cone.checkers == 1:
							score += 20
					#if the ending position doesn't have a friend check how close enemies are
					else:
						for cone1 in coneList:
							if cone1.enemy == True and cone.checkers > 0:
								if abs(cone.number - cone1.number) < 6:
									score -= 3
								elif abs(cone.number - cone1.number) < 12:
									score -= 1
				
				if route[recursionAmount].number == cone.number:
					
					#if you leave a checker vulnerable, check also how close enemies are
					if cone.checkers == 2:
						for cone1 in coneList:
							if cone1.enemy == True and cone.checkers > 0:
								if abs(cone.number - cone1.number) < 6:
									score -= 10
								elif abs(cone.number - cone1.number) < 12:
									score -= 3
						score -= 30
						
					#if you move from a position in your home field
					if cone.number > 19 and cone.checkers > 1:
						score -= 50
						
			#this turns scores are count, move to next turn
			for cone in imgCones:
				if cone.number == route[recursionAmount].number:		
					cone.removePiece()
						
				elif cone.number == route[recursionAmount + 1].number:
						
					cone.addPiece()
					cone.enemy = False

		return calculateScoreRecursion(route, imgCones, recursionAmount + 2, score)
	

def initializeGame():	

	#Globals
	global coneList
	coneList = []
	global diceValue
	diceValue = [0,0,0,0]
	global deleteInUpdate
	deleteInUpdate = []

	#player 1: 0 -> roll dice -> 
	# ( 1 -> move -> 2 -> move ->) 3 -> move -> 4 -> move -> 5
	# 5-10 for enemy
	global turnPhase
	turnPhase = 0
	global enemyPhase
	enemyPhase = 0
	global bestRoute
	bestRoute = []
	global possibleMoves
	possibleMoves = []
	global enemyTurnGraphics
	enemyTurnGraphics = False

	#for gamelog
	global totalTurns
	totalTurns = 0
	global startTime
	startTime = time.time()

	#array: dice no, reason: 0 no possible moves (red), 1 only possible if moved certainly (yellow), 2 only possible if not moved (green), 3 always possible (white)
	global impossibleMoves
	impossibleMoves = []


	for x in range (0, 26):

		cone = Cone(x)

		#starting setup

		if x == 0:
			cone.enemy = False	
		elif x == 1:
			cone.checkers+=2
			cone.enemy = False
		elif x == 6:
			cone.checkers+=5
			cone.enemy = True
		elif x == 8:
			cone.checkers+=3
			cone.enemy = True		
		elif x == 12:
			cone.checkers+=5
			cone.enemy = False
		elif x == 13:
			cone.checkers+=5
			cone.enemy = True
		elif x == 17:
			cone.checkers+=3
			cone.enemy = False
		elif x == 19:
			cone.checkers+=5
			cone.enemy = False
		elif x == 24:
			cone.checkers+=2
			cone.enemy = True
		elif x == 25:
			cone.enemy = True
		

		coneList.append(cone)
		
	global enemyChat; enemyChat = "Hello, I'm Viktor, Nice to meet you"
	global gameEnded; gameEnded = False
		
	reverseGame()


def mainMenu():
	#Menu
	
	global testModeOn

	while True:
	
		"\n\n Welcome to Backgammon by Peetu Nuottajarvi \n"
		print " What do you want to do? \n"
		print " P - Play \n"
		print " S - Statistics \n"
		print " T - Test AI against Random \n"
		print " Q - Quit \n"
		playerInput = raw_input(" ")
		
		if playerInput.upper() == "Q" or playerInput.upper() == "QUIT":
			sys.exit()
			break
		
		if playerInput.upper()  == "P" or playerInput.upper() == "PLAY":
			
			testModeOn = False
			initializeGame()
			startTkinter()		

		if playerInput.upper() == "T" or playerInput.upper() == "TEST AI":
			global gameEnded
			
			while True:
			
				numberInput = raw_input("\n Give amount of games to simulate: ")
				
				try:
					numberInput = int(numberInput)
					break
				except ValueError:
					pass
			
			a = 0
			
			global playerWins
			playerWins = 0
			global enemyWins
			enemyWins = 0
			
			while a < numberInput:
			
				testModeOn = True
				initializeGame()
							
				while gameEnded == False:
					pressButton()
			
				a+=1
				
			print "\n Player won: %s (%.2f%%)" % (playerWins, float(playerWins) / (playerWins + enemyWins) * 100)
			print " AI won: %s (%.2f%%)" % (enemyWins, float(enemyWins) / (playerWins + enemyWins) * 100)
	
			
		if playerInput.upper()  == "S" or playerInput.upper() == "STATISTICS":
			#open statistics

			pyfilepath = os.path.dirname(__file__)
			txtfilepath = "statistics.txt"
			completepath = os.path.join(pyfilepath, txtfilepath)
			
			#Hopefully this works if you are not using Windows.
			#if it doesn't work on linux uncomment the line down below
			#completepath = "(write some path here)"
			
			#creates file if it doesn't exist
			open(completepath, "a")
			
			
			#opens it and reads it
			with open(completepath, 'r') as statistics:
				data = statistics.read()
			
			print "\n\n"
			if len(data) == 0:
				print " - no data - "
			print data
			
			print "\n\n Do you wish to reset the game log?"
			playerInput = raw_input(' write "RESET" to reset the database, anything else to not\n ')
			
			while True:
				if playerInput.upper() == "RESET" or playerInput.upper() == '"RESET"':
					open(completepath, "w")
					print " reset succesfull"
					mainMenu()
				else:
					mainMenu()
def startTkinter():

	global root
	root = Tk()
	root.geometry("884x300")
	root.resizable(width=FALSE, height=FALSE)

	#Create object Window(Frame)
	gui = Window(root)
	#onClickListener and Canvas on our Frame
	root.bind("<Button-1>", gui.mousePress)
	root.bind("<ButtonRelease-1>", gui.mouseRelease)
	gui.canvas()
	root.mainloop()

mainMenu()
