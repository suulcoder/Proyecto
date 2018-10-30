import pymongo

conexion = pymongo.MongoClient()
db = conexion.Learn4
coleccion = db.Usuarios
from models import Usuario
user = Usuario('luis','luisito','me','fsjlk@uvg.edu.gt','jfdskljñls')
diccionario = {}
diccionario['user'] = user
coleccion.insert(diccionario)