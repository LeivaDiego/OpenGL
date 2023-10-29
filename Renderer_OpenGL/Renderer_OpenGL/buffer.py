from OpenGL.GL import *
from numpy import array, float32

class Buffer(object):

	def __init__(self, data):
		# Constructor del Buffer

		self.vertexBuffer = array(data, dtype = float32)
		
		# Vertex Buffer Object
		self.VBO = glGenBuffers(1)

		# Vertex Array Object
		self.VAO = glGenVertexArrays(1)


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

		# Atributos
		# Especificar que representa el contenido del vertice
		glVertexAttribPointer(index = 0,						# Attribute Number
							  size	= 3,						# Attribute Size		
							  type	= GL_FLOAT,					# Attribute Type
							  normalized = GL_FALSE,			# Is it Normalized
							  stride = 4 * 3,					# Stride
							  pointer = ctypes.c_void_p(0))		# Offset

		glEnableVertexAttribArray(0)

		# Dibujar en la pantalla
		glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertexBuffer / 3)))