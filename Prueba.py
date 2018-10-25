"""
Proyecto POO, Learn4

Saul CONTRERAS
Roberto Figueroa
Isabel Ortiz
Gerardo Mendez
Randy Venegas

Este documento tiene como objetivo realizar un prueba para conectar el html con
nuestro flask, con el objetivo de luego conectarlo con la base de Datos. 


"""

import pymongo

conexion = pymongo.MongoClient()
db = conexion.Learn4
coleccion = db.Usuarios

from flask import *
from flask_wtf import CsrfProtect
import forms
import json
from config import DevelopmentConfig
from models import *

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

@app.route('/', methods=['GET','POST'])#Decorador para rutas con estos metodos para los formularios
def index():#Index de URLS
	formulario = forms.SignInForm(request.form)
	formlogin = forms.LoginForm(request.form)
	if request.method == 'POST' and formlogin.submit1.data and formlogin.validate():
		return redirect('user')
	if request.method == 'POST' and formulario.submit2.data and formulario.validate():
		if formulario.tipo.data == 'A':
			user = Alumno(formulario.username.data,formulario.nombres.data,formulario.apellidos.data,formulario.email.data,formulario.clave.data)
		elif formulario.tipo.data == 'M':
			user = Maestro(formulario.username.data,formulario.nombres.data,formulario.apellidos.data,formulario.email.data,formulario.clave.data)
		flash('Gracias por Registrarte')
		return redirect('user')
	return render_template('Home.html', form=formulario, formLogin=formlogin)#Llamamos nuestro diseño

@app.route('/user')
def user():#Index de URL
	return render_template('loggedUser.html')	

@app.route('/cookie')
def cookie():
	response = make_response( render_template('cookie.html'))
	response.set.cookie('custome_cookie', '')

@app.route('/ajax-login', methods= ['POST'])
def ajax_login():
	print(request.form)
	username = request.form['username']
	response = {'status' : 200, 'username': username, 'id': 1}
	return json.dumps(response)

@app.errorhandler(404)#Programamos defensivamente
def page_not_found():
	return render_template('404.html')


if __name__ == '__main__':
	app.run(port=5000)#Corre el sistema y nos permite que al actualizar esta se actualice automaticamente
