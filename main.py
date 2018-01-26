import pygame
from math import pi
#import math
import random

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
	if movements == 0: movements = numberOfArcs
	if (movements - 1) == circlePins[0]:
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

#def playAgain():
	#let screen tick for a second or two
	#blacken screen
	#Display game over; final score
	#Ask to hit space bar if they want to play again
	#if space bar is hit, return True

pygame.init()
pygame.display.set_caption("ArcSpin")
size = (960, 640)
screen = pygame.display.set_mode(size)
frame = pygame.time.Clock()
largeFont = pygame.font.SysFont("arial", 30, True)
mediumFont = pygame.font.SysFont("arial", 22, True)
smallFont = pygame.font.SysFont("arial", 14, True)

#Initialize all global variables
#bools
failed = False
gameActive = True
xsCircleActive = True
sCircleActive = False
mCircleActive = False
lCircleActive = False
xlCircleActive = False

#colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (204, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 153)
purple = (76, 0, 153)
gray = (96, 96, 96)
darkGray = (32, 32, 32)

#create Rects for Arc Circles
xsSquareForCircles = [260, 260, 120, 120]
sSquareForCircles = [200, 200, 240, 240]
mSquareForCircles = [140, 140, 360, 360]
lSquareForCircles = [80, 80, 480, 480]
xlSquareForCircles = [20, 20, 600, 600]

tooManyRotations = largeFont.render("Too many rotations!", True, white)
arcWidth = 12

while gameActive == True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			failed = True
			gameActive = False
	

	#New game starts here
	level = 1
	missedPins = 0
	comboMultiplier = 0
	score = 0
	frameTicks = 30
	scoreTextWord = largeFont.render("Score", True, white)
	scoreTextNumber = largeFont.render(str(score), True, white)
	circleScoreText = smallFont.render("", True, white)

	while failed == False:
		frame.tick(5)
		xsCircle = drawPinnedCircle(1, 6, red, blue, xsSquareForCircles, [])
		randomMultiplier = random.randint(0, xsCircle.numberOfArcs)
		movements = randomMultiplier
		rotations = 0
		xsCircleStartingRadiant = randomMultiplier * 2 * pi / xsCircle.numberOfArcs
		xsCircleEndingRadiant = xsCircleStartingRadiant + (2 * pi / xsCircle.numberOfArcs)
		xsCircleRadiantIncrement = 2 * pi/ xsCircle.numberOfArcs
		pygame.draw.arc(screen, white, xsSquareForCircles, xsCircleStartingRadiant, xsCircleEndingRadiant, arcWidth)
		ticks = 0
		screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
		screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
		screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
		while xsCircleActive == True:
			pygame.event.pump()
			pressedKeys = pygame.key.get_pressed()
			if pressedKeys[pygame.K_SPACE]:
				circleScore, missedPin, comboMultiplier = getScoreMissedPinsAndMultiplier(100, 60, movements, xsCircle.pins, xsCircle.numberOfArcs, comboMultiplier, rotations)
				if missedPin: missedPins += 1
				score += circleScore
				xsCircleActive = False
				sCircleActive = True
				break
			if level >= 10:
				screen.fill(black)
				screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
				screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				drawPinnedCircle(xsCircle.numberOfPins, xsCircle.numberOfArcs, xsCircle.color1, xsCircle.color2, xsCircle.areaForCircle, xsCircle.pins)
				pygame.draw.arc(screen, white, xsSquareForCircles, xsCircleStartingRadiant, xsCircleEndingRadiant, arcWidth)
				xsCircleStartingRadiant += xsCircleRadiantIncrement
				xsCircleEndingRadiant += xsCircleRadiantIncrement
				movements += 1
			elif ticks == 90 - ((level - 1) * 10):
				screen.fill(black)
				screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
				screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				drawPinnedCircle(xsCircle.numberOfPins, xsCircle.numberOfArcs, xsCircle.color1, xsCircle.color2, xsCircle.areaForCircle, xsCircle.pins)
				pygame.draw.arc(screen, white, xsSquareForCircles, xsCircleStartingRadiant, xsCircleEndingRadiant, arcWidth)
				xsCircleStartingRadiant += xsCircleRadiantIncrement
				xsCircleEndingRadiant += xsCircleRadiantIncrement
				ticks = 0
				movements += 1
			if movements == xsCircle.numberOfArcs:
				rotations += 1
				movements = 0
			ticks += 1
			if rotations > 10:
				circleScore = 0
				xsCircleActive = False
				failed = True
				screen.blit(tooManyRotations, (800 - tooManyRotations.get_width()/2, 320 - tooManyRotations.get_height()/2))
			pygame.display.flip()
			frame.tick(frameTicks)
		screen.fill(black)
		circleScoreText = smallFont.render("+ " + str(circleScore), True, white)
		screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
		drawPinnedCircle(xsCircle.numberOfPins, xsCircle.numberOfArcs, xsCircle.color1, xsCircle.color2, xsCircle.areaForCircle, xsCircle.pins)
		pygame.draw.arc(screen, white, xsSquareForCircles, xsCircleStartingRadiant - xsCircleRadiantIncrement, xsCircleEndingRadiant - xsCircleRadiantIncrement, arcWidth)
		screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
		scoreTextNumber = largeFont.render(str(score), True, white)
		screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))

		if failed: 
			#Show high score(s)
			#gameRestart = playAgain()
			#if not gameRestart: gameActive = False
			continue

		frame.tick(5)
		sCircle = drawPinnedCircle(1, 12, red, blue, sSquareForCircles, [])
		randomMultiplier = random.randint(0, sCircle.numberOfArcs)
		movements = randomMultiplier
		rotations = 0
		sCircleStartingRadiant = randomMultiplier * 2 * pi / sCircle.numberOfArcs
		sCircleEndingRadiant = sCircleStartingRadiant + (2 * pi / sCircle.numberOfArcs)
		sCircleRadiantIncrement = 2 * pi/ sCircle.numberOfArcs
		pygame.draw.arc(screen, white, sSquareForCircles, sCircleStartingRadiant, sCircleEndingRadiant, arcWidth)
		ticks = 0
		screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
		screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
		while sCircleActive == True:
			pygame.event.pump()
			pressedKeys = pygame.key.get_pressed()
			if pressedKeys[pygame.K_SPACE]:
				circleScore, missedPin, comboMultiplier = getScoreMissedPinsAndMultiplier(500, 300, movements, sCircle.pins, sCircle.numberOfArcs, comboMultiplier, rotations)
				if missedPin: missedPins += 1
				score += circleScore
				sCircleActive = False
				mCircleActive = True
				break
			if level >= 10:
				screen.fill(black)
				screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
				screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				drawPinnedCircle(sCircle.numberOfPins, sCircle.numberOfArcs, sCircle.color1, sCircle.color2, sCircle.areaForCircle, sCircle.pins)
				pygame.draw.arc(screen, white, sSquareForCircles, sCircleStartingRadiant, sCircleEndingRadiant, arcWidth)
				sCircleStartingRadiant += sCircleRadiantIncrement
				sCircleEndingRadiant += sCircleRadiantIncrement
				movements += 1
			elif ticks == 85 - ((level - 1) * 10):
				screen.fill(black)
				screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
				screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				drawPinnedCircle(sCircle.numberOfPins, sCircle.numberOfArcs, sCircle.color1, sCircle.color2, sCircle.areaForCircle, sCircle.pins)
				pygame.draw.arc(screen, white, sSquareForCircles, sCircleStartingRadiant, sCircleEndingRadiant, arcWidth)
				sCircleStartingRadiant += sCircleRadiantIncrement
				sCircleEndingRadiant += sCircleRadiantIncrement
				ticks = 0
				movements += 1
			if movements == sCircle.numberOfArcs: #Add a rotation for every {numberOfArcs} movements
				rotations += 1
				movements = 0
			ticks += 1
			if rotations > 12:
				circleScore = 0
				sCircleActive = False
				failed = True
				gameActive = False
				screen.blit(tooManyRotations, (800 - tooManyRotations.get_width()/2, 320 - tooManyRotations.get_height()/2))
			pygame.display.flip()
			frame.tick(300)
		screen.fill(black)
		circleScoreText = smallFont.render("+ " + str(circleScore), True, white)
		screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
		drawPinnedCircle(sCircle.numberOfPins, sCircle.numberOfArcs, sCircle.color1, sCircle.color2, sCircle.areaForCircle, sCircle.pins)
		pygame.draw.arc(screen, white, sSquareForCircles, sCircleStartingRadiant - sCircleRadiantIncrement, sCircleEndingRadiant - sCircleRadiantIncrement, arcWidth)
		screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
		scoreTextNumber = largeFont.render(str(score), True, white)
		screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))

		if failed: continue

		frame.tick(5)
		mCircle = drawPinnedCircle(1, 24, red, blue, mSquareForCircles, [])
		randomMultiplier = random.randint(0, mCircle.numberOfArcs)
		movements = randomMultiplier
		rotations = 0
		mCircleStartingRadiant = randomMultiplier * 2 * pi / mCircle.numberOfArcs
		mCircleEndingRadiant = mCircleStartingRadiant + (2 * pi / mCircle.numberOfArcs)
		mCircleRadiantIncrement = 2 * pi/ mCircle.numberOfArcs
		pygame.draw.arc(screen, white, mSquareForCircles, mCircleStartingRadiant, mCircleEndingRadiant, arcWidth)
		ticks = 0
		screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
		screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
		while mCircleActive == True:
			pygame.event.pump()
			pressedKeys = pygame.key.get_pressed()
			if pressedKeys[pygame.K_SPACE]:
				circleScore, missedPin, comboMultiplier = getScoreMissedPinsAndMultiplier(1000, 600, movements, mCircle.pins, mCircle.numberOfArcs, comboMultiplier, rotations)
				if missedPin: missedPins += 1
				score += circleScore
				if level > 3:
					mCircleActive = False
					lCircleActive = True
				else:
					if missedPins > 0: 
						circleScoreText = smallFont.render("+ " + str(circleScore), True, white)
						screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2)) 
						mCircleActive = False
						failed = True
					else:
						circleScoreText = smallFont.render("+ " + str(circleScore), True, white)
						screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
						drawPinnedCircle(mCircle.numberOfPins, mCircle.numberOfArcs, mCircle.color1, mCircle.color2, mCircle.areaForCircle, mCircle.pins)
						pygame.draw.arc(screen, white, mSquareForCircles, mCircleStartingRadiant - mCircleRadiantIncrement, mCircleEndingRadiant - mCircleRadiantIncrement, arcWidth)
						level += 1	
						mCircleActive = False
						xsCircleActive = True
				break
			if level >= 9:
				screen.fill(black)
				screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
				screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				drawPinnedCircle(mCircle.numberOfPins, mCircle.numberOfArcs, mCircle.color1, mCircle.color2, mCircle.areaForCircle, mCircle.pins)
				pygame.draw.arc(screen, white, mSquareForCircles, mCircleStartingRadiant, mCircleEndingRadiant, arcWidth)
				mCircleStartingRadiant += mCircleRadiantIncrement
				mCircleEndingRadiant += mCircleRadiantIncrement
				movements += 1
			elif ticks == 80 - ((level - 1) * 10):
				screen.fill(black)
				screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
				screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				drawPinnedCircle(mCircle.numberOfPins, mCircle.numberOfArcs, mCircle.color1, mCircle.color2, mCircle.areaForCircle, mCircle.pins)
				pygame.draw.arc(screen, white, mSquareForCircles, mCircleStartingRadiant, mCircleEndingRadiant, arcWidth)
				mCircleStartingRadiant += mCircleRadiantIncrement
				mCircleEndingRadiant += mCircleRadiantIncrement
				ticks = 0
				movements += 1
			if movements == mCircle.numberOfArcs: #Add a rotation for every {numberOfArcs} movements
				rotations += 1
				movements = 0
			ticks += 1
			if rotations > 15:
				circleScore = 0
				mCircleActive = False
				failed = True
				gameActive = False
				screen.blit(tooManyRotations, (800 - tooManyRotations.get_width()/2, 320 - tooManyRotations.get_height()/2))
			pygame.display.flip()
			frame.tick(300)
		screen.fill(black)
		if lCircleActive:
			circleScoreText = smallFont.render("+ " + str(circleScore), True, white)
			screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
			drawPinnedCircle(mCircle.numberOfPins, mCircle.numberOfArcs, mCircle.color1, mCircle.color2, mCircle.areaForCircle, mCircle.pins)
			pygame.draw.arc(screen, white, mSquareForCircles, mCircleStartingRadiant - mCircleRadiantIncrement, mCircleEndingRadiant - mCircleRadiantIncrement, arcWidth)
		screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
		scoreTextNumber = largeFont.render(str(score), True, white)
		screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))

		if failed: continue

		if lCircleActive and level > 3:
			frame.tick(5)
			lCircle = drawPinnedCircle(1, 60, red, blue, lSquareForCircles, [])
			randomMultiplier = random.randint(0, lCircle.numberOfArcs)
			movements = randomMultiplier
			rotations = 0
			lCircleStartingRadiant = randomMultiplier * 2 * pi / lCircle.numberOfArcs
			lCircleEndingRadiant = lCircleStartingRadiant + (2 * pi / lCircle.numberOfArcs)
			lCircleRadiantIncrement = 2 * pi/ lCircle.numberOfArcs
			pygame.draw.arc(screen, white, lSquareForCircles, lCircleStartingRadiant, lCircleEndingRadiant, arcWidth)
			ticks = 0
			screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
			screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
			while lCircleActive == True:
				pygame.event.pump()
				pressedKeys = pygame.key.get_pressed()
				if pressedKeys[pygame.K_SPACE]:
					circleScore, missedPin, comboMultiplier = getScoreMissedPinsAndMultiplier(5000, 3000, movements, lCircle.pins, lCircle.numberOfArcs, comboMultiplier, rotations)
					if missedPin: missedPins += 1
					score += circleScore
					if level >= 5:
						lCircleActive = False
						xlCircleActive = True
					else:
						if missedPins > 0:
							circleScoreText = smallFont.render("+ " + str(circleScore), True, white)
							screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2)) 
							lCircleActive = False
							failed = True
						else:
							drawPinnedCircle(lCircle.numberOfPins, lCircle.numberOfArcs, lCircle.color1, lCircle.color2, lCircle.areaForCircle, lCircle.pins)
							pygame.draw.arc(screen, white, lSquareForCircles, lCircleStartingRadiant - lCircleRadiantIncrement, lCircleEndingRadiant - lCircleRadiantIncrement, arcWidth)
							circleScoreText = smallFont.render("+ " + str(circleScore), True, white)
							screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
							level += 1	
							lCircleActive = False
							xsCircleActive = True
					break
				if level == 4 and ticks == 10:
					screen.fill(black)
					screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
					screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
					screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
					drawPinnedCircle(lCircle.numberOfPins, lCircle.numberOfArcs, lCircle.color1, lCircle.color2, lCircle.areaForCircle, lCircle.pins)
					pygame.draw.arc(screen, white, lSquareForCircles, lCircleStartingRadiant, lCircleEndingRadiant, arcWidth)
					lCircleStartingRadiant += lCircleRadiantIncrement
					lCircleEndingRadiant += lCircleRadiantIncrement
					ticks = 0
					movements += 1
				elif level >= 5 and ticks == 3:
					screen.fill(black)
					screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
					screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
					screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
					drawPinnedCircle(lCircle.numberOfPins, lCircle.numberOfArcs, lCircle.color1, lCircle.color2, lCircle.areaForCircle, lCircle.pins)
					pygame.draw.arc(screen, white, lSquareForCircles, lCircleStartingRadiant, lCircleEndingRadiant, arcWidth)
					lCircleStartingRadiant += lCircleRadiantIncrement
					lCircleEndingRadiant += lCircleRadiantIncrement
					ticks = 0
					movements += 1
				if movements == lCircle.numberOfArcs: #Add a rotation for every {numberOfArcs} movements
					rotations += 1
					movements = 0
				ticks += 1
				if rotations > 18:
					circleScore = 0
					lCircleActive = False
					failed = True
					gameActive = False
					screen.blit(tooManyRotations, (800 - tooManyRotations.get_width()/2, 320 - tooManyRotations.get_height()/2))
				pygame.display.flip()
				frame.tick(300)
			screen.fill(black)
			if xlCircleActive:
				circleScoreText = smallFont.render("+ " + str(circleScore), True, white)
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				drawPinnedCircle(lCircle.numberOfPins, lCircle.numberOfArcs, lCircle.color1, lCircle.color2, lCircle.areaForCircle, lCircle.pins)
				pygame.draw.arc(screen, white, lSquareForCircles, lCircleStartingRadiant - lCircleRadiantIncrement, lCircleEndingRadiant - lCircleRadiantIncrement, arcWidth)
			screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
			scoreTextNumber = largeFont.render(str(score), True, white)
			screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))

		if failed: continue

		if xlCircleActive and level >= 5:
			frame.tick(5)
			xlCircle = drawPinnedCircle(1, 120, red, blue, xlSquareForCircles, [])
			randomMultiplier = random.randint(0, xlCircle.numberOfArcs)
			movements = randomMultiplier
			rotations = 0
			xlCircleStartingRadiant = randomMultiplier * 2 * pi / xlCircle.numberOfArcs
			xlCircleEndingRadiant = xlCircleStartingRadiant + (2 * pi / xlCircle.numberOfArcs)
			xlCircleRadiantIncrement = 2 * pi/ xlCircle.numberOfArcs
			pygame.draw.arc(screen, white, xlSquareForCircles, xlCircleStartingRadiant, xlCircleEndingRadiant, arcWidth)
			ticks = 0
			screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
			screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
			while xlCircleActive == True:
				pygame.event.pump()
				pressedKeys = pygame.key.get_pressed()
				if pressedKeys[pygame.K_SPACE]:
					circleScore, missedPin, comboMultiplier = getScoreMissedPinsAndMultiplier(100000, 20000, movements, xlCircle.pins, xlCircle.numberOfArcs, comboMultiplier, rotations)
					score += circleScore
					if missedPin: 
						failed = True
						gameActive = False
					else:
						if missedPins > 0:
							circleScoreText = smallFont.render("+ " + str(circleScore), True, white)
							screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2)) 
							xlCircleActive = False
							failed = True
						else:
							drawPinnedCircle(xlCircle.numberOfPins, xlCircle.numberOfArcs, xlCircle.color1, xlCircle.color2, xlCircle.areaForCircle, xlCircle.pins)
							pygame.draw.arc(screen, white, xlSquareForCircles, xlCircleStartingRadiant - xlCircleRadiantIncrement, xlCircleEndingRadiant - xlCircleRadiantIncrement, arcWidth)
							circleScoreText = smallFont.render("+ " + str(circleScore), True, white)
							screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
							level += 1	
							xlCircleActive = False
							xsCircleActive = True
					break
				screen.fill(black)
				screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
				screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))
				screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
				drawPinnedCircle(xlCircle.numberOfPins, xlCircle.numberOfArcs, xlCircle.color1, xlCircle.color2, xlCircle.areaForCircle, xlCircle.pins)
				pygame.draw.arc(screen, white, xlSquareForCircles, xlCircleStartingRadiant, xlCircleEndingRadiant, arcWidth)
				xlCircleStartingRadiant += xlCircleRadiantIncrement
				xlCircleEndingRadiant += xlCircleRadiantIncrement
				movements += 1
				if movements == xlCircle.numberOfArcs: #Add a rotation for every {numberOfArcs} movements
					rotations += 1
					movements = 0
				if rotations > 25:
					circleScore = 0
					xlCircleActive = False
					failed = True
					gameActive = False
					screen.blit(tooManyRotations, (800 - tooManyRotations.get_width()/2, 320 - tooManyRotations.get_height()/2))
				pygame.display.flip()
				frame.tick(300)
			screen.fill(black)
			circleScoreText = smallFont.render("+ " + str(circleScore), True, white)
			screen.blit(circleScoreText, (320 - circleScoreText.get_width()/2, 320 - circleScoreText.get_height()/2))
			drawPinnedCircle(xlCircle.numberOfPins, xlCircle.numberOfArcs, xlCircle.color1, xlCircle.color2, xlCircle.areaForCircle, xlCircle.pins)
			pygame.draw.arc(screen, white, xlSquareForCircles, xlCircleStartingRadiant - xlCircleRadiantIncrement, xlCircleEndingRadiant - xlCircleRadiantIncrement, arcWidth)
			screen.blit(scoreTextWord, (800 - scoreTextWord.get_width()/2, 120 - scoreTextWord.get_height()/2))
			scoreTextNumber = largeFont.render(str(score), True, white)
			screen.blit(scoreTextNumber, (800 - scoreTextNumber.get_width()/2, 160 - scoreTextNumber.get_height()/2))

		if failed: continue