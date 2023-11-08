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

rend.setShader(vertexShader = vertex_shader, 
			   fragmentShader = psycho_shader)


model = Model("models/model.obj")
model.loadTexture("textures/model.bmp")
model.position.z = -6
model.scale = glm.vec3(2,2,2)

rend.scene.append(model)

isRunning = True


# Variables para el seguimiento del movimiento del mouse
mouse_dragging = False
last_mouse_position = None

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

		# Rotacion del modelo mediante mouse-drag
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: 
				mouse_dragging = True
				last_mouse_position = pygame.mouse.get_pos()

		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:  
				mouse_dragging = False

		elif event.type == pygame.MOUSEMOTION:
			if mouse_dragging:
				mouse_position = pygame.mouse.get_pos()
				dx = mouse_position[0] - last_mouse_position[0]
				dy = mouse_position[1] - last_mouse_position[1]

				model.rotation.y += dx * 0.2
				model.rotation.x += dy * 0.2

				last_mouse_position = mouse_position


	# Movimiento de camara en los ejes x, y, z
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

	model.rotation.y  += 25 * deltaTime

	rend.elapsedTime += deltaTime

	rend.render()

	pygame.display.flip()

pygame.quit()