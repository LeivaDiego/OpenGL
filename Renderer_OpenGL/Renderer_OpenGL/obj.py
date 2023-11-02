class Obj(object):
	def __init__(self, filename):

		# Asumiendo que el archivo es un formato .obj
		with open(filename,"r") as file:
			self.lines = file.read().splitlines()
	
		# Se crean los contenedores de los datos del modelo
		self.vertices = []
		self.texcoords = []
		self.normals = []
		self.faces = []

		# Por cada linea en el archivo
		for line in self.lines:

			# Si la linea no cuenta con un prefijo y un valor,
			# seguimos a la siguiente linea
			try:
				prefix, value = line.split(" ",1)
			except: # si encuentra una linea vacia, se pasa a la siguiente linea
				continue
			
			# Dependiendo del prefijo, parseamos y guardamos la informacion
			# en el contenedor correcto
			if prefix == "v": # Vertices
				self.vertices.append(list(map(float,value.split(" "))))
			elif prefix == "vt": # Texture coordinates
				uvw = list(map(float,value.split(" ")))
				self.texcoords.append(uvw[:2])
			elif prefix == "vn": # Normals
				self.normals.append(list(map(float,value.split(" "))))
			if prefix == "f": # Faces
				self.faces.append([list(map(int, vert.split("/"))) for vert in value.split(" ")])

		self.data = self.get_model_data()

	def get_model_data(self):
		# Convierte los arrays del .obj a un unico array intercalado
		data = []

		# Se procesa cada cara y se extraen los datos
		for face in self.faces:
			for vert in face:
				# Se obtienen las coordenadas del vertice
				vertex_index = vert[0] - 1
				vertex_coords = self.vertices[vertex_index]

				# Se inicializan los placeholders para las texturas y normales
				texture_coords = (0, 0)  # Placeholder para las texturas
				normal_coords = (0, 0, 0)  # Placeholder para las normales

				# Se obtienen las coordenadas de la textura si existen
				if len(vert) > 1 and vert[1] > 0:
					texture_coords = self.texcoords[vert[1] - 1]

				# Se obtienen las normales si existen
				if len(vert) > 2 and vert[2] > 0:
					normal_coords = self.normals[vert[2] - 1]

				# Se agregan los datos a la lista plana
				data.extend(vertex_coords)
				data.extend(texture_coords)
				data.extend(normal_coords)

		return data
