import pygame
from math import pi
import random

class ArcCircle:
	def __init__(self, numberOfPins, numberOfArcs, color1, color2, areaForCircle, pins):
		self.numberOfPins = numberOfPins
		self.numberOfArcs = numberOfArcs
		self.color1 = color1
		self.color2 = color2
		self.areaForCircle = areaForCircle
		self.pins = pins

#Assign pins
def createRandomPins(numberOfPins, numberOfArcs):
	randomNumber = random.randint(0, numberOfArcs)
	pins = []
	for i in range(numberOfPins):
		pins.append((randomNumber + i)%numberOfArcs)
	return pins

#function for creating the circles
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

pygame.init()
size = (960, 640)
screen = pygame.display.set_mode(size)
frame = pygame.time.Clock()
pygame.display.set_caption("ArcSpin")
font = pygame.font.SysFont("arial", 30, True)
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

screen.fill(darkGray)

arcWidth = 12

#create center Circle(s)
pygame.draw.circle(screen, blue, (320,320), arcWidth)

#create Rects for Arc Circles
xsSquareForCircles = [260, 260, 120, 120]
sSquareForCircles = [200, 200, 240, 240]
mSquareForCircles = [140, 140, 360, 360]
lSquareForCircles = [80, 80, 480, 480]
xlSquareForCircles = [20, 20, 600, 600]

while failed == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			failed = True

	level = 1
	
	while gameActive == True: 
		xsCircle = drawPinnedCircle(1, 6, red, blue, xsSquareForCircles, [])
		xsCircleStartingRadiant = 0
		xsCircleEndingRadiant = pi/3
		xsCircleArcIncrement = pi/3
		xsIncrement = 0
		frame.tick(5)
		while xsCircleActive == True:
			pygame.event.pump()
			pressedKeys = pygame.key.get_pressed()
			if pressedKeys[pygame.K_SPACE]:
				xsCircleActive = False
				sCircleActive = True
				break
			if xsIncrement % 40 == 0:
				drawPinnedCircle(xsCircle.numberOfPins, xsCircle.numberOfArcs, xsCircle.color1, xsCircle.color2, xsCircle.areaForCircle, xsCircle.pins)
				pygame.draw.arc(screen, white, xsSquareForCircles, xsCircleStartingRadiant, xsCircleEndingRadiant, arcWidth)
				xsCircleStartingRadiant += xsCircleArcIncrement
				xsCircleEndingRadiant += xsCircleArcIncrement
			xsIncrement += 1
			if xsIncrement > 1800:
				xsCircleActive = False
				gameActive = False
				failed = True
				tooMany = font.render("Too many rotations!", True, (255, 255, 255))
				screen.blit(tooMany, (800 - tooMany.get_width()/2, 320 - tooMany.get_height()/2))
			pygame.display.flip()
			frame.tick(180)

		if not gameActive:
			continue

		frame.tick(5)
		smallCircle = drawPinnedCircle(1, 12, red, blue, sSquareForCircles, [])
		sCircleStartingRadiant = 0
		sCircleEndingRadiant = pi/6
		sCircleArcIncrement = pi/6
		sIncrement = 0
		while sCircleActive == True:
			pygame.event.pump()
			pressedKeys = pygame.key.get_pressed()
			if pressedKeys[pygame.K_SPACE]:
				sCircleActive = False
				mCircleActive = True
				break
			if sIncrement % 28 == 0:
				drawPinnedCircle(smallCircle.numberOfPins, smallCircle.numberOfArcs, smallCircle.color1, smallCircle.color2, smallCircle.areaForCircle, smallCircle.pins)
				pygame.draw.arc(screen, white, sSquareForCircles, sCircleStartingRadiant, sCircleEndingRadiant, arcWidth)
				sCircleStartingRadiant -= sCircleArcIncrement
				sCircleEndingRadiant -= sCircleArcIncrement
			sIncrement += 1
			if sIncrement > 1800:
				sCircleActive = False
				gameActive = False
				failed = True
				tooMany = font.render("Too many rotations!", True, (255, 255, 255))
				screen.blit(tooMany, (800 - tooMany.get_width()/2, 320 - tooMany.get_height()/2))
			pygame.display.flip()
			frame.tick(180)

		if not gameActive:
			continue

		frame.tick(5)
		mediumCircle = drawPinnedCircle(1, 24, red, blue, mSquareForCircles, [])
		mCircleStartingRadiant = 0
		mCircleEndingRadiant = pi/12
		mCircleArcIncrement = pi/12
		mIncrement = 0
		while mCircleActive == True:
			pygame.event.pump()
			pressedKeys = pygame.key.get_pressed()
			if pressedKeys[pygame.K_SPACE]:
				mCircleActive = False
				lCircleActive = True
				break
			if mIncrement % 20 == 0:
				drawPinnedCircle(mediumCircle.numberOfPins, mediumCircle.numberOfArcs, mediumCircle.color1, mediumCircle.color2, mediumCircle.areaForCircle, mediumCircle.pins)
				pygame.draw.arc(screen, white, mSquareForCircles, mCircleStartingRadiant, mCircleEndingRadiant, arcWidth)
				mCircleStartingRadiant += mCircleArcIncrement
				mCircleEndingRadiant += mCircleArcIncrement
			mIncrement += 1
			if mIncrement > 1800:
				mCircleActive = False
				gameActive = False
				failed = True
				tooMany = font.render("Too many rotations!", True, (255, 255, 255))
				screen.blit(tooMany, (800 - tooMany.get_width()/2, 320 - tooMany.get_height()/2))
			pygame.display.flip()
			frame.tick(180)

		frame.tick(5)
		largeCircle = drawPinnedCircle(1, 60, red, blue, lSquareForCircles, [])
		lCircleStartingRadiant = 0
		lCircleEndingRadiant = pi/30
		lCircleArcIncrement = pi/30
		lIncrement = 0
		while lCircleActive == True:
			pygame.event.pump()
			pressedKeys = pygame.key.get_pressed()
			if pressedKeys[pygame.K_SPACE]:
				lCircleActive = False
				xlCircleActive = True
				break
			if lIncrement % 2 == 0:
				drawPinnedCircle(largeCircle.numberOfPins, largeCircle.numberOfArcs, largeCircle.color1, largeCircle.color2, largeCircle.areaForCircle, mediumCircle.pins)
				pygame.draw.arc(screen, white, lSquareForCircles, lCircleStartingRadiant, lCircleEndingRadiant, arcWidth)
				lCircleStartingRadiant -= lCircleArcIncrement
				lCircleEndingRadiant -= lCircleArcIncrement
			lIncrement += 1
			if lIncrement > 1800:
				lCircleActive = False
				gameActive = False
				failed = True
				tooMany = font.render("Too many rotations!", True, (255, 255, 255))
				screen.blit(tooMany, (800 - tooMany.get_width()/2, 320 - tooMany.get_height()/2))
			pygame.display.flip()
			frame.tick(180)

		frame.tick(5)
		xlCircle = drawPinnedCircle(1, 120, red, blue, xlSquareForCircles, [])
		xlCircleStartingRadiant = 0
		xlCircleEndingRadiant = pi/60
		xlCircleArcIncrement = pi/60
		xlIncrement = 0
		while xlCircleActive == True:
			pygame.event.pump()
			pressedKeys = pygame.key.get_pressed()
			if pressedKeys[pygame.K_SPACE]:
				xlCircleActive = False
				xsCircleActive = True
				break
			drawPinnedCircle(xlCircle.numberOfPins, xlCircle.numberOfArcs, xlCircle.color1, xlCircle.color2, xlCircle.areaForCircle, xlCircle.pins)
			pygame.draw.arc(screen, white, xlSquareForCircles, xlCircleStartingRadiant, xlCircleEndingRadiant, arcWidth)
			xlCircleStartingRadiant += xlCircleArcIncrement
			xlCircleEndingRadiant += xlCircleArcIncrement
			xlIncrement += 1
			if xlIncrement > 2100:
				xlCircleActive = False
				gameActive = False
				failed = True
				tooMany = font.render("Too many rotations!", True, (255, 255, 255))
				screen.blit(tooMany, (800 - tooMany.get_width()/2, 320 - tooMany.get_height()/2))
			pygame.display.flip()
			frame.tick(240)