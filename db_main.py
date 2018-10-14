'''

Proyecto Learn4 - Programacion orientada a objetos

Integrantes:
-



db_main.py
PyMongo - 3.7.2
docs - https://api.mongodb.com/python/current/

'''
import json
import os
import logging
from db_util import *
from time import sleep
from principales import *
from pymongo import MongoClient

#   Logging Setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s:')
file_handler = logging.FileHandler('main_info.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def add_user(user):
    #   recibe un usuario, clase User, agrega a coleccion users.
    try:
        users.insert(user.all_details())

    except Exception as e:
        logger.exception(e)

#   también podria ser una clase que manipule todo, quizá sea más fácil.
class DbQueries:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client["users"]
        self.alumnos = self.db.alumnos
        self.maestros = self.db.maestros

    def get_maestros(self, *args):
        try:
            maestros = self.maestros.find()
            #   maestros es un cursor de la coleccion "maestros"
            #   lo podemos operar con un for
        except Exception as e:
            print(e)

    def get_maestro(self, nombre=None, _id=None):
        try:
            maestro = self.maestros.find_one({"_id":{ _id: nombre}})
            return maestro

        except Exception as e:
            logger.exception(e)

    # def get_user_courses(self, User):
    #     try:
    #         lista_cursos = self.db.find()
    #     except Exception as e:
    #         raise e


# db.insert_many()
# #	insertar multiples objetos, lista de dicts por ejemplo

# db.insert_one(userdict)
# #	un unico documento
if __name__ == "__main__":
    client = MongoClient()
    # sin info en el constructor de mongoclient asume red local 127.0.0.1

    db = client['database']
    users = db.users
    cursos = db.cursos
    # colecciones dentro de base de datos