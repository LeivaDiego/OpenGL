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

# Establecimiento de los shaders para el renderizado
rend.setShader(vertexShader = vertex_shader, 
			   fragmentShader = fragment_shader)

# Carga y configuracion del modelo
model = Model("models/mario.obj")
model.loadTexture("textures/mario.jpg")
model.position.z = -7.5

# Anadir el modelo a la escena
rend.scene.append(model)

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

				model.rotation.y += dx * 0.2
				model.rotation.x += dy * 0.2

				last_mouse_position = mouse_position
	

	# Movimiento de la camara con las teclas WASDQE
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

	# Rotacion automatica del modelo
	model.rotation.y += 45 * deltaTime

	# Actualizar el tiempo transcurrido y renderizar la escena
	rend.elapsedTime += deltaTime
	rend.render()

	# Actualizar la pantalla
	pygame.display.flip()

# Finalizar Pygame al salir del bucle
pygame.quit()
