import glm # Libreria de matematicas compatible con OpenGL
from OpenGL.GL import * # Libreria OpenGL compatible con Python
from OpenGL.GL.shaders import compileProgram, compileShader

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

		# Matriz de Vista
		self.camPosition = glm.vec3(0, 0, 0) # Posicion de la camara
		self.camRotation = glm.vec3(0, 0, 0) # Rotacion de la camara

		# Matriz de Proyeccion
		self.projectionMatirx = glm.perspective(glm.radians(60),          # FOV (campo de vision)
												self.width / self.height, # Aspect Ratio (relacion de aspecto)
												0.1,                      # Near Plane (plano cercano)
												1000)                     # Far Plane (plano lejano)

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

	def render(self):
		# Renderizado de la escena

		glClearColor(*self.clearColor, 1) # Color de limpieza del fondo
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpiar buffers

		if self.activeShader is not None:
			glUseProgram(self.activeShader)

			# Configurar matrices de vista, proyeccion y camara en el shader
			glUniformMatrix4fv(glGetUniformLocation(self.activeShader,"viewMatrix"),
							   1, GL_FALSE, glm.value_ptr(self.getViewMatrix()))

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
