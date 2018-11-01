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

    def check_email(self, email):
        try:
            db_users.find({'email': email})
        except Exception as e:
            raise e

    def __generate_id(self):
        #   metodos privados
        try:
            self.id = db_users.find().count() +1
            #   de momento solo cuenta usuarios y se agrega. ese
        except Exception as e:
            #   mejorar exceptions
            print(e)
  
    def _login(self):
        if self.state != 'logged in':
            self.state = 'logged in'
        else:
            pass

    def _logout(self):
        if self.state != 'logged out':
            self.state = 'logged out'
            print('Logged out')
        else:
            pass

    def present(self):
        print(self.nombre, self.apellidos)
        print(self.id)
        print(self.email)
        print(self.state)

    #   setters / getters
    def getUsername(self):
        return self.username

    def getNombres(self):
        return self.nombres

    def getApellidos(self):
        return self.apellidos

    def getEmail(self):
        return self.email

    def getId(self):
        return self.id

    def setUsername(self, username):
        self.username = username

    def setNombres(self, nombres):
        self.nombres = nombres

    def setApellidos(self, apellidos):
        self.apellidos = apellidos

    def setClave(self, Clave):
        self.clave = Clave


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
       	print(diccionario)
       	db_users.insert(diccionario)

    def modificar_curso(self, curso=None):
        #   en lugar de usar overloading utilizamos parametros con valores default
        try:
            if curso.edit():
                #   True para editado
                #   luego guardar actualizaciones a db
                #   db_cursos.find_one_and_update(curso)
                pass

            else:
                #   curso no editado
                pass

        except Exception as e:
            print(e)

    def modificar_leccion(self, curso=None, leccion=None):
        #   recibir objeto Curso para modificarle una leccion por nombre.
        try:
            if curso.modificar_leccion(leccion):
                #   True para editado
                #   luego guardar actualizaciones a db
                #   db_cursos.find_one_and_update(curso)
                pass

            else:
                #   leccion no editada
                pass

        except Exception as e:
            print(e)


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
        self.nombre = nombre
        self.departamento = departamento
        self.autor = Maestro.getNombres()
        self.lecciones = []
        self.c_id = 1

    def crear_en_db(self,):
        try:
            self.__generate_id()
            cursor = db_cursos.find()
        except Exception as e:
            raise e

    def __generate_id(self):
        #   metodos privados
        try:
            self.c_id += db_cursos.find().count()
            #   de momento solo cuenta usuarios y se agrega. ese
        except Exception as e:
            #   mejorar exceptions
            print(e)

    def nueva_leccion(self, titulo, resumen, enlaces):
        Lec = Leccion(titulo, resumen, enlaces, self.nombre, self.departamento)
        self.lecciones.append(Lec)
        self.update_db()

    def update_db(self):
        try:
            pass
            # db_cursos.insert('_id': self.c_id)
        except Exception as e:
            raise e


class Leccion:

    def __init__(self, titulo, resumen, enlaces, curso=None, departamento=None):
        self.titulo = titulo
        self.resumen = resumen
        self.contenido = ''
        self.ejemplos = []
        self.curso = curso
        self.orden = int
        #   posicion en listado de lecciones del curso
        #   podria ser un diccionario si es necesario.
        #   {int: leccion}

    def editar_cont(self, nuevo):
        if nuevo != self.contenido:
            self.contenido = nuevo
            #   actualizar db

        else:
            pass

    def editar_titulo(self, nuevo):
        pass


class DbQueries:

    def __init__(self, db):
        self.db = db
        self.db_users = db.users
        self.db_cursos = db.cursos

    def get_users(self, kw=None, filter=None):
        try:
            if filter is not None:
                #   devolveria todo
                cursor = self.db_users.find()

            else:
                if filter == 'nombre':
                    cursor = self.db_users.find({'nombre': kw})

                elif filter == 'id':
                    cursor = self.db_users.find({'_id': kw})

                elif filter == 'email':
                    cursor = self.db_users.find({'email': kw})

            return cursor

        except Exception as e:
            print(e)

    def get_cursos(self, kw=None, filter=None):
        try:
            if filter is not None:
                #   devolveria todo
                cursor = self.db_cursos.find()

            else:
                if filter == 'nombre':
                    cursor = self.db_cursos.find({'nombre': kw})

                elif filter == 'id':
                    cursor = self.db_cursos.find({'_id': kw})

                elif filter == 'maestro':
                    cursor = self.db_cursos.find({'maestro': kw})

            return cursor
        except Exception as e:
            print(e)

    def delete_user(self, user):
        try:
            self.users_db.delete_one({'_id': user.getId(), 'nombre': user.getNombres()})
        except Exception as e:
            raise e

    def delete_curso(self, curso):
        try:
            self.db_cursos.delete_one({'_id': curso.getId(), 'nombre': curso.getNombres()})
        except Exception as e:
            raise e

    def _help(self):
        print('''
            \nComandos:\n\n
            get_users // devuelve usuarios
            get_cursos // devuelve cursos
                Ambos gets tienen filteros de nombre/_id/
            maestro o email para curso o email respectivamente
            delete_user(User) // toma un objeto User y con sus atributos lo elimina de db
            delete_cursos(Curso) // toma un objeto Curso y con sus atributos lo elimina de db
            ''')