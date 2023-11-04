from OpenGL.GL.shaders import fragment_shader, vertex_shader
import pygame
from pygame.locals import * 
from gl import Renderer
from model import Model
from shaders import *
import glm

width = 1920
height = 1080

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShader(vertexShader = starman_vertex, 
			   fragmentShader = starman_fragment)


model = Model("models/model.obj")
model.loadTexture("textures/model.bmp")
model.position.z = -5
rend.scene.append(model)

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

	if keys[K_d]:
		rend.camPosition.x -= 5 * deltaTime
	
	if keys[K_a]:
		rend.camPosition.x += 5 * deltaTime

	if keys[K_w]:
		rend.camPosition.y -= 5 * deltaTime
	
	if keys[K_s]:
		rend.camPosition.y += 5 * deltaTime

	if keys[K_q]:
		rend.camPosition.z -= 5 * deltaTime
	
	if keys[K_e]:
		rend.camPosition.z += 5 * deltaTime

	model.rotation.y += 45 * deltaTime

	rend.elapsedTime += deltaTime

	rend.render()

	pygame.display.flip()

pygame.quit()