import pymongo

conexion = pymongo.MongoClient()
db = conexion.Learn4
db_users = db.Usuarios
db_cursos = db.Cursos
categorias = []


class User:

    def __init__(self, username, nombres, apellidos, email, clave, tipo):
        self.username = username
        self.nombre = nombres
        self.apellidos = apellidos
        self.email = email
        self.tipo = tipo
        self.clave = clave
        self.state = 'logged in'
        self.id = 1

        #   Cursos
        self.CursosInscritos = []
        self.CursosAdministrados = []

    #   metodos para db / mongo

    def __generate_id(self):
        #   metodos privados
        try:
            self.id = db_users.find().count() +1
            #   de momento solo cuenta usuarios y se agrega. ese
        except Exception as e:
            #   mejorar exceptions
            print(e)
  

    @staticmethod
    def actualizar(username,nombre,apellidos,clave,user):
        datos = db_users.find({'email':user})
        lista = []
        for i in datos:
            lista.append(i['username'])
            lista.append(i['tipo'])
            lista.append(i['nombres'])
            lista.append(i['apellidos'])
            lista.append(i['email'])
            lista.append(i['clave'])
            lista.append(i['CursosInscritos'])
            lista.append(i['CursosAdministrados'])
        diccionario = {}
        diccionario['username'] = username
        diccionario['tipo'] = lista[1]
        diccionario['nombres'] = nombre
        diccionario['apellidos'] = apellidos
        diccionario['email'] = lista[4]
        diccionario['clave'] = clave
        diccionario['CursosInscritos'] = lista[6]
        diccionario['CursosAdministrados'] = lista[7]
        db_users.update({'email':user},diccionario)

    @staticmethod
    def Unirse(user,nombre):
        datos = db_users.find({'email':user})
        lista = []
        for i in datos:
            lista.append(i['username'])
            lista.append(i['tipo'])
            lista.append(i['nombres'])
            lista.append(i['apellidos'])
            lista.append(i['email'])
            lista.append(i['clave'])
            lista.append(i['CursosInscritos'])
            if lista[1] == 'M':
                lista.append(i['CursosAdministrados'])
        curso = db_cursos.find({'nombre':nombre})
        new = lista[6]
        for i in curso:
            new.append(i['id_curso'])
        diccionario = {}
        diccionario['username']= lista[0]
        diccionario['tipo'] = lista[1]
        diccionario['nombres'] = lista[2]
        diccionario['apellidos'] = lista[3]
        diccionario['email'] = lista[4]
        diccionario['clave'] = lista[5]
        diccionario['CursosInscritos'] = new
        if lista[1] == 'M':
            diccionario['CursosAdministrados'] = lista[7]
        db_users.update({'email':user},diccionario)

class Maestro(User):

    def __init__(self, username, nombres, apellidos, email, clave, tipo):
        User.__init__(self, username, nombres, apellidos, email, clave, tipo)
        self.CursosAdministrados = []
        self.CursosInscritos = []
        diccionario = {}
       	diccionario['username']=	self.username
       	diccionario['tipo'] = self.tipo
       	diccionario['nombres'] = self.nombre
       	diccionario['apellidos'] = self.apellidos
       	diccionario['email'] = self.email
       	diccionario['clave'] = self.clave
       	diccionario['CursosInscritos'] = self.CursosInscritos
       	diccionario['CursosAdministrados'] = self.CursosAdministrados
        db_users.insert(diccionario)

    @staticmethod
    def CrearCurso(nombre, departamento, maestro):
        datos = db_users.find({'email':maestro})
        lista = []
        for i in datos:
            lista.append(i['username'])
            lista.append(i['tipo'])
            lista.append(i['nombres'])
            lista.append(i['apellidos'])
            lista.append(i['email'])
            lista.append(i['clave'])
            lista.append(i['CursosInscritos'])
            lista.append(i['CursosAdministrados'])
        curso = Curso(nombre,departamento,maestro)
        ingresar = curso.getId()
        lista[7].append(ingresar)
        diccionario = {}
        diccionario['username']= lista[0]
        diccionario['tipo'] = lista[1]
        diccionario['nombres'] = lista[2]
        diccionario['apellidos'] = lista[3]
        diccionario['email'] = lista[4]
        diccionario['clave'] = lista[5]
        diccionario['CursosInscritos'] = lista[6]
        diccionario['CursosAdministrados'] = lista[7]
        db_users.update({'email':maestro},diccionario)
        return(ingresar)

class Alumno(User):

    def __init__(self, username, nombres, apellidos, email, clave,tipo):
        User.__init__(self, username, nombres, apellidos, email, clave,tipo)
        self.id_curso = int
        diccionario = {}
       	diccionario['username']=	self.username
       	diccionario['tipo'] = self.tipo
       	diccionario['nombres'] = self.nombre
       	diccionario['apellidos'] = self.apellidos
       	diccionario['email'] = self.email
       	diccionario['clave'] = self.clave
       	diccionario['CursosInscritos'] = self.CursosInscritos
       	db_users.insert(diccionario)

class Curso:

    def __init__(self, nombre, departamento, User):
        nombre = nombre.replace(' ','_')
        self.nombre = nombre
        self.departamento = departamento
        self.autor = User
        self.lecciones = []
        self.c_id = db_cursos.find().count()+1
        diccionario = {}
        diccionario['nombre'] = self.nombre
        diccionario['departamento'] = self.departamento
        diccionario['autor'] = self.autor
        diccionario['lecciones'] = self.lecciones
        diccionario['id_curso'] = self.c_id
        db_cursos.insert(diccionario)
     
    @staticmethod
    def actualizar(nombre,departamento,lecciones):
        datos = db_cursos.find({'nombre':nombre})
        lista = []
        for i in datos:
            lista.append(i['nombre'])
            lista.append(i['departamento'])
            lista.append(i['autor'])
            lista.append(i['lecciones'])
            lista.append(i['id_curso'])
        diccionario = {}
        diccionario['nombre'] = nombre
        diccionario['departamento'] = lista[1]
        diccionario['autor'] = lista[2]
        diccionario['lecciones'] = lecciones
        diccionario['id_curso'] = lista[4]
        db_cursos.update({'nombre':nombre},diccionario)

    def getId(self):
        return(self.c_id)

    def __generate_id(self):
        #   metodos privados
        try:
            self.c_id += db_cursos.find().count()
            #   de momento solo cuenta usuarios y se agrega. ese
        except Exception as e:
            #   mejorar exceptions
            print(e)

class Leccion:

    def __init__(self, titulo, contenido,c_id):
        self.titulo = titulo
        self.resumen = contenido
        datos = db_cursos.find({'id_curso':c_id})
        lista = []
        for i in datos:
            lista.append(i['nombre'])
            lista.append(i['departamento'])
            lista.append(i['autor'])
            lista.append(i['lecciones'])
        diccionario = {}
        diccionario['nombre'] = lista[0]
        diccionario['departamento'] = lista[1]
        diccionario['autor'] = lista[2]
        lista[3].append([titulo,contenido])
        diccionario['lecciones'] = lista[3]
        diccionario['id_curso'] = c_id
        db_cursos.update({'id_curso':c_id},diccionario)
        
        