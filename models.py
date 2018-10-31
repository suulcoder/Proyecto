import pymongo

conexion = pymongo.MongoClient()
db = conexion.Learn4
db_users = db.Usuarios
db_cursos = db.Cursos
categorias = []


class User:

    def __init__(self, username, clave, nombre, apellidos, email, tipo):
        self.username = username
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.tipo = tipo
        self.clave = clave
        self.state = 'logged in'
        self.id = 1

        #   Cursos
        self.CursosInscritos = []
        self.CursosAdministrados = []
        #   antes de instanciar al usuario se verifica si ya esta en db
        #   entonces al instanciar lo agregamos a db
        self.__insert()

    #   metodos para db / mongo

    def check_email(self, email):
        try:
            db_users.find({'email': email})
        except Exception as e:
            raise e

    def __generate_id(self):
        #   metodos privados
        try:
            self.id += db_users.find().count()
            #   de momento solo cuenta usuarios y se agrega. ese
        except Exception as e:
            #   mejorar exceptions
            print(e)

    def __insert(self):
        #   metodos privados
        try:
            if self.id == 1:
                self.__generate_id()
                db_users.insert(dict(_id=self.id, username=self.username, Tipo=self.tipo, nombres=self.nombres, apellidos=self.apellidos, email=self.email,
                                     clave=self.clave, CursosInscritos=self.CursosInscritos, CursosAdministrados=self.CursosAdministrados))

            print("New User:")
            self.present()
            self._login()
        except Exception as e:
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
        #   antes de incertar el usuario a la base de datos se verifica si ya esta.
        # coleccion.insert(diccionario)

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

    def __init__(self, username, nombres, apellidos, email, clave, tipo):
        User.__init__(self, username, nombres, apellidos, email, clave, tipo)
        self.id_curso = int


class Curso:

    def __init__(self, nombre, departamento, User):
        self.nombre = nombre
        self.departamento = departamento
        self.autor = Maestro.getNombres()
        self.lecciones = []
        self.c_id = 1
        self.__insert()

    def __insert(self):
        #   metodos privados
        try:
            if self.id == 1:
                self.__generate_id()
                db_users.insert(dict(_id=self.c_id, nombre=self.nombre, departamento=self.departamento, autor=self.autor, lecciones=self.lecciones))

            print("Nuevo curso:")

        except Exception as e:
            print(e)

    def __generate_id(self):
        #   metodos privados
        try:
            self.c_id += db_cursos.find().count()
            #   de momento solo cuenta resultados
        except Exception as e:
            #   mejorar exceptions
            print(e)

    def nueva_leccion(self, titulo, resumen, enlaces):
        Lec = Leccion(titulo, resumen, enlaces, self.nombre, self.departamento)
        self.lecciones.append(Lec)
        # self.update_db()

    def update_db(self):
        try:
            pass
            # db_cursos.insert('_id': self.c_id)
        except Exception as e:
            raise e

    def get_nombre(self):
        return self.nombre

    def get_departamento(self):
        return self.departamento

    def get_lecciones(self):
        return self.lecciones


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
    #   esta clase toma un objeto de cliente de mongo y se encarga de hacer
    #   todos los cambios de manera mas directa.
    #   Toda la documentacion de como manejar las colecciones/db puede ser encontrada aqui:
    #
    #   https://api.mongodb.com/python/current/api/pymongo/collection.html

    def __init__(self, db):
        self.db = db
        self.db_users = db.users
        self.db_cursos = db.cursos

    def menu(self):
        print('todavia no funciona como consola')
        print('1. get / get_counts ')
        print('2. set / update')
        print('3. Insert')
        print('4. Delete\n')

    def get_users(self, kw=None, filter=None):
        try:
            if filter is None:
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

    def get_users_count(self, kw=None, filter=None):
        try:
            if filter is None:
                #   devolveria todo
                cursor = self.db_users.find().count()

            else:
                if filter == 'nombre':
                    cursor = self.db_users.find({'nombre': kw}).count()

                elif filter == 'id':
                    cursor = self.db_users.find({'_id': kw}).count()

                elif filter == 'email':
                    cursor = self.db_users.find({'email': kw}).count()

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

    def get_cursos_count(self, kw=None, filter=None):
        try:
            if filter is not None:
                #   devolveria todo
                cursor = self.db_cursos.find().count()

            else:
                if filter == 'nombre':
                    cursor = self.db_cursos.find({'nombre': kw}).count()

                elif filter == 'id':
                    cursor = self.db_cursos.find({'_id': kw}).count()

                elif filter == 'maestro':
                    cursor = self.db_cursos.find({'maestro': kw}).count()

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
            self.db_cursos.delete_one({'_id': curso.getId(), 'nombre': curso.get_nombre(), 'departamento': curso.get_departamento()})
        except Exception as e:
            raise e

    def update_user_field(self, _filter, filter_value, field, new_value):
        #   actualizar un solo detalle de un usuario
        try:
            #   ({filter: filter_value}, {'$set': {field: new_value}})
            #   ({campos/filtros para encontrar al usuario} , {'$set': {campo: valor_nuevo}})
            #
            #   ejemplo:
            #   update_user_field('email', 'ejemplo@dominio.com', 'clave', 'nueva_clave')
            #   busca a usuario por email y actualiza su clave
            self.db_users.find_one_and_update({_filter: filter_value}, {'$set': {field: new_value}})
        except Exception as e:
            raise e

    def _help(self):
        print('''
            \nComandos:\n\n
            keyword == termino a buscar, i.e. un nombre o un email. "andrea" / 'andrea@dominio.com'
            filter == seccion a buscar, i.e. 'email' / 'nombre' / '_id'
            get_users(keyword, filter) // devuelve cursor 
            get_users_count // devuelve int
            get_cursos // devuelve cursor
            get_cursos_count // devuelve int

            update_user(field, new_value)
            update_curso(field, new_value)
                
            delete_user(User) // toma un objeto User y con sus atributos lo elimina de db
            delete_cursos(Curso) // toma un objeto Curso y con sus atributos lo elimina de db
            \n
            ''')
        self.menu()
