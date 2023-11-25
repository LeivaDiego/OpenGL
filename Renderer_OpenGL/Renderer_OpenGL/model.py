from numpy import array, float32
from OpenGL.GL import *
import pygame
import glm
from obj import Obj

class Model(object):

	def __init__(self, file):
		# Constructor del Modelo

		self.obj = Obj(file) # Carga del archivo .obj
		self.data = self.obj.data # Datos del objeto

		# Constructor del Buffer
		self.vertexBuffer = array(self.data, dtype = float32) # Buffer de vertices
		
		# Vertex Buffer Object (VBO)
		self.VBO = glGenBuffers(1) # Generacion del VBO

		# Vertex Array Object (VAO)
		self.VAO = glGenVertexArrays(1) # Generacion del VAO

		# Transformaciones
		self.position = glm.vec3(0, 0, 0) # Posicion
		self.rotation = glm.vec3(0, 0, 0) # Rotacion
		self.scale = glm.vec3(1, 1, 1) # Escala


	def loadTexture(self, texturePath):
		# Carga de la textura

		self.textureSurface = pygame.image.load(texturePath) # Cargar superficie de la textura
		self.textureData = pygame.image.tostring(self.textureSurface, "RGB", True) # Datos de la textura
		self.textureBuffer = glGenTextures(1) # Generacion del buffer de textura


	def getModelMatrix(self):
		# Obtener la matriz del modelo

		identity = glm.mat4(1) # Matriz identidad

		translationMatrix = glm.translate(identity, self.position) # Matriz de traslacion

		# Rotaciones en los ejes X, Y, Z
		pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0)) # Rotacion en X (pitch)
		yaw   = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0)) # Rotacion en Y (yaw)
		roll  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1)) # Rotacion en Z (roll)

		rotationMatrix = pitch * yaw * roll

		scaleMatrix = glm.scale(identity, self.scale)

		return translationMatrix * rotationMatrix * scaleMatrix # Retorna la matriz compuesta


	def render(self):
		# Renderizado del modelo

		# Asociar los buffers del objeto a la GPU
		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		glBindVertexArray(self.VAO)

		# Especificar la informacion de vertices
		glBufferData(target = GL_ARRAY_BUFFER,                # Buffer ID
					 size = self.vertexBuffer.nbytes,        # Buffer Size (bytes)
					 data = self.vertexBuffer,               # Buffer Data
					 usage = GL_STATIC_DRAW)                # Usage

		# ATRIBUTOS

		# Atributo de Vertices
		glVertexAttribPointer(index = 0,                      # Attribute Number
							  size = 3,                       # Attribute Size
							  type = GL_FLOAT,                # Attribute Type
							  normalized = GL_FALSE,          # Is it Normalized
							  stride = 4 * 8,                 # Stride
							  pointer = ctypes.c_void_p(0))   # Offset
		glEnableVertexAttribArray(0) # Activar atributo

		# Atributo de UVs (textura)
		glVertexAttribPointer(index = 1,                      # Attribute Number
							  size = 2,                       # Attribute Size
							  type = GL_FLOAT,                # Attribute Type
							  normalized = GL_FALSE,          # Is it Normalized
							  stride = 4 * 8,                 # Stride
							  pointer = ctypes.c_void_p(4 * 3)) # Offset
		glEnableVertexAttribArray(1) # Activar atributo

		# Atributo de normales
		glVertexAttribPointer(index = 2,                      # Attribute Number
							  size = 3,                       # Attribute Size
							  type = GL_FLOAT,                # Attribute Type
							  normalized = GL_FALSE,          # Is it Normalized
							  stride = 4 * 8,                 # Stride
							  pointer = ctypes.c_void_p(4 * 5)) # Offset
		glEnableVertexAttribArray(2) # Activar atributo

		# Activar la textura del modelo
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.textureBuffer)
		glTexImage2D(GL_TEXTURE_2D,                            # Texture Type
					 0,                                       # Positions
					 GL_RGB,                                  # Internal Format
					 self.textureSurface.get_width(),         # Width
					 self.textureSurface.get_height(),        # Height
					 0,                                       # Border
					 GL_RGB,                                  # Format
					 GL_UNSIGNED_BYTE,                        # Type
					 self.textureData)                        # Data

		glGenerateTextureMipmap(self.textureBuffer)

		# Dibujar en la pantalla
		glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertexBuffer) / 8))
