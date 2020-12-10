import pygame
import sys, pygame

pygame.init()

size = width, height = 1000, 800
black = 0, 0, 0

#placing things on the table
line = []
#0 for face up, 1 for face down
pool = [("1", 0), ("2", 0), ("3", 0), ("4", 0), ("5", 0), ("6", 0), ("7", 0)]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Client")

ClientNumber = 0
	
def makeWindow():
	win.fill((0, 255, 0))
	pygame.display.update()
	
def main():
	run = True
	
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

		makeWindow()