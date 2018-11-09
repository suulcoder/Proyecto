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