import pygame
from pygame.locals import * 
from gl import Renderer
from buffer import Buffer 

width = 1920
height = 1080

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

triangle = [-0.5, -0.5, 0.0,
			 0.0,  0.5, 0.0,
			 0.5, -0.5, 0.0]

rend.scene.append(Buffer(triangle))



isRunning = True

while isRunning:

	# 60 FPS
	deltaTime = clock.tick(60) / 1000

	# Lista de teclas presionadas
	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		# Presiona la x
		if event.type == pygame.QUIT:
			isRunning = False

		# Presiona la tecla esc
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False

	if keys[K_RIGHT]:
		if rend.clearColor[0] < 1.0:
			rend.clearColor[0] += deltaTime
	
	if keys[K_LEFT]:
		if rend.clearColor[0] > 0.0:
			rend.clearColor[0] -= deltaTime

	if keys[K_UP]:
		if rend.clearColor[1] < 1.0:
			rend.clearColor[1] += deltaTime
	
	if keys[K_DOWN]:
		if rend.clearColor[1] > 0.0:
			rend.clearColor[1] -= deltaTime

	if keys[K_x]:
		if rend.clearColor[2] < 1.0:
			rend.clearColor[2] += deltaTime
	
	if keys[K_z]:
		if rend.clearColor[2] > 0.0:
			rend.clearColor[2] -= deltaTime

	rend.render()

	pygame.display.flip()

pygame.quit()