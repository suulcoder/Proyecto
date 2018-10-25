import pymongo

conexion = pymongo.MongoClient()
db = conexion.Learn4
coleccion = db.Usuarios

class Usuario:
	username = 'guest'
	nombres = ''
	apellidos = ''
	email = ''
	clave = ''

	def __init__(self, username, nombres, apellidos, email, clave):
		self.username = username
		self.nombres = nombres
		self.apellidos = apellidos
		self.email = email
		self.clave = clave
		

	def getUsername(self):
		return(self.username)

	def getNombres(self):
		return(self.nombres)

	def getApellidos(self):
		return(self.apellidos)

	def getEmai(self):
		return(self.email)

	def setUsername(self, Username):
		self.username = username


	def setNombres(self, nombres):
		self.nombres = nombres

	def setApellidos(self, apellidos):
		self.apellidos = apellidos

	def setClave(self, Clave):
		self.clave = Clave
		

class Maestro(Usuario):

	CursosAdministrados = []
	CursosInscritos = []

	def __init__(self,username, nombres, apellidos, email, clave):
		Usuario.__init__(self, username, nombres, apellidos, email, clave)
		self.CursosAdministrados=[]
		diccionario = {'username': username, 'Tipo':'Alumno','nombres': nombres,'apellidos':apellidos,'email':email,'clave':clave, 'CursosInscritos' : CursosInscritos, 'CursosAdministrados': CursosAdministrados}		
		coleccion.insert(diccionario)
		

class Alumno(Usuario):

	CursosInscritos = []

	def __init__(self,username, nombres, apellidos, email, clave):
		Usuario.__init__(self,username, nombres, apellidos, email, clave)
		diccionario = {'username': username, 'Tipo':'Maestro','nombres': nombres,'apellidos':apellidos,'email':email,'clave':clave, 'CursosInscritos' : self.CursosInscritos}		
		coleccion.insert(diccionario)