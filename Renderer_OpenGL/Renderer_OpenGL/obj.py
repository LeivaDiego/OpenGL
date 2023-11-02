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
				self.texcoords.append(list(map(float,value.split(" "))))
			elif prefix == "vn": # Normals
				self.normals.append(list(map(float,value.split(" "))))
			if prefix == "f": # Faces
				self.faces.append([list(map(int, vert.split("/"))) for vert in value.split(" ")])


	def get_model_data(self):
		# Convierte los arrays del .obj a un unico array intercalado

		# Crear listas para datos intercalados
		vertices = []
		texcoords = []
		normals = []

		for face in self.faces:
			for vertex in face:
				# Los indices en un archivo .obj comienzan en 1
				vert_index, tex_index, norm_index = [idx - 1 for idx in vertex]
				vertices.extend(self.vertices[vert_index])
				texcoords.extend(self.texcoords[tex_index])
				normals.extend(self.normals[norm_index])

		# Intercalar los datos
		data = []
		for i in range(len(vertices) // 3):
			data.extend(vertices[i*3:i*3+3])
			data.extend(texcoords[i*2:i*2+2])
			data.extend(normals[i*3:i*3+3])
	
		return data


