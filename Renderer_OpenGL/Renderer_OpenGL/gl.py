from pickletools import pybool
import glm # Libreria de matematicas compatible con OpenGL
from OpenGL.GL import * # Libreria OpenGL compatible con Python
from OpenGL.GL.shaders import compileProgram, compileShader
from numpy import array, float32
import pygame

class Renderer(object):

	def __init__(self, screen):
		# Constructor del Renderer

		self.screen = screen
		_, _, self.width, self.height = screen.get_rect()

		self.clearColor = [0, 0, 0] # Color de fondo RGB
		
		glEnable(GL_DEPTH_TEST) # Habilitar prueba de profundidad
		glEnable(GL_CULL_FACE) # Habilitar culling de caras
		glCullFace(GL_BACK) # Descartar caras traseras
		glEnable(GL_BLEND) # Habilitar mezcla de colores
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # Configurar funcion de mezcla
		
		glViewport(0, 0, self.width, self.height) # Configurar el viewport

		self.scene = [] # Lista para almacenar objetos de la escena

		self.elapsedTime = 0.0 # Tiempo transcurrido
		
		self.activeShader = None # Shader activo
		self.skyboxShader = None # Shader de la skybox
		
		# Matriz de Vista
		self.camPosition = glm.vec3(0, 0, 0) # Posicion de la camara
		self.camRotation = glm.vec3(0, 0, 0) # Rotacion de la camara
		
		self.viewMatrix = self.getViewMatrix()
		self.camMatrix = self.getCamMatrix()
		
		# Camara
		self.target = glm.vec3(0,0,0)

		# Matriz de Proyeccion
		self.projectionMatirx = glm.perspective(glm.radians(60),          # FOV (campo de vision)
												self.width / self.height, # Aspect Ratio (relacion de aspecto)
												0.1,                      # Near Plane (plano cercano)
												1000)                     # Far Plane (plano lejano)


	def createSkybox(self, texturesList, vertexShader, fragmentShader):
		skyboxBuffer = [-1.0,  1.0, -1.0,
						-1.0, -1.0, -1.0,
						 1.0, -1.0, -1.0,
						 1.0, -1.0, -1.0,
						 1.0,  1.0, -1.0,
						-1.0,  1.0, -1.0,

						-1.0, -1.0,  1.0,
						-1.0, -1.0, -1.0,
						-1.0,  1.0, -1.0,
						-1.0,  1.0, -1.0,
						-1.0,  1.0,  1.0,
						-1.0, -1.0,  1.0,

						 1.0, -1.0, -1.0,
						 1.0, -1.0,  1.0,
						 1.0,  1.0,  1.0,
						 1.0,  1.0,  1.0,
						 1.0,  1.0, -1.0,
						 1.0, -1.0, -1.0,

						-1.0, -1.0,  1.0,
						-1.0,  1.0,  1.0,
						 1.0,  1.0,  1.0,
						 1.0,  1.0,  1.0,
						 1.0, -1.0,  1.0,
						-1.0, -1.0,  1.0,

						-1.0,  1.0, -1.0,
						 1.0,  1.0, -1.0,
						 1.0,  1.0,  1.0,
						 1.0,  1.0,  1.0,
						-1.0,  1.0,  1.0,
						-1.0,  1.0, -1.0,

						-1.0, -1.0, -1.0,
						-1.0, -1.0,  1.0,
						 1.0, -1.0, -1.0,
						 1.0, -1.0, -1.0,
						-1.0, -1.0,  1.0,
						 1.0, -1.0,  1.0
						]
		
		self.skyboxVertBuffer = array(skyboxBuffer, dtype = float32)
		self.skyboxVBO = glGenBuffers(1)
		self.skyboxVAO = glGenVertexArrays(1)
		
		self.skyboxShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
											compileShader(fragmentShader, GL_FRAGMENT_SHADER))
		
		self.skyboxTexture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_CUBE_MAP, self.skyboxTexture)
		
		for i in range(len(texturesList)): # 6 texturas
			texture = pygame.image.load(texturesList[i])
			textureData = pygame.image.tostring(texture, "RGB", False)
			
			glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,	# Texture Type
					 0,											# Positions
					 GL_RGB,									# Internal Format
					 texture.get_width(),						# Width
					 texture.get_height(),						# Height
					 0,											# Border
					 GL_RGB,									# Format
					 GL_UNSIGNED_BYTE,							# Type
					 textureData)
			
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
		glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)


		

	def renderSkybox(self):
		
		if self.skyboxShader == None:
			return

		glDepthMask(GL_FALSE)		

		glUseProgram(self.skyboxShader)
		
		skyboxViewMatrix = glm.mat4(glm.mat3(self.viewMatrix))
		
		glUniformMatrix4fv(glGetUniformLocation(self.skyboxShader, "viewMatrix"),
							   1, GL_FALSE, glm.value_ptr(skyboxViewMatrix))

		glUniformMatrix4fv(glGetUniformLocation(self.skyboxShader, "projectionMatrix"),
							   1, GL_FALSE, glm.value_ptr(self.projectionMatirx))

		glBindBuffer(GL_ARRAY_BUFFER, self.skyboxVBO)
		glBindVertexArray(self.skyboxVAO)
		
		glBufferData(target = GL_ARRAY_BUFFER,                
					 size = self.skyboxVertBuffer.nbytes,
					 data = self.skyboxVertBuffer,  
					 usage = GL_STATIC_DRAW)               

		glVertexAttribPointer(index = 0,                       
							  size = 3,                         
							  type = GL_FLOAT,                
							  normalized = GL_FALSE,
							  stride = 4 * 3,                 							  
							  pointer = ctypes.c_void_p(0))   	
		
		glEnableVertexAttribArray(0) 
		
		glBindTexture(GL_TEXTURE_CUBE_MAP, self.skyboxTexture)
		
		glDrawArrays(GL_TRIANGLES, 0, 36)
		
		glDepthMask(GL_TRUE)
	


	def getViewMatrix(self):
		# Obtener la matriz de vista

		identity = glm.mat4(1) # Matriz identidad

		translationMatrix = glm.translate(identity, self.camPosition) # Matriz de traslacion

		# Rotaciones en los ejes X, Y, Z
		pitch = glm.rotate(identity, glm.radians(self.camRotation.x), glm.vec3(1, 0, 0)) # Rotacion en X (pitch)
		yaw   = glm.rotate(identity, glm.radians(self.camRotation.y), glm.vec3(0, 1, 0)) # Rotacion en Y (yaw)
		roll  = glm.rotate(identity, glm.radians(self.camRotation.z), glm.vec3(0, 0, 1)) # Rotacion en Z (roll)

		rotationMatrix = pitch * yaw * roll

		camMatrix = translationMatrix * rotationMatrix

		return glm.inverse(camMatrix) # Retorna la inversa de la matriz de camara



	def getCamMatrix(self):
		# Obtener la matriz de la camara

		identity = glm.mat4(1) # Matriz identidad

		translationMatrix = glm.translate(identity, self.camPosition) # Matriz de traslacion

		# Rotaciones en los ejes X, Y, Z
		pitch = glm.rotate(identity, glm.radians(self.camRotation.x), glm.vec3(1, 0, 0)) # Rotacion en X (pitch)
		yaw   = glm.rotate(identity, glm.radians(self.camRotation.y), glm.vec3(0, 1, 0)) # Rotacion en Y (yaw)
		roll  = glm.rotate(identity, glm.radians(self.camRotation.z), glm.vec3(0, 0, 1)) # Rotacion en Z (roll)

		rotationMatrix = pitch * yaw * roll

		camMatrix = translationMatrix * rotationMatrix

		return camMatrix # Retorna la matriz de camara
	


	def setShader(self, vertexShader, fragmentShader):
		# Configurar el shader activo

		if vertexShader is not None and fragmentShader is not None:
			self.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
											   compileShader(fragmentShader, GL_FRAGMENT_SHADER))
		else:
			self.activeShader = None


	def update(self):
		self.viewMatrix = glm.lookAt(self.camPosition, self.target, glm.vec3(0,1,0))
		

	def render(self):
		# Renderizado de la escena

		glClearColor(*self.clearColor, 1) # Color de limpieza del fondo
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpiar buffers

		self.renderSkybox()

		if self.activeShader is not None:
			glUseProgram(self.activeShader)

			# Configurar matrices de vista, proyeccion y camara en el shader
			glUniformMatrix4fv(glGetUniformLocation(self.activeShader,"viewMatrix"),
							   1, GL_FALSE, glm.value_ptr(self.viewMatrix))

			glUniformMatrix4fv(glGetUniformLocation(self.activeShader,"projectionMatrix"),
							   1, GL_FALSE, glm.value_ptr(self.projectionMatirx))

			glUniformMatrix4fv(glGetUniformLocation(self.activeShader,"camMatrix"),
							   1, GL_FALSE, glm.value_ptr(self.getCamMatrix()))

			glUniform1f(glGetUniformLocation(self.activeShader, "time"), self.elapsedTime)

		for obj in self.scene:
			if self.activeShader is not None:
				glUniformMatrix4fv(glGetUniformLocation(self.activeShader,"modelMatrix"),
								   1, GL_FALSE, glm.value_ptr(obj.getModelMatrix()))

			obj.render() # Renderizar cada objeto en la escena
