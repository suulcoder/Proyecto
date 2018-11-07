"""
Proyecto POO, Learn4

Saul CONTRERAS
Roberto Figueroa
Isabel Ortiz
Gerardo Pineda
Randy Venegas

Este documento tiene como objetivo realizar un prueba para conectar el html con
nuestro flask, con el objetivo de luego conectarlo con la base de Datos. 


"""
from flask import *
from flask_wtf import CsrfProtect
import forms
import json
from config import DevelopmentConfig
from models import *
import pymongo

conexion = pymongo.MongoClient()#Realizamos conexiones con Base de Datos
db = conexion.Learn4
coleccion = db.Usuarios
database = DbQueries(db)
app = Flask(__name__)#Iniciamos Flask
app.config.from_object(DevelopmentConfig)

@app.route('/', methods=['GET','POST'])#Decorador para rutas con estos metodos para los formularios
def index():#Index de URLS
	formulario = forms.SignInForm(request.form)
	formlogin = forms.LoginForm(request.form)
	comentario = forms.Contacto(request.form)
	userdb = {}
	if request.method == 'POST' and comentario.submit.data and comentario.validate():
		diccionario = {}
		diccionario['email'] = comentario.email.data
		diccionario['nombre'] = comentario.nombre.data
		diccionario['comentario'] = comentario.mensaje.data
		db.Comentarios.insert(diccionario)
	if request.method == 'POST' and formlogin.submit1.data and formlogin.validate():
		userdb = coleccion.find({'email':formlogin.email.data})#Me serviria que fuera un Cursor
		lista = []
		acceso = False
		try:
			for ir in userdb:
				lista.append(ir['email'])
				lista.append(ir['clave'])
				if lista[1] == formlogin.clave.data:
					acceso = True
		except:
			flash('La contraseña no coincide con el Email')		
		try:
			lista[0]
		except:
			flash('Este email no ha sido registrado')	
		if acceso == True:
			i = lista[0]
			return redirect('user/'+i)
	if request.method == 'POST' and formulario.submit2.data and formulario.validate():
		userdb = coleccion.find({'email':formulario.email.data})#Que cuente la cantidad que cumpla con el parametro
		lista = []
		acceso = False
		try:
			for ir in userdb:
				lista.append(ir['email'])
				flash('Este email ya esta registrado')
		except:
			acceso = True
		if len(lista) == 0:
			acceso = True
		if acceso == True:
			if formulario.tipo.data == 'A':
				user = Alumno(formulario.username.data,formulario.nombres.data,formulario.apellidos.data,formulario.email.data,formulario.clave.data,formulario.tipo.data)
			elif formulario.tipo.data == 'M':
				user = Maestro(formulario.username.data,formulario.nombres.data,formulario.apellidos.data,formulario.email.data,formulario.clave.data,formulario.tipo.data)
			flash('Gracias por Registrarte')
			i = formulario.email.data
			return redirect('user/'+i)
	return render_template('Home.html', form=formulario, formLogin=formlogin, comentario=comentario)#Llamamos nuestro diseño


@app.route('/user/<usuario>', methods=['GET','POST'])
def user(usuario):#Index de URL
	datos = coleccion.find({'email':usuario})
	lista = []
	for i in datos:
		lista.append(i['username'])
		lista.append(i['nombres'])
		lista.append(i['apellidos'])
		lista.append(i['email'])
		lista.append(i['tipo'])
		lista.append(i['CursosInscritos'])
	if lista[4]=='M':
		return redirect('maestro/'+usuario)
	if request.method == 'POST':
		if request.form['submit_button'] == '+':
			return redirect('buscar/'+buscar.palabra.data+'/'+usuario)
		else:
			pass
	elif request.method == 'GET':
		return render_template('user.html', username=lista[0], nombre=lista[1], apellidos=lista[2], email=lista[3], tipo=lista[4], CursosInscritos=lista[5])	

@app.route('/maestro/<usuario>', methods=['GET','POST'])
def maestro(usuario):#Index de URL
	crear = forms.CrearCurso(request.form)
	datos = coleccion.find({'email':usuario})
	lista = []
	for i in datos:
		lista.append(i['username'])
		lista.append(i['nombres'])
		lista.append(i['apellidos'])
		lista.append(i['email'])
		lista.append(i['tipo'])
		lista.append(i['CursosInscritos'])
		lista.append(i['CursosAdministrados'])
	listcursos = []
	for i in lista[6]:
		cursodb = db.Cursos.find({'id_curso':i})
		for j in cursodb:
			listcursos.append(j['nombre'])
	if request.method == 'POST':
		if request.form['submit_button'] == '+':
			return redirect('buscar/'+usuario)
		elif request.form['submit_button'] == 'Crear':
			return redirect('nuevocurso/'+crear.palabra.data+'/'+usuario)
		for t in listcursos:
			if request.form['submit_button'] == t:
				return redirect('curso/'+t+'/'+usuario)
	elif request.method == 'GET':
		return render_template('maestro.html', username=lista[0], nombre=lista[1], apellidos=lista[2], email=lista[3], tipo=lista[4], CursosInscritos=lista[5], CursosAdministrados=listcursos, crear=crear)
	return render_template('maestro.html', username=lista[0], nombre=lista[1], apellidos=lista[2], email=lista[3], tipo=lista[4], CursosInscritos=lista[5], CursosAdministrados=listcursos, crear=crear)
		
@app.route('/buscar/<usuario>', methods=['GET', 'POST'])
def buscar(usuario):
	cursos = db.Cursos.find()
	lista_cursos = []
	for j in cursos:
		lista_cursos.append(j['nombre'])
	for t in lista_cursos:
		if request.method == 'POST':
			if request.form['submit_button'] == t:
				return redirect('curso/'+t+'/'+usuario)
			elif request.form == 'GET':
				return render_template('menu-cursos.html', lista=lista_cursos)
	return render_template('menu-cursos.html', lista=lista_cursos)

@app.route('/curso/<nombre>/editleccion/<numero>/<usuario>')
def editleccion(nombre,numero,usuario):#
	return('ok')

@app.route('/curso/<nombre>/<usuario>', methods=['GET', 'POST'])
def curso(nombre,usuario):
	datos = db.Cursos.find({'nombre':nombre})
	lista = []
	for i in datos:
		lista.append(i['nombre'])
		lista.append(i['lecciones'])
		lista.append(i['autor'])	
	if lista[2] == usuario:
		if request.method == 'POST':
			if request.form['submit_button'] == 'editar curso':
				return redirect('editcurso/'+nombre+'/'+usuario)
		elif request.method == 'GET':
			return render_template('curso.html', nombre=lista[0], lecciones=lista[1], autor=lista[2])
	return render_template('curso.html', nombre=lista[0], lecciones=lista[1], autor=lista[2])

@app.route('/nuevocurso/<nombre>/<usuario>', methods=['GET','POST'])
def nuevocurso(nombre,usuario):
	name = nombre.replace(' ','_')
	datos = coleccion.find({'email':usuario})
	lista = []
	for i in datos:
		lista.append(i['username'])
		lista.append(i['tipo'])
	if lista[1]=='M':
		cursos = db.Cursos.find({'nombre':name})
		lista_cursos = []
		for j in cursos:
			lista_cursos.append(j['autor'])
		if len(lista_cursos)!=0:
			if lista_cursos[0]==usuario:
				return redirect('editcurso/'+name+'/'+usuario)
			else:
				return redirect('curso/'+name+'/'+usuario)
		else:
			formulario = forms.infoCurso(request.form)
			if request.method == 'POST':
				if request.form['submit_button'] == 'Crear':
					Maestro.CrearCurso(name, formulario.departamento.data, usuario)
					return redirect('curso/'+name+'/'+usuario)
				elif request.form['submit_button'] == '+':
					return redirect('curso/'+name+'/editleccion/'+str(len(lista_cursos[1])+1)+'/'+usuario)
			elif request.method == 'GET':
				return render_template('cursoMaestro.html', nombre=nombre, formulario=formulario, lecciones=[])
			return render_template('cursoMaestro.html', nombre=nombre, formulario=formulario, lecciones=lista_cursos[1])
	else:
		return redirect('curso/'+usuario)

@app.route('/editcurso/<nombre>/<usuario>')
def editcurso(nombre,usuario):#
	datos = db.Cursos.find({'nombre':nombre})
	lista = []
	for i in datos:
		lista.append(i['nombre'])
		lista.append(i['lecciones'])
		lista.append(i['autor'])
	if lista[2] == usuario:
		formulario = forms.infoCurso(request.form)
		if request.method == 'POST':
			if request.form['submit_button'] == 'Crear':
				Curso.actualizar(nombre, formulario.departamento.data, lecciones)
				return redirect('curso/'+nombre+'/'+usuario)
			elif request.form['submit_button'] == '+':
				return redirect('curso/'+nombre+'/editleccion/'+str(len(lista_cursos[1])+1)+'/'+usuario)
		elif request.method == 'GET':
			return render_template('cursoMaestro.html', nombre=nombre, formulario=formulario, lecciones=[])
		return render_template('cursoMaestro.html', nombre=nombre, formulario=formulario, lecciones=lista[1])
	else:
		return redirect('curso/'+nombre+'/'+usuario)


@app.errorhandler(404)#Programamos defensivamente
def page_not_found(e):
	return render_template('error.html')

if __name__ == '__main__':
	app.run(port=5000)#Corre el sistema y nos permite que al actualizar esta se actualice automaticamente