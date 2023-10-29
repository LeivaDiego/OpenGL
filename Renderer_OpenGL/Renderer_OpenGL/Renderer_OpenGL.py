import pygame
from pygame.locals import * 

width = 1920
height = 1080

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

isRunning = True

while isRunning:
	for event in pygame.event.get():
		# Presiona la x
		if event.type == pygame.QUIT:
			isRunning = False

		# Presiona la tecla esc
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False
	
	# 60 FPS
	deltaTime = clock.tick(60) / 1000
	
	pygame.display.flip()

pygame.quit()