class Obj(object):
	def __init__(self, filename):
		# Constructor de la clase Obj

		# Abrir y leer el archivo .obj
		with open(filename, "r") as file:
			self.lines = file.read().splitlines()
	
		# Inicializar listas para almacenar los datos del modelo
		self.vertices = []  # Almacena los vertices
		self.texcoords = [] # Almacena las coordenadas de textura
		self.normals = []   # Almacena las normales
		self.faces = []     # Almacena las caras

		# Procesar cada linea del archivo .obj
		for line in self.lines:

			# Ignorar lineas vacias o sin suficiente informacion
			try:
				prefix, value = line.split(" ", 1)
			except: # Si encuentra una linea vacia, se pasa a la siguiente linea
				continue
			
			# Parsear la informacion basada en el prefijo
			if prefix == "v": # Vertices
				self.vertices.append(list(map(float, value.split(" "))))
			elif prefix == "vt": # Coordenadas de textura
				uvw = list(map(float, value.split(" ")))
				self.texcoords.append(uvw[:2])
			elif prefix == "vn": # Normales
				self.normals.append(list(map(float, value.split(" "))))
			if prefix == "f": # Caras
				self.faces.append([list(map(int, vert.split("/"))) for vert in value.split(" ")])

		# Convertir datos del .obj a un formato adecuado para OpenGL
		self.data = self.get_model_data()

	def get_model_data(self):
		# Convertir los datos del .obj a un array intercalado

		data = []

		# Procesar cada cara y extraer los datos necesarios
		for face in self.faces:
			for vert in face:
				# Obtener las coordenadas del vertice
				vertex_index = vert[0] - 1
				vertex_coords = self.vertices[vertex_index]

				# Inicializar valores por defecto para texturas y normales
				texture_coords = (0, 0)  # Coordenadas de textura por defecto
				normal_coords = (0, 0, 0)  # Coordenadas normales por defecto

				# Obtener las coordenadas de textura si estan disponibles
				if len(vert) > 1 and vert[1] > 0:
					texture_coords = self.texcoords[vert[1] - 1]

				# Obtener las coordenadas normales si estan disponibles
				if len(vert) > 2 and vert[2] > 0:
					normal_coords = self.normals[vert[2] - 1]

				# Agregar los datos al array final
				data.extend(vertex_coords)
				data.extend(texture_coords)
				data.extend(normal_coords)

		return data  # Retornar los datos procesados

