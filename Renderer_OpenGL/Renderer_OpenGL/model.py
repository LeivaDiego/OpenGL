from numpy import array, float32
from OpenGL.GL import *
import pygame
import glm
from obj import Obj

class Model(object):

	def __init__(self, file):

		self.obj = Obj(file)
		self.data = self.obj.get_model_data()

		# Constructor del Buffer
		self.vertexBuffer = array(self.data, dtype = float32)
		
		# Vertex Buffer Object
		self.VBO = glGenBuffers(1)

		# Vertex Array Object
		self.VAO = glGenVertexArrays(1)

		# Transformaciones
		self.position = glm.vec3(0,0,0)
		self.rotation = glm.vec3(0,0,0)
		self.scale = glm.vec3(1,1,1)


	def loadTexture(self, texturePath):
		self.textureSurface = pygame.image.load(texturePath)
		self.textureData	= pygame.image.tostring(self.textureSurface, "RGB", True)
		self.textureBuffer	= glGenTextures(1)


	def getModelMatrix(self):
		identity = glm.mat4(1)

		translationMatrix = glm.translate(identity, self.position)

		pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))		# Rotacion en X (pitch)
		yaw	  = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))		# Rotacion en Y (yaw)
		roll  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))		# Rotacion en Z (roll)

		rotationMatrix = pitch * yaw * roll

		scaleMatrix = glm.scale(identity, self.scale)

		return translationMatrix * rotationMatrix * scaleMatrix


	def render(self):
		# Renderizado del objeto
		
		# Atar los buffers delk objeto a la GPU
		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		glBindVertexArray(self.VAO)

		# Especificar la informacion de vertices
		glBufferData(target = GL_ARRAY_BUFFER,				# Buffer ID
					 size = self.vertexBuffer.nbytes,		# Buffer Size (bytes)
					 data = self.vertexBuffer,				# Buffer Data
					 usage = GL_STATIC_DRAW)                # Usage


		# ATRIBUTOS		
		
		# Atributo de Vertices
		# Especificar que representa el contenido del vertice
		glVertexAttribPointer(index = 0,						# Attribute Number
							  size	= 3,						# Attribute Size		
							  type	= GL_FLOAT,					# Attribute Type
							  normalized = GL_FALSE,			# Is it Normalized
							  stride = 4 * 8,					# Stride
							  pointer = ctypes.c_void_p(0))		# Offset
		# Activacion de atributo
		glEnableVertexAttribArray(0)


		# Atributo de UVs (textura)
		glVertexAttribPointer(index = 1,						# Attribute Number
							  size	= 2,						# Attribute Size		
							  type	= GL_FLOAT,					# Attribute Type
							  normalized = GL_FALSE,			# Is it Normalized
							  stride = 4 * 8,					# Stride
							  pointer = ctypes.c_void_p(4 * 3))	# Offset
		# Activacion de atributo
		glEnableVertexAttribArray(1)


		# Atributo de normales
		glVertexAttribPointer(index = 2,						# Attribute Number
							  size	= 3,						# Attribute Size		
							  type	= GL_FLOAT,					# Attribute Type
							  normalized = GL_FALSE,			# Is it Normalized
							  stride = 4 * 8,					# Stride
							  pointer = ctypes.c_void_p(4 * 5))	# Offset
		# Activacion de atributo
		glEnableVertexAttribArray(2)


		# Activar la textura del modelo
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.textureBuffer)
		glTexImage2D(GL_TEXTURE_2D,							# Texture Type
					 0,										# Positions
					 GL_RGB,								# Internal Format
					 self.textureSurface.get_width(),		# Width
					 self.textureSurface.get_height(),		# Height
					 0,										# Border
					 GL_RGB,								# Format
					 GL_UNSIGNED_BYTE,						# Type
					 self.textureData)						# Data

		glGenerateTextureMipmap(self.textureBuffer)


		# Dibujar en la pantalla
		glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertexBuffer / 8)))