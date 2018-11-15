from flask import Flask
from flask_wtf import Form, FlaskForm
from wtforms import Form, SubmitField, BooleanField, StringField, PasswordField, validators, SelectField, RadioField
from wtforms.fields.html5 import EmailField

'''
Formularios que nos permitira que el usuaio ingrese informacion 
a la plataforma.

'''
class LoginForm(Form):#Formulario para Login que pregunta email, clave y boton submit
	email = EmailField('E-mail',[validators.DataRequired(message='Escriba un E-mail Valido')])#Valida que sea email
	clave = PasswordField('Escriba clave de acceso',[validators.DataRequired()])
	submit1 = SubmitField('Ingresar')

class SignInForm(Form):#Formulario para SignIn que pregunta los siguientes campos
	username = StringField('Nombre de Usuario', [validators.DataRequired(message='Este campo es requerdio')])#Valida que exista
	nombres =  StringField('Nombres',[validators.DataRequired(message='Campo Requerido')])#Valida que exista
	apellidos = StringField('Apellidos',[validators.DataRequired(message='Campo Requerido')])
	email = EmailField('E-mail',[validators.DataRequired(message='Escriba un E-mail Valido')])#Valida que sea email
	clave = PasswordField('Escriba una clave de Acceso',[validators.DataRequired(message='Campo Requerido'),validators.EqualTo('confirm', message='Las Claves deben de ser Iguales')])
	confirm = PasswordField('Confirma tu Clave de Acceso')
	accept = BooleanField('Acepto Terminos y Condiciones', [validators.DataRequired(message='Campo Requerido')])
	tipo = RadioField('Tipo de Usuario', choices=[('A','Alumno'),('M','Maestro')])
	submit2 = SubmitField('Registrar')
	
class Contacto(Form):#Pregunta Contacto, Formulario que hereda de Form, que pregunta lo siguiente, 
    email = EmailField('Email', [validators.DataRequired(message='Campo Requerido)')])
    nombre = StringField('Nombres')
    mensaje = StringField('Comentario', [validators.DataRequired(message='Campo Requerido')])
    submit = SubmitField('Enviar')

class CrearCurso(Form):#Formulario para llenar los datos del curso
	palabra = StringField('Nombre del Curso')#Nombre del Curso
	submit1 = SubmitField('CREAR CURSO')#Boton submit

"""Existen dos para cursos ya que se usa uno en diferente ruta, o funcion o template"""

class infoCurso(Form):#Formulario que pregunta la info del Curso
	departamento = StringField('Departamento del curso')

class formleccion(Form):#Pregunta la informacion de una leccion
	titulo = StringField('Titulo')
	contenido = StringField('Escriba el contenido de la lección')