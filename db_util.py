'''

Proyecto Learn4 - Programacion orientada a objetos


Funciones para usar en db_main
PyMongo - 3.7.2
docs - https://api.mongodb.com/python/current/
'''

import os
import json
import random
from principales import *
from pymongo import MongoClient



#   para generar informacion random y hacer pruebas

example_database = {
    'cursos': {'Calculo': {'lecciones':
                              {'leccion 1': {'nombre': 'Limites parte 1', 'Duracion': 45, 'ejemplos': [1, 2, 3]},
                                'leccion 2': {'nombre': 'Limites parte 2', 'Duracion': 25, 'ejemplos': [4, 5, 6]},
                                        },
                          }
               },


    'usuarios':{
    #     '01': {'id': 1,
    #            'nombre': 'algo',
    #            'tipo': 'maestro',
    #            'cursos': [],
    #            'email': 'email@dominio.com',
    #            'password': '123',
    #            },
    #     '02':{'id': 2,
    #            'nombre': 'alguien',
    #            'tipo': 'alumno',
    #            'cursos': ['calculo'],
    #            'email': 'email@dominio.com',
    #            'password': '1234',
    #
    #     }
    }



}

users = {}

names = [
    'luis', 'andre', 'saul', 'isa', 'monica',
    'andres', 'juan', 'pedro', 'josue', 'renato'
]

tipo = [ 'maestro', 'alumno']

last_names = [
    'gonzalez', 'andrade', 'fernandez', 'monge', 'ortiz',
    'aju', 'paak', 'davis', 'garcia', 'estrada'
]

cursos = [
    'calculo', 'fisica', 'ecuaciones diferenciales', 'programacion', 'estructuras de datos',
    'estaditica', 'algebra lineal', 'cocina', 'carpinteria', 'web dev'
]

dominios = [
    'gmail.com', 'yahoo.com', 'uvg.edu.gt', 'outlook.com', 'hotmail.com',
    'colegio.com', 'url.edu.gt', 'gov.gt', 'amazon.com', 'valvesoftware.com'
]


def generate_person():
    #   generate random user info combinations
    #   diccionario o objeto User con {id, nombre, apellido, password, cursos, email}
    a, b, c, d, e = random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 1)
    suma = a + b * (c + 1) * random.randint(373, 1268)
    email = last_names[b][:3] + str(suma) + "@" + dominios[d]

    return User(_id=suma, nombre=names[a], tipo=tipo[e], apellido=last_names[b], password=1234, cursos=list(cursos[c]), email=email)
    # return dict(_id=suma, nombre=names[a], tipo=tipo[e], apellido=last_names[b], password=1234, cursos=list(cursos[c]), email=email)


def to_db(person):
    #   check if in dict add if ID is unused.
    if person['id'] not in users['id']:
        users['id'][person["id"]] = person





