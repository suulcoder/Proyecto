from flask import Flask
from flask_wtf import Form, FlaskForm
from wtforms import Form, SubmitField, BooleanField, StringField, PasswordField, validators, SelectField, RadioField
from wtforms.fields.html5 import EmailField

'''
Formularios que nos permitira que el usuaio ingrese informacion 
a la plataforma.

'''


class LoginForm(Form):
    email = EmailField('E-mail', [validators.DataRequired(message='Escriba un E-mail Valido')])
    clave = PasswordField('Escriba clave de acceso', [validators.DataRequired()])
    submit1 = SubmitField('Ingresar')


class SignInForm(Form):
    username = StringField('Nombre de Usuario', [validators.DataRequired(message='Este campo es requerdio')])
    nombres = StringField('Nombres', [validators.DataRequired(message='Campo Requerido')])
    apellidos = StringField('Apellidos', [validators.DataRequired(message='Campo Requerido')])
    email = EmailField('E-mail', [validators.DataRequired(message='Escriba un E-mail Valido')])
    clave = PasswordField('Escriba una clave de Acceso', [validators.DataRequired(message='Campo Requerido'), validators.EqualTo('confirm', message='Las Claves deben de ser Iguales')])
    confirm = PasswordField('Confirma tu Clave de Acceso')
    accept = BooleanField('Acepto Terminos y Condiciones', [validators.DataRequired(message='Campo Requerido')])
    tipo = RadioField('Tipo de Usuario', choices=[('A', 'Alumno'), ('M', 'Maestro')])
    submit2 = SubmitField('Registrar')


class Contacto(Form):
    email = EmailField('Email', [validators.DataRequired(message='Campo Requerido)')])
    nombre = StringField('Nombres')
    mensaje = StringField('Comentario', [validators.DataRequired(message='Campo Requerido')])

class CrearCurso(Form):
    submit = SubmitField('CREAR CURSO')

class InscribirseaCurso(Form):
    submit = SubmitField('BUSCAR CURSOS')