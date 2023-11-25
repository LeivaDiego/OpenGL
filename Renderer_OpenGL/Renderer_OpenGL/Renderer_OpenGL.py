# Importacion de las bibliotecas necesarias
from OpenGL.GL.shaders import fragment_shader, vertex_shader
from OpenGL.GL import *
import pygame
from pygame.locals import * 
from gl import Renderer
from model import Model
from shaders import *
import glm

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

models = []

# Carga y configuracion del modelo

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
shaders_mapping = {
	pygame.K_1: (vertex_shader, fragment_shader),
	pygame.K_2: (minecraft_vertex, fragment_shader),
	pygame.K_3: (vertex_shader, glow_shader),
	pygame.K_4: (minecraft_vertex, glow_shader),
	pygame.K_5: (vertex_shader, hologram_shader),
	pygame.K_6: (minecraft_vertex, hologram_shader),
	pygame.K_7: (vertex_shader, psycho_shader),
	pygame.K_8: (minecraft_vertex, psycho_shader)
}


def change_model(direction):
	global current_model
	if direction == "next":
		current_model = (current_model + 1) % len(models)
	elif direction == "previous":
		current_model = (current_model - 1) % len(models)

	rend.scene.clear()
	rend.scene.append(models[current_model])


# Bucle principal
while isRunning:

	# Configuracion de 60 FPS
	deltaTime = clock.tick(60) / 1000

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

			if event.key in shaders_mapping:
				# Cambia los shaders segun la tecla presionada
				vertex_shader, fragment_shader = shaders_mapping[event.key]
				rend.setShader(vertexShader=vertex_shader, fragmentShader=fragment_shader)
				
			if event.key == pygame.K_LEFT:
				change_model("previous")

			# Cambiar al modelo siguiente con la flecha derecha
			if event.key == pygame.K_RIGHT:
				change_model("next")

		# Inicio de la rotacion del modelo con el mouse
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1: 
				mouse_dragging = True
				last_mouse_position = pygame.mouse.get_pos()

		# Fin de la rotacion del modelo con el mouse
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:  
				mouse_dragging = False

		# Movimiento del mouse para rotar el modelo
		elif event.type == pygame.MOUSEMOTION:
			if mouse_dragging:
				mouse_position = pygame.mouse.get_pos()
				dx = mouse_position[0] - last_mouse_position[0]
				dy = mouse_position[1] - last_mouse_position[1]

				goomba.rotation.y += dx * 0.2
				goomba.rotation.x += dy * 0.2

				last_mouse_position = mouse_position
			
		elif event.type == pygame.MOUSEWHEEL:
			rend.camPosition.z += event.y


	# Actualizar el tiempo transcurrido y renderizar la escena
	rend.elapsedTime += deltaTime
	rend.update()
	rend.render()

	# Actualizar la pantalla
	pygame.display.flip()

# Finalizar Pygame al salir del bucle
pygame.quit()
