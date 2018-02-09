import pygame
from math import pi
import random
import shelve

#classes
class ArcCircle:
	def __init__(self, numberOfPins, numberOfArcs, color1, color2, areaForCircle, pins):
		self.numberOfPins = numberOfPins
		self.numberOfArcs = numberOfArcs
		self.color1 = color1
		self.color2 = color2
		self.areaForCircle = areaForCircle
		self.pins = pins

#Methods
def createRandomPins(numberOfPins, numberOfArcs):
	randomNumber = random.randint(0, numberOfArcs)
	pins = []
	for i in range(numberOfPins):
		pins.append((randomNumber + i) % numberOfArcs)
	return pins

def drawPinnedCircle(numberOfPins, numberOfArcs, color1, color2, areaForCircle, pins):
	global pi
	if not pins:
		pins = createRandomPins(numberOfPins, numberOfArcs)
	startingRadian = 0
	endingRadian = 2*pi/numberOfArcs
	for i in range(numberOfArcs):
		if i in pins:
			pygame.draw.arc(screen, color1, areaForCircle, startingRadian, endingRadian, arcWidth)
		else:
			pygame.draw.arc(screen, color2, areaForCircle, startingRadian, endingRadian, arcWidth)
		startingRadian = endingRadian
		endingRadian += 2*pi/numberOfArcs
	return ArcCircle(numberOfPins, numberOfArcs, color1, color2, areaForCircle, pins)

def getScoreMissedPinsAndMultiplier(circlePinValue, circleNonPinValue, movements, circlePins, numberOfArcs, comboMultiplier, rotations):
	print movements
	if (movements) == circlePins[0]:
		missedPin = False
		comboMultiplier += 1
		if rotations > 2:
			thisCircleScore = comboMultiplier * (int(circlePinValue * (.95 ** (rotations - 2))))
		else:
			thisCircleScore = comboMultiplier * circlePinValue
	else:
		missedPin = True
		comboMultiplier = 1
		if rotations > 2:
			thisCircleScore = int(circleNonPinValue * (.95 ** (rotations - 2)) * (.95 ** (abs(movements - 1 - circlePins[0]))))
		else:
			thisCircleScore = int(circleNonPinValue * (.95 ** (abs(movements - 1 - circlePins[0]))))
	return thisCircleScore, missedPin, comboMultiplier

pygame.init()
pygame.display.set_caption("arcSpin")
size = (960, 640)
screen = pygame.display.set_mode(size)
frame = pygame.time.Clock()
mainMenuFont = pygame.font.Font("Roboto-Light.ttf", 100)
largestFont = mainMenuFont
largeFont = pygame.font.SysFont("Roboto-Light.ttf", 40, True)
mediumFont = pygame.font.SysFont("Roboto-Light.ttf", 30, True)
smallFont = pygame.font.SysFont("Roboto-Light.ttf", 18, True)

#Initialize all global variables
#bools
gameInUse = True
mainMenuShowing = True
gameActive = False
restartScreenActive = False

#colors
black = (0, 0, 0)
white = (255, 255, 255)
darkGray = (32, 32, 32)
lightGray = (120, 120, 120)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 230)

mainMenuTopRect = [400, 152, 160, 160]
mainMenuBottomRect = [400, 306, 160, 160]

#create Rects for Arc Circles
xsSquareForCircles = [260, 260, 120, 120]
sSquareForCircles = [200, 200, 240, 240]
mSquareForCircles = [140, 140, 360, 360]
lSquareForCircles = [80, 80, 480, 480]
xlSquareForCircles = [20, 20, 600, 600]
gameInfoRectOuter = [640, 0, 320, 640]
gameInfoRectInner = [655, 15, 290, 610]

arcWidth = 12

mainMenuArc1 = [mainMenuTopRect, 0, pi/4]
mainMenuArc2 = [mainMenuTopRect, pi/4, pi/2]
mainMenuArc3 = [mainMenuTopRect, pi/2, 3*pi/4]
mainMenuArc4 = [mainMenuTopRect, 3*pi/4, pi]
mainMenuArc5 = [mainMenuTopRect, pi, 5*pi/4]
mainMenuArc6 = [mainMenuTopRect, 5*pi/4, 3*pi/2]
mainMenuArc7 = [mainMenuBottomRect, pi/4, pi/2]
mainMenuArc8 = [mainMenuBottomRect, 0, pi/4]
mainMenuArc9 = [mainMenuBottomRect, 7*pi/4, 2*pi]
mainMenuArc10 = [mainMenuBottomRect, 3*pi/2, 7*pi/4]
mainMenuArc11 = [mainMenuBottomRect, 5*pi/4, 3*pi/2]
mainMenuArc12 = [mainMenuBottomRect, pi, 5*pi/4]
mainMenuArcs = [mainMenuArc1, mainMenuArc2, mainMenuArc3, mainMenuArc4, mainMenuArc5, mainMenuArc6, mainMenuArc7, mainMenuArc8, mainMenuArc9, mainMenuArc10, mainMenuArc11, mainMenuArc12]

while gameInUse:
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver = True
				gameActive = False
	scoreHolder = shelve.open('highscore.txt')
	highScore = scoreHolder['highScore']
	scoreHolder.close()

	pygame.mixer.music.stop()
	pygame.mixer.music.load('mainmenu2.mid')
	pygame.mixer.music.play(-1)

	frame.tick(2)
	ticks = 0
	movements = 0
	arcColorRed = random.randint(0,255)
	arcColorBlue = random.randint(0,255)
	arcColorGreen = random.randint(0,255)
	pinColorRed = (arcColorRed + random.randint(20,235)) % 256
	pinColorBlue = (arcColorBlue + random.randint(20,235)) % 256
	pinColorGreen = (arcColorGreen + random.randint(20,235)) % 256
	arcColor = (arcColorRed, arcColorBlue, arcColorGreen)
	spinnerColor = (255, 255, 255)
	if (arcColorRed + arcColorGreen + arcColorBlue) > 500: 
		spinnerColor = darkGray
	elif arcColorRed > 200 and (arcColorBlue > 85 or arcColorGreen > 85): 
		spinnerColor = darkGray
	elif arcColorGreen > 200 and (arcColorRed > 80 or arcColorBlue > 80):
		spinnerColor = darkGray
	elif arcColorBlue > 200 and (arcColorRed > 150 or arcColorGreen > 150):
		spinnerColor = darkGray
	pinColor = (pinColorRed, pinColorBlue, pinColorGreen)
	arcText = mainMenuFont.render("arc", True, pinColor)
	pinText = mainMenuFont.render("pin", True, pinColor)
	while mainMenuShowing:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver = True
				gameActive = False
		if ticks == 5:
			if movements > 11: 
				arcColorRed = random.randint(0,255)
				arcColorBlue = random.randint(0,255)
				arcColorGreen = random.randint(0,255)
				pinColorRed = (arcColorRed + random.randint(20,235)) % 256
				pinColorBlue = (arcColorBlue + random.randint(20,235)) % 256
				pinColorGreen = (arcColorGreen + random.randint(20,235)) % 256
				arcColor = (arcColorRed, arcColorBlue, arcColorGreen)
				pinColor = (pinColorRed, pinColorBlue, pinColorGreen)
				arcText = mainMenuFont.render("arc", True, pinColor)
				pinText = mainMenuFont.render("pin", True, pinColor)
				movements = 0
			screen.fill(black)
			for arc in mainMenuArcs:
				pygame.draw.arc(screen, arcColor, arc[0], arc[1], arc[2], 6)
			screen.blit(arcText, (400 - arcText.get_width(), 232 - arcText.get_height()/2))
			screen.blit(pinText, (560, 386 - pinText.get_height()/2))
			highScoreText = largeFont.render("High Score => " + str(highScore), True, pinColor)
			screen.blit(highScoreText, (480 - highScoreText.get_width()/2, 540 - highScoreText.get_height()/2))
			aaHumbleText = smallFont.render("By A Humble Tech Co, copyright 2018", True, arcColor)
			screen.blit(aaHumbleText, (480 - aaHumbleText.get_width()/2, 600 - aaHumbleText.get_height()/2))
			pygame.draw.arc(screen, pinColor, mainMenuArcs[movements][0], mainMenuArcs[movements][1], mainMenuArcs[movements][2], 6)
			movements += 1
			ticks = 0
		ticks += 1
		pygame.display.flip()
		frame.tick(30)

		pygame.event.pump()
		if pygame.mouse.get_pressed()[0]:
			#Game Over Reasons
			tooManyRotations = largeFont.render("Too many rotations!", True, pinColor)
			missedAPin = largeFont.render("You missed a pin!", True, pinColor)
			ticks = 0
			mainMenuShowing = False
			gameActive = True
			xsCircleActive = True
			pygame.mixer.music.stop()
			pygame.mixer.music.load('gameplay2.mid')
			pygame.mixer.music.play(-1)


	while gameActive:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver = True
				gameActive = False
		
		gameOver = False
		sCircleActive = False
		mCircleActive = False
		lCircleActive = False
		xlCircleActive = False
		isNewHighScore = False
		screen.fill(black)
		#New game starts here
		level = 1
		missedPins = 0
		comboMultiplier = 0
		score = 0
		speedFps = 60
		levelTextWord = largestFont.render("Level", True, pinColor)
		scoreTextWord = largestFont.render("Score", True, pinColor)
		comboTextWord = largeFont.render("Multiplier", True, pinColor)
		levelTextNumber = largestFont.render(str(level), True, arcColor)
		comboTextNumber = largeFont.render(str(comboMultiplier + 1), True, arcColor)
		scoreTextNumber = largeFont.render(str(score), True, arcColor)
		circleScoreText = smallFont.render("", True, pinColor)

		while gameOver == False:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOver = True
					gameActive = False
			frame.tick(5)
			xsCircle = drawPinnedCircle(1, 6, pinColor, arcColor, xsSquareForCircles, [])
			randomMultiplier = random.randint(0, xsCircle.numberOfArcs)
			movements = randomMultiplier
			rotations = 0
			xsCircleStartingRadiant = randomMultiplier * 2 * pi / xsCircle.numberOfArcs
			xsCircleEndingRadiant = xsCircleStartingRadiant + (2 * pi / xsCircle.numberOfArcs)
			xsCircleRadiantIncrement = 2 * pi/ xsCircle.numberOfArcs
			pygame.draw.arc(screen, spinnerColor, xsSquareForCircles, xsCircleStartingRadiant, xsCircleEndingRadiant, arcWidth)
			ticks = 0
			levelTextNumber = largestFont.render(str(level), True, arcColor)
			comboTextNumber = largeFont.render(str(comboMultiplier + 1), True, arcColor)
			pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
			pygame.draw.rect(screen, darkGray, gameInfoRectInner)
			screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
			screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
			screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
			screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
			screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
			screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))
			screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
			
			while xsCircleActive == True:
				pygame.event.pump()
				if pygame.mouse.get_pressed()[0]:
					if movements == 0: movements = xsCircle.numberOfArcs
					print movements, xsCircle.pins[0]
					circleScore, missedPin, comboMultiplier = getScoreMissedPinsAndMultiplier(100, 60, movements - 1, xsCircle.pins, xsCircle.numberOfArcs, comboMultiplier, rotations)
					if missedPin: missedPins += 1
					score += circleScore
					xsCircleActive = False
					sCircleActive = True
					speedFps = int(1.02 * speedFps)
					continue
				elif ticks == 20:
					screen.fill(black)
					pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
					pygame.draw.rect(screen, darkGray, gameInfoRectInner)
					screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
					screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
					screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
					screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
					screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
					screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))
					screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
					drawPinnedCircle(xsCircle.numberOfPins, xsCircle.numberOfArcs, xsCircle.color1, xsCircle.color2, xsCircle.areaForCircle, xsCircle.pins)
					pygame.draw.arc(screen, spinnerColor, xsSquareForCircles, xsCircleStartingRadiant, xsCircleEndingRadiant, arcWidth)
					xsCircleStartingRadiant += xsCircleRadiantIncrement
					xsCircleEndingRadiant += xsCircleRadiantIncrement
					ticks = 0
					movements += 1
				elif movements == xsCircle.numberOfArcs:
					rotations += 1
					movements = 0
				ticks += 1
				if rotations > 15:
					circleScore = 0
					xsCircleActive = False
					gameOver = True
					gameOverReason = tooManyRotations
				pygame.display.flip()
				frame.tick(speedFps)
			screen.fill(black)
			pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
			pygame.draw.rect(screen, darkGray, gameInfoRectInner)
			circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
			screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
			drawPinnedCircle(xsCircle.numberOfPins, xsCircle.numberOfArcs, xsCircle.color1, xsCircle.color2, xsCircle.areaForCircle, xsCircle.pins)
			pygame.draw.arc(screen, spinnerColor, xsSquareForCircles, xsCircleStartingRadiant - xsCircleRadiantIncrement, xsCircleEndingRadiant - xsCircleRadiantIncrement, arcWidth)
			scoreTextNumber = largeFont.render(str(score), True, arcColor)
			screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
			screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
			screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
			screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
			screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
			screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))

			if gameOver:
				if score > highScore:
					scoreHolder = shelve.open('highscore.txt')
					scoreHolder['highScore'] = score
					scoreHolder.close()
					highScore = score
					isNewHighScore = True
				frame.tick(1)
				screen.fill(black)
				circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				restartScreenActive = True
				pygame.display.flip()
				continue

			frame.tick(5)
			sCircle = drawPinnedCircle(1, 12, pinColor, arcColor, sSquareForCircles, [])
			randomMultiplier = random.randint(0, sCircle.numberOfArcs)
			movements = randomMultiplier
			rotations = 0
			sCircleStartingRadiant = randomMultiplier * 2 * pi / sCircle.numberOfArcs
			sCircleEndingRadiant = sCircleStartingRadiant + (2 * pi / sCircle.numberOfArcs)
			sCircleRadiantIncrement = 2 * pi/ sCircle.numberOfArcs
			pygame.draw.arc(screen, spinnerColor, sSquareForCircles, sCircleStartingRadiant, sCircleEndingRadiant, arcWidth)
			ticks = 0
			levelTextNumber = largestFont.render(str(level), True, arcColor)
			comboTextNumber = largeFont.render(str(comboMultiplier + 1), True, arcColor)
			pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
			pygame.draw.rect(screen, darkGray, gameInfoRectInner)	
			screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
			screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
			screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
			screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
			screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
			screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))
			
			while sCircleActive == True:
				pygame.event.pump()
				if pygame.mouse.get_pressed()[0]:
					if movements == 0: movements = sCircle.numberOfArcs
					print movements, sCircle.pins[0]
					circleScore, missedPin, comboMultiplier = getScoreMissedPinsAndMultiplier(200, 120, movements - 1, sCircle.pins, sCircle.numberOfArcs, comboMultiplier, rotations)
					if missedPin: missedPins += 1
					score += circleScore
					sCircleActive = False
					mCircleActive = True
					speedFps = int(1.02 * speedFps)
					continue
				if ticks == 20:
					screen.fill(black)
					pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
					pygame.draw.rect(screen, darkGray, gameInfoRectInner)
					screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
					screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
					screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
					screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
					screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
					screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))
					screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
					drawPinnedCircle(sCircle.numberOfPins, sCircle.numberOfArcs, sCircle.color1, sCircle.color2, sCircle.areaForCircle, sCircle.pins)
					pygame.draw.arc(screen, spinnerColor, sSquareForCircles, sCircleStartingRadiant, sCircleEndingRadiant, arcWidth)
					sCircleStartingRadiant += sCircleRadiantIncrement
					sCircleEndingRadiant += sCircleRadiantIncrement
					ticks = 0
					movements += 1
				if movements == sCircle.numberOfArcs:
					rotations += 1
					movements = 0
				ticks += 1
				if rotations > 15:
					circleScore = 0
					sCircleActive = False
					gameOver = True
					gameOverReason = tooManyRotations
				pygame.display.flip()
				frame.tick(speedFps)
			screen.fill(black)
			pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
			pygame.draw.rect(screen, darkGray, gameInfoRectInner)
			circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
			screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
			drawPinnedCircle(sCircle.numberOfPins, sCircle.numberOfArcs, sCircle.color1, sCircle.color2, sCircle.areaForCircle, sCircle.pins)
			pygame.draw.arc(screen, spinnerColor, sSquareForCircles, sCircleStartingRadiant - sCircleRadiantIncrement, sCircleEndingRadiant - sCircleRadiantIncrement, arcWidth)
			scoreTextNumber = largeFont.render(str(score), True, arcColor)
			screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
			screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
			screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
			screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
			screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
			screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))

			if gameOver:
				if score > highScore:
					scoreHolder = shelve.open('highscore.txt')
					scoreHolder['highScore'] = score
					scoreHolder.close()
					highScore = score
					isNewHighScore = True
				frame.tick(1)
				screen.fill(black)
				circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				restartScreenActive = True
				pygame.display.flip()
				continue

			frame.tick(5)
			mCircle = drawPinnedCircle(1, 24, pinColor, arcColor, mSquareForCircles, [])
			randomMultiplier = random.randint(0, mCircle.numberOfArcs)
			movements = randomMultiplier
			rotations = 0
			mCircleStartingRadiant = randomMultiplier * 2 * pi / mCircle.numberOfArcs
			mCircleEndingRadiant = mCircleStartingRadiant + (2 * pi / mCircle.numberOfArcs)
			mCircleRadiantIncrement = 2 * pi/ mCircle.numberOfArcs
			pygame.draw.arc(screen, spinnerColor, mSquareForCircles, mCircleStartingRadiant, mCircleEndingRadiant, arcWidth)
			ticks = 0
			levelTextNumber = largestFont.render(str(level), True, arcColor)
			comboTextNumber = largeFont.render(str(comboMultiplier + 1), True, arcColor)
			pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
			pygame.draw.rect(screen, darkGray, gameInfoRectInner)
			screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
			screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
			screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
			screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
			screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
			screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))
			
			while mCircleActive == True:
				pygame.event.pump()
				if pygame.mouse.get_pressed()[0]:
					if movements == 0: movements = mCircle.numberOfArcs
					circleScore, missedPin, comboMultiplier = getScoreMissedPinsAndMultiplier(400, 240, movements - 1, mCircle.pins, mCircle.numberOfArcs, comboMultiplier, rotations)
					if missedPin: missedPins += 1
					score += circleScore

					if level > 3:
						mCircleActive = False
						lCircleActive = True
						speedFps = int(1.02 * speedFps)
					else:
						if missedPins > 0:
							circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
							screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2)) 
							mCircleActive = False
							gameOver = True
							gameOverReason = missedAPin
							continue
						else:
							circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
							screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
							drawPinnedCircle(mCircle.numberOfPins, mCircle.numberOfArcs, mCircle.color1, mCircle.color2, mCircle.areaForCircle, mCircle.pins)
							pygame.draw.arc(screen, spinnerColor, mSquareForCircles, mCircleStartingRadiant - mCircleRadiantIncrement, mCircleEndingRadiant - mCircleRadiantIncrement, arcWidth)
							level += 1	
							mCircleActive = False
							xsCircleActive = True
							speedFps = int((1.02 ** level) * speedFps)
				if ticks == 20:
					screen.fill(black)
					pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
					pygame.draw.rect(screen, darkGray, gameInfoRectInner)
					screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
					screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
					screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
					screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
					screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
					screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))
					screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
					drawPinnedCircle(mCircle.numberOfPins, mCircle.numberOfArcs, mCircle.color1, mCircle.color2, mCircle.areaForCircle, mCircle.pins)
					pygame.draw.arc(screen, spinnerColor, mSquareForCircles, mCircleStartingRadiant, mCircleEndingRadiant, arcWidth)
					mCircleStartingRadiant += mCircleRadiantIncrement
					mCircleEndingRadiant += mCircleRadiantIncrement
					ticks = 0
					movements += 1
				if movements == mCircle.numberOfArcs:
					rotations += 1
					movements = 0
				ticks += 1
				if rotations > 15:
					circleScore = 0
					mCircleActive = False
					gameOver = True
					gameOverReason = tooManyRotations
				pygame.display.flip()
				frame.tick(speedFps)
			screen.fill(black)
			if lCircleActive:
				pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
				pygame.draw.rect(screen, darkGray, gameInfoRectInner)
				circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				drawPinnedCircle(mCircle.numberOfPins, mCircle.numberOfArcs, mCircle.color1, mCircle.color2, mCircle.areaForCircle, mCircle.pins)
				pygame.draw.arc(screen, spinnerColor, mSquareForCircles, mCircleStartingRadiant - mCircleRadiantIncrement, mCircleEndingRadiant - mCircleRadiantIncrement, arcWidth)
			scoreTextNumber = largeFont.render(str(score), True, arcColor)
			screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
			screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
			screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
			screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
			screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
			screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))

			if gameOver:
				if score > highScore:
					scoreHolder = shelve.open('highscore.txt')
					scoreHolder['highScore'] = score
					scoreHolder.close()
					highScore = score
					isNewHighScore = True
				frame.tick(1)
				screen.fill(black)
				circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				restartScreenActive = True
				pygame.display.flip()
				continue

			if lCircleActive and level > 3:
				frame.tick(5)
				lCircle = drawPinnedCircle(1, 60, pinColor, arcColor, lSquareForCircles, [])
				randomMultiplier = random.randint(0, lCircle.numberOfArcs)
				movements = randomMultiplier
				rotations = 0
				lCircleStartingRadiant = randomMultiplier * 2 * pi / lCircle.numberOfArcs
				lCircleEndingRadiant = lCircleStartingRadiant + (2 * pi / lCircle.numberOfArcs)
				lCircleRadiantIncrement = 2 * pi/ lCircle.numberOfArcs
				pygame.draw.arc(screen, spinnerColor, lSquareForCircles, lCircleStartingRadiant, lCircleEndingRadiant, arcWidth)
				ticks = 0
				levelTextNumber = largestFont.render(str(level), True, arcColor)
				comboTextNumber = largeFont.render(str(comboMultiplier + 1), True, arcColor)
				pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
				pygame.draw.rect(screen, darkGray, gameInfoRectInner)
				screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
				screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
				screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
				screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
				screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
				screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))
				while lCircleActive == True:
					pygame.event.pump()
					if pygame.mouse.get_pressed()[0]:
						if movements == 0: movements = lCircle.numberOfArcs
						circleScore, missedPin, comboMultiplier = getScoreMissedPinsAndMultiplier(1000, 600, movements - 1, lCircle.pins, lCircle.numberOfArcs, comboMultiplier, rotations)
						if missedPin: missedPins += 1
						score += circleScore
						if level >= 6:
							lCircleActive = False
							xlCircleActive = True
							speedFps = int(1.02 * speedFps)
						else:
							if missedPins > 0:
								circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
								screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2)) 
								lCircleActive = False
								gameOver = True
								gameOverReason = missedAPin
								continue
							else:
								drawPinnedCircle(lCircle.numberOfPins, lCircle.numberOfArcs, lCircle.color1, lCircle.color2, lCircle.areaForCircle, lCircle.pins)
								pygame.draw.arc(screen, spinnerColor, lSquareForCircles, lCircleStartingRadiant - lCircleRadiantIncrement, lCircleEndingRadiant - lCircleRadiantIncrement, arcWidth)
								circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
								screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
								level += 1	
								lCircleActive = False
								xsCircleActive = True
								speedFps = int((1.02 ** level) * speedFps)
					if ticks == 12:
						screen.fill(black)
						pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
						pygame.draw.rect(screen, darkGray, gameInfoRectInner)
						screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
						screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
						screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
						screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
						screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
						screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))
						screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
						drawPinnedCircle(lCircle.numberOfPins, lCircle.numberOfArcs, lCircle.color1, lCircle.color2, lCircle.areaForCircle, lCircle.pins)
						pygame.draw.arc(screen, spinnerColor, lSquareForCircles, lCircleStartingRadiant, lCircleEndingRadiant, arcWidth)
						lCircleStartingRadiant += lCircleRadiantIncrement
						lCircleEndingRadiant += lCircleRadiantIncrement
						ticks = 0
						movements += 1
					if movements == lCircle.numberOfArcs:
						rotations += 1
						movements = 0
					ticks += 1
					if rotations > 20:
						circleScore = 0
						lCircleActive = False
						gameOver = True
						gameOverReason = tooManyRotations
					pygame.display.flip()
					frame.tick(speedFps)
				screen.fill(black)
				if xlCircleActive:
					pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
					pygame.draw.rect(screen, darkGray, gameInfoRectInner)
					circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
					screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
					drawPinnedCircle(lCircle.numberOfPins, lCircle.numberOfArcs, lCircle.color1, lCircle.color2, lCircle.areaForCircle, lCircle.pins)
					pygame.draw.arc(screen, spinnerColor, lSquareForCircles, lCircleStartingRadiant - lCircleRadiantIncrement, lCircleEndingRadiant - lCircleRadiantIncrement, arcWidth)
				scoreTextNumber = largeFont.render(str(score), True, arcColor)
				screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
				screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
				screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
				screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
				screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
				screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))

			if gameOver:
				if score > highScore:
					scoreHolder = shelve.open('highscore.txt')
					scoreHolder['highScore'] = score
					scoreHolder.close()
					highScore = score
					isNewHighScore = True
				frame.tick(1)
				screen.fill(black)
				circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				restartScreenActive = True
				pygame.display.flip()
				continue

			if xlCircleActive and level >= 6:
				frame.tick(5)
				xlCircle = drawPinnedCircle(1, 120, pinColor, arcColor, xlSquareForCircles, [])
				randomMultiplier = random.randint(0, xlCircle.numberOfArcs)
				movements = randomMultiplier
				rotations = 0
				xlCircleStartingRadiant = randomMultiplier * 2 * pi / xlCircle.numberOfArcs
				xlCircleEndingRadiant = xlCircleStartingRadiant + (2 * pi / xlCircle.numberOfArcs)
				xlCircleRadiantIncrement = 2 * pi/ xlCircle.numberOfArcs
				pygame.draw.arc(screen, spinnerColor, xlSquareForCircles, xlCircleStartingRadiant, xlCircleEndingRadiant, arcWidth)
				ticks = 0
				levelTextNumber = largestFont.render(str(level), True, arcColor)
				comboTextNumber = largeFont.render(str(comboMultiplier + 1), True, arcColor)
				pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
				pygame.draw.rect(screen, darkGray, gameInfoRectInner)
				screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
				screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
				screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
				screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
				screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
				screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))
				while xlCircleActive == True:
					pygame.event.pump()
					if pygame.mouse.get_pressed()[0]:
						if movements == 0: movements = xlCircle.numberOfArcs
						circleScore, missedPin, comboMultiplier = getScoreMissedPinsAndMultiplier(2000, 1200, movements - 1, xlCircle.pins, xlCircle.numberOfArcs, comboMultiplier, rotations)
						if missedPin: missedPins += 1
						score += circleScore
						if missedPins > 0:
							circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
							screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2)) 
							xlCircleActive = False
							gameOver = True
							gameOverReason = missedAPin
							continue
						else:
							drawPinnedCircle(xlCircle.numberOfPins, xlCircle.numberOfArcs, xlCircle.color1, xlCircle.color2, xlCircle.areaForCircle, xlCircle.pins)
							pygame.draw.arc(screen, spinnerColor, xlSquareForCircles, xlCircleStartingRadiant - xlCircleRadiantIncrement, xlCircleEndingRadiant - xlCircleRadiantIncrement, arcWidth)
							circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
							screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
							level += 1	
							xlCircleActive = False
							xsCircleActive = True
							speedFps = int((1.02 ** level) * speedFps)
					if ticks == 8:
						screen.fill(black)
						pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
						pygame.draw.rect(screen, darkGray, gameInfoRectInner)
						screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
						screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
						screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
						screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
						screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
						screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))
						screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
						drawPinnedCircle(xlCircle.numberOfPins, xlCircle.numberOfArcs, xlCircle.color1, xlCircle.color2, xlCircle.areaForCircle, xlCircle.pins)
						pygame.draw.arc(screen, spinnerColor, xlSquareForCircles, xlCircleStartingRadiant, xlCircleEndingRadiant, arcWidth)
						xlCircleStartingRadiant += xlCircleRadiantIncrement
						xlCircleEndingRadiant += xlCircleRadiantIncrement
						ticks = 0
						movements += 1
					if movements == xlCircle.numberOfArcs:
						rotations += 1
						movements = 0
					ticks += 1
					if rotations > 25:
						circleScore = 0
						xlCircleActive = False
						gameOver = True
						gameOverReason = tooManyRotations
					pygame.display.flip()
					frame.tick(speedFps)
				screen.fill(black)
				pygame.draw.rect(screen, lightGray, gameInfoRectOuter)
				pygame.draw.rect(screen, darkGray, gameInfoRectInner)
				circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				drawPinnedCircle(xlCircle.numberOfPins, xlCircle.numberOfArcs, xlCircle.color1, xlCircle.color2, xlCircle.areaForCircle, xlCircle.pins)
				pygame.draw.arc(screen, spinnerColor, xlSquareForCircles, xlCircleStartingRadiant - xlCircleRadiantIncrement, xlCircleEndingRadiant - xlCircleRadiantIncrement, arcWidth)
				scoreTextNumber = largeFont.render(str(score), True, arcColor)
				screen.blit(levelTextWord, (800 - levelTextWord.get_width()/2, 80 - levelTextWord.get_height()/2))
				screen.blit(levelTextNumber, (800 - levelTextNumber.get_width()/2, 160 - levelTextNumber.get_height()/2))
				screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 280 - scoreTextWord.get_height()/2))
				screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 340 - scoreTextNumber.get_height()/2))
				screen.blit(comboTextWord, (800 - comboTextWord.get_width()/2, 480 - comboTextWord.get_height()/2))
				screen.blit(comboTextNumber, (800 - comboTextNumber.get_width()/2, 520 - comboTextNumber.get_height()/2))
				pygame.display.flip()

			if gameOver:
				if score > highScore:
					scoreHolder = shelve.open('highscore.txt')
					scoreHolder['highScore'] = score
					scoreHolder.close()
					highScore = score
					isNewHighScore = True
				frame.tick(2)
				screen.fill(black)
				circleScoreText = smallFont.render("+ " + str(circleScore), True, pinColor)
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				restartScreenActive = True
				pygame.display.flip()
				frame.tick(1.5)
				ticks = 0
				continue
		
		pygame.mixer.music.stop()
		pygame.mixer.music.load('gameover.mid')
		pygame.mixer.music.play(1)
		while restartScreenActive:
			if ticks == 30:
				screen.fill(black)
				gameOverText = largestFont.render("GAME OVER", True, arcColor)
				screen.blit(gameOverText, (480 - gameOverText.get_width()/2, 150 - gameOverText.get_height()/2))
				screen.blit(gameOverReason, (480 - gameOverReason.get_width()/2, 240 - gameOverReason.get_height()/2))
				finalScoreText = largeFont.render("Your Score => " + str(score), True, arcColor)
				screen.blit(finalScoreText, (480 - finalScoreText.get_width()/2, 320 - finalScoreText.get_height()/2))
				highScoreText = largeFont.render("High Score => " + str(highScore), True, pinColor)
				screen.blit(highScoreText, (480 - highScoreText.get_width()/2, 400 - highScoreText.get_height()/2))
			elif ticks == 60:
				screen.fill(black)
				gameOverText = largestFont.render("GAME OVER", True, pinColor)
				screen.blit(gameOverText, (480 - gameOverText.get_width()/2, 150 - gameOverText.get_height()/2))
				finalScoreText = largeFont.render("Your Score => " + str(score), True, arcColor)
				screen.blit(finalScoreText, (480 - finalScoreText.get_width()/2, 320 - finalScoreText.get_height()/2))
				highScoreText = largeFont.render("High Score => " + str(highScore), True, pinColor)
				screen.blit(highScoreText, (480 - highScoreText.get_width()/2, 400 - highScoreText.get_height()/2))
				ticks = 0
			pygame.display.flip()
			frame.tick(60)
			ticks += 1
			pygame.event.pump()
			if pygame.mouse.get_pressed()[0]:
				restartScreenActive = False
				mainMenuShowing = True
				gameActive = False
				continue