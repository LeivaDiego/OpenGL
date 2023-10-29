import glm # Libreria de matematicas compatible con OpenGl
from OpenGL.GL import * # Libreria OpenGl compatible con python
from OpenGL.GL.shaders import compileProgram, compileShader

class Renderer(object):

	def __init__(self, screen):
		# Constructor del Renderer

		self.screen = screen
		_, _, self.width, self.height = screen.get_rect()

		self.clearColor = [0,0,0] # RGB
		
		glEnable(GL_DEPTH_TEST)
		glViewport(0,0,self.width, self.height)

		self.scene = []

		self.activeShader = None

	def setShader(self, vertexShader, fragmentShader):
		if vertexShader is not None and fragmentShader is not None:
			self.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
											   compileShader(fragmentShader, GL_FRAGMENT_SHADER))
		else:
			self.activeShader = None



	def render(self):
		# Renderizado de la escena

		glClearColor(*self.clearColor, 1)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		if self.activeShader is not None:
			glUseProgram(self.activeShader)

		for obj in self.scene:
			obj.render()