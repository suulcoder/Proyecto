'''
Proyecto Learn4 - Programacion orientada a objetos
clases principales
'''
class User:
    #   clase usuario que deberia ser como se maneja el usuario en django
    def __init__(self, nombre, apellido, email, cursos, tipo, password=1234, _id=None):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.tipo = tipo
        self.cursos = []
        self.password = password
        self._id = 0

    def get_cursos(self, *args):
        return self.cursos

    def get_id(self, *args):
        return self._id

    def all_details(self, *args):
        return dict(_id=self._id, nombre=self.nombre, apellido=self.apellido, tipo=self.tipo,
                    cursos=self.cursos, email=self.email)


class Leccion:

    def __init__(self, nombre):
        self.orden = 0
        self.nombre = nombre
        self.contenido_texto = ''
        self.links = []


class Curso:

    def __init__(self, nombre):
        self.nombre = nombre
        self.lecciones = []

    def get_lecciones(self, *args):
        return self.lecciones

    def add_leccion(self, leccion):
        self.lecciones.append(leccion)