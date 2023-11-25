# Importacion de las bibliotecas necesarias
from OpenGL.GL.shaders import fragment_shader, vertex_shader
from OpenGL.GL import *
import pygame
from pygame.locals import * 
from gl import Renderer
from model import Model
from shaders import *
import glm
import math


# Configuracion inicial de las dimensiones de la ventana
width = 1920
height = 1080

# Inicializacion de Pygame
pygame.init()

# Creacion de la ventana con soporte para OpenGL y doble buffer
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
# Reloj para control de FPS
clock = pygame.time.Clock()

# Creacion del objeto Renderer
rend = Renderer(screen)

skyboxTextures = ["skybox/right.jpg",
				  "skybox/left.jpg",
				  "skybox/top.jpg",
				  "skybox/bottom.jpg",
				  "skybox/front.jpg",
				  "skybox/back.jpg"]

rend.createSkybox(skyboxTextures, skybox_vertex, skybox_fragment)

# Establecimiento de los shaders para el renderizado
rend.setShader(vertexShader = vertex_shader, 
			   fragmentShader = fragment_shader)

current_model = 0
current_shader_pair = 0

models = []

# Carga y configuracion del modelos
mario = Model("models/mario.obj")
mario.loadTexture("textures/mario.jpg")
mario.position.z = -7.5
models.append(mario)

luigi = Model("models/luigi.obj")
luigi.loadTexture("textures/luigi.jpg")
luigi.position.z = -7.5
models.append(luigi)

goomba = Model("models/goomba.obj")
goomba.loadTexture("textures/goomba.png")
goomba.position.z = -7.5
models.append(goomba)

bill = Model("models/bill.obj")
bill.loadTexture("textures/bill.png")
bill.position.z = -7.5
models.append(bill)


# Anadir el modelo a la escena
rend.scene.append(models[current_model])

rend.target.z = -7.5

# Variable para controlar el ciclo principal
isRunning = True

# Variables para el seguimiento del movimiento del mouse
mouse_dragging = False
last_mouse_position = None


# Mapeo de teclas a combinaciones de shaders
shader_pairs = [
	(vertex_shader, fragment_shader),
	(minecraft_vertex, fragment_shader),
	(vertex_shader, glow_shader),
	(minecraft_vertex, glow_shader),
	(vertex_shader, hologram_shader),
	(minecraft_vertex, hologram_shader),
	(vertex_shader, psycho_shader),
	(minecraft_vertex, psycho_shader)
]


def change_model(direction):
	global current_model
	if direction == "next":
		current_model = (current_model + 1) % len(models)
	elif direction == "previous":
		current_model = (current_model - 1) % len(models)

	rend.scene.clear()
	rend.scene.append(models[current_model])


def change_shader_pair(direction):
	global current_shader_pair
	if direction == "next":
		current_shader_pair = (current_shader_pair + 1) % len(shader_pairs)
	elif direction == "previous":
		current_shader_pair = (current_shader_pair - 1) % len(shader_pairs)

	vertex_shader, fragment_shader = shader_pairs[current_shader_pair]
	rend.setShader(vertexShader=vertex_shader, fragmentShader=fragment_shader)

movement_sensitive = 0.1
sens_x = 0.2
sens_y = 0.2
distance = abs(rend.camPosition.z - models[current_model].position.z)
radius = distance
zoom_sensitive = 0.5
angle = 0.0
angle_y = 0.0


# Bucle principal
while isRunning:

	# Configuracion de 60 FPS
	deltaTime = clock.tick(60) / 1000
	
	# Actualizacion de la posicion de la camara en X y Z
	rend.camPosition.x = math.sin(math.radians(angle)) * radius + models[current_model].position.x
	rend.camPosition.z = math.cos(math.radians(angle)) * radius + models[current_model].position.z

	# Actualizacion de la posicion de la camara en Y
	rend.camPosition.y = math.sin(math.radians(angle_y)) * radius + models[current_model].position.y

	# Lista de teclas presionadas
	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		# Evento de salida
		if event.type == pygame.QUIT:
			isRunning = False

		# Evento para cerrar con la tecla ESC
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False

			if event.key == pygame.K_UP:
				change_shader_pair("previous")

			if event.key == pygame.K_DOWN:
				change_shader_pair("next")
				
			if event.key == pygame.K_LEFT:
				change_model("previous")

			if event.key == pygame.K_RIGHT:
				change_model("next")
				

		# Inicio de la rotacion del camara con el mouse
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: 
				mouse_dragging = True
				last_mouse_position = pygame.mouse.get_pos()

		# Fin de la rotacion del camara con el mouse
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:  
				mouse_dragging = False

		# Rotacion de camara basada en mouse input
		elif event.type == pygame.MOUSEMOTION:
			if mouse_dragging:
				new_position = pygame.mouse.get_pos()
				deltax = new_position[0] - last_mouse_position[0]
				deltay = new_position[1] - last_mouse_position[1]

				angle += deltax * -sens_x
				angle_y += deltay * sens_y

				if angle > 360:
					angle = 0
				if angle_y > 360:
					angle_y = 0

				last_mouse_position = new_position

		# Zoom de la camara con la rueda del mouse
		elif event.type == pygame.MOUSEWHEEL:
			if event.y > 0 and radius > distance * 0.5:
				radius -= zoom_sensitive
			elif event.y < 0 and radius < distance * 1.5:
				radius += zoom_sensitive
		
		# Aumentar pixelSize
		if keys[pygame.K_w]:
			rend.pixelSize += 0.1
			rend.pixelSize = min(rend.pixelSize, 0.8)  # Asegurar que no exceda 0.8

		# Disminuir pixelSize
		if keys[pygame.K_s]:
			rend.pixelSize -= 0.1
			rend.pixelSize = max(rend.pixelSize, 0.1)  # Asegurar que no sea menor que 0.1


	# Actualizar el tiempo transcurrido y renderizar la escena
	rend.elapsedTime += deltaTime
	rend.update()
	rend.render()

	# Actualizar la pantalla
	pygame.display.flip()

# Finalizar Pygame al salir del bucle
pygame.quit()
