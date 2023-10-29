import glm # Libreria de matematicas compatible con OpenGl
from OpenGL.GL import * # Libreria OpenGl compatible con python


class Renderer(object):

	def __init__(self, screen):
		# Constructor del Renderer

		self.screen = screen
		_, _, self.width, self.height = screen.get_rect()

		self.clearColor = [0,0,0,1] # RGBA
		
		glEnable(GL_DEPTH_TEST)
		glViewport(0,0,self.width, self.height)

		self.scene = []


	def render(self):
		# Renderizado de la escena

		glClearColor(*self.clearColor)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		for obj in self.scene:
			obj.render()