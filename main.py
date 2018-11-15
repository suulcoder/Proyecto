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
app = Flask(__name__)#Iniciamos Flask
app.config.from_object(DevelopmentConfig)

@app.route('/', methods=['GET','POST'])#Decorador para rutas con estos metodos para los formularios
def index():#Index de URLS
	formulario = forms.SignInForm(request.form)#Instanciamos los tres formularios
	formlogin = forms.LoginForm(request.form)
	comentario = forms.Contacto(request.form)
	userdb = {}
	if request.method == 'POST' and comentario.submit.data and comentario.validate():#Evaluamos si el formulario de comentario tiene datos
		diccionario = {}
		diccionario['email'] = comentario.email.data
		diccionario['nombre'] = comentario.nombre.data
		diccionario['comentario'] = comentario.mensaje.data
		db.Comentarios.insert(diccionario)#Insertamos los comentarios
	if request.method == 'POST' and formlogin.submit1.data and formlogin.validate():
		userdb = coleccion.find({'email':formlogin.email.data})#Buscamos los datos del usuario
		lista = []
		acceso = False
		try:
			for ir in userdb:
				lista.append(ir['email'])
				lista.append(ir['clave'])
				if lista[1] == formlogin.clave.data:
					acceso = True
		except:#Programacion defensiva
			flash('La contraseña no coincide con el Email')		
		try:#buscamos el primer elemento. 
			lista[0]
		except:#Programamos defensivamente
			flash('Este email no ha sido registrado')	
		if acceso == True:
			i = lista[0]
			return redirect('user/'+i)
	if request.method == 'POST' and formulario.submit2.data and formulario.validate():#Evaluamos si el formulario esta enviando datos
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
			if formulario.tipo.data == 'A':#Si es de tipo alumno
				#Instanciamos a una clase tipo Usuario Alumno
				user = Alumno(formulario.username.data,formulario.nombres.data,formulario.apellidos.data,formulario.email.data,formulario.clave.data,formulario.tipo.data)
			elif formulario.tipo.data == 'M':#Si es de tipo maestro
				#Instanciamos a una clase tipo Usuario Maestro
				user = Maestro(formulario.username.data,formulario.nombres.data,formulario.apellidos.data,formulario.email.data,formulario.clave.data,formulario.tipo.data)
			flash('Gracias por Registrarte')#Agradecemos por el registro
			i = formulario.email.data
			return redirect('user/'+i)
	return render_template('Home.html', form=formulario, formLogin=formlogin, comentario=comentario)#Llamamos nuestro diseño


@app.route('/user/<usuario>', methods=['GET','POST'])
def user(usuario):#Index de URL
	formulario = forms.SignInForm(request.form)#Instanciamos el formulario
	datos = coleccion.find({'email':usuario})
	lista = []#Creamos una lista para llenar conlos datos del alumno
	for i in datos:#Llenamos la lista con los datos del alumno
		lista.append(i['username'])
		lista.append(i['nombres'])
		lista.append(i['apellidos'])
		lista.append(i['email'])
		lista.append(i['tipo'])
		lista.append(i['CursosInscritos'])
	listainscritos = []#Creamos una lista con los cursos en los que esta inscrito. 
	for i in lista[5]:
		cursodb = db.Cursos.find({'id_curso':i})
		for j in cursodb:
			listainscritos.append(j['nombre'])#Agregamos los elementos a la lista
	if lista[4]=='M':
		return redirect('maestro/'+usuario)
	if request.method == 'POST':#Si se envian datos
		if request.form['submit_button'] == '+':#Si se pide que se agregue uno mas
			return redirect('buscar/'+usuario)
		elif request.form['submit_button'] == 'Guardar':#Si se pide que se agregue el boton Guardar
			User.actualizar(formulario.username.data,formulario.nombres.data,formulario.apellidos.data,formulario.clave.data,usuario)
			return redirect('user/'+usuario)
		elif request.form['submit_button'] == "Loggedout":#Si se pide salir
			return redirect('')#Redireccionamos a index
		elif request.form['submit_button'] == "Mis Cursos":#Si se pide ver Mis Cursos
			return redirect('user/'+usuario)
		elif request.form['submit_button'] == "Perfil":#Si se pide ver perfil
			return redirect('user/'+usuario)
		for t in listainscritos:
			if request.form['submit_button'] == t:#Para ver Uusuarios
				return redirect('curso/'+t+'/'+usuario)
	elif request.method == 'GET':
		return render_template('user.html', username=lista[0], nombre=lista[1], apellidos=lista[2], email=lista[3], tipo=lista[4], CursosInscritos=listainscritos, formulario=formulario)	


@app.route('/maestro/<usuario>', methods=['GET','POST'])
def maestro(usuario):#Index de URL
	formulario = forms.SignInForm(request.form)#Instanciamos los formularios 
	crear = forms.CrearCurso(request.form)
	datos = coleccion.find({'email':usuario})
	lista = []
	for i in datos:#Recogemos los dato del usuario
		lista.append(i['username'])
		lista.append(i['nombres'])
		lista.append(i['apellidos'])
		lista.append(i['email'])
		lista.append(i['tipo'])
		lista.append(i['CursosInscritos'])
		lista.append(i['CursosAdministrados'])
	listcursos = []#Recogemos los datos de los cursos
	for i in lista[6]:
		cursodb = db.Cursos.find({'id_curso':i})
		for j in cursodb:
			listcursos.append(j['nombre'])
	listainscritos = []
	for i in lista[5]:
		cursodb = db.Cursos.find({'id_curso':i})
		for j in cursodb:
			listainscritos.append(j['nombre'])
	if request.method == 'POST':
		if request.form['submit_button'] == '+':#Interactuamos con el usuario
			return redirect('buscar/'+usuario)
		elif request.form['submit_button'] == 'Crear':
			return redirect('nuevocurso/'+crear.palabra.data+'/'+usuario)
		elif request.form['submit_button'] == 'Guardar':
			User.actualizar(formulario.username.data,formulario.nombres.data,formulario.apellidos.data,formulario.clave.data,usuario)
			return redirect('maestro/'+usuario)
		elif request.form['submit_button'] == "Loggedout":
			return redirect('')
		elif request.form['submit_button'] == "Mis Cursos":
			return redirect('user/'+usuario)
		elif request.form['submit_button'] == "Perfil":
			return redirect('user/'+usuario)
		for t in listcursos:
			if request.form['submit_button'] == t:
				return redirect('curso/'+t+'/'+usuario)
	elif request.method == 'GET':
		return render_template('maestro.html', username=lista[0], nombre=lista[1], apellidos=lista[2], email=lista[3], tipo=lista[4], CursosInscritos=listainscritos, CursosAdministrados=listcursos, crear=crear, formulario=formulario)
	return render_template('maestro.html', username=lista[0], nombre=lista[1], apellidos=lista[2], email=lista[3], tipo=lista[4], CursosInscritos=listainscritos, CursosAdministrados=listcursos, crear=crear, formulario=formulario)
		
@app.route('/buscar/<usuario>', methods=['GET', 'POST'])
def buscar(usuario):#Esta ruta nos permitira que el usuario vea todos los cursos
	cursos = db.Cursos.find()
	lista_cursos = []
	for j in cursos:
		lista_cursos.append(j['nombre'])
	for t in lista_cursos:
		if request.method == 'POST':
			if request.form['submit_button'] == t:
				return redirect('curso/'+t+'/'+usuario)#Redirigimos a Curso
			elif request.form['submit_button'] == "Loggedout":
				return redirect('')
			elif request.form['submit_button'] == "Mis Cursos":
				return redirect('user/'+usuario)
			elif request.form['submit_button'] == "Perfil":
				return redirect('user/'+usuario)
			elif request.form == 'GET':
				return render_template('menu-cursos.html', lista=lista_cursos)
	return render_template('menu-cursos.html', lista=lista_cursos)

@app.route('/curso/<nombre>/<usuario>', methods=['GET', 'POST'])
def curso(nombre,usuario):#Ruta de Curso
	datos = db.Cursos.find({'nombre':nombre})#Tomamos los datos del Curso
	lista = []
	for i in datos:
		lista.append(i['nombre'])
		lista.append(i['lecciones'])
		lista.append(i['autor'])
		lista.append(i['id_curso'])
	curso = db.Usuarios.find({'email':usuario})
	for i in curso:
		lista.append(i['CursosInscritos'])
	inscrito = False
	for i in lista[4]:#eEvaluamos si el usuario ya esta inscrito
		if i == lista[3]:
			inscrito = True
	if inscrito == True:#Si el usuario esta inscrito redirigimos
		return redirect('course/'+nombre+'/'+usuario)
	else:#
		if lista[2] == usuario:#Si el usuario es el maestro
			if request.method == 'POST':
				if request.form['submit_button'] == 'editar curso':#Peimos que edite el curo
					return redirect('editcurso/'+nombre+'/'+usuario)
				elif request.form['submit_button'] == "Loggedout":
					return redirect('')
				elif request.form['submit_button'] == "Mis Cursos":
					return redirect('user/'+usuario)
				elif request.form['submit_button'] == "Perfil":
					return redirect('user/'+usuario)
			elif request.method == 'GET':
				return render_template('curso.html', nombre=lista[0], lecciones=lista[1], autor=lista[2])
		else:
			if request.method == 'POST':#Sino redirigimos
				if request.form['submit_button'] == 'Unirse':
					User.Unirse(usuario,nombre)
					return redirect('course/'+nombre+'/'+usuario)
			elif request.method == 'GET':#Programacion defensiva
				return render_template('mycurso.html', nombre=lista[0], lecciones=lista[1], autor=lista[2])
	return render_template('mycurso.html', nombre=lista[0], lecciones=lista[1], autor=lista[2])
							
@app.route('/course/<nombre>/<usuario>', methods=['GET', 'POST'])
def course(nombre,usuario):#Esta ruta ayuda al curso maestro
	datos = db.Cursos.find({'nombre':nombre})
	lista = []#Tomamos datos
	for i in datos:
		lista.append(i['nombre'])
		lista.append(i['lecciones'])
		lista.append(i['autor'])
		lista.append(i['id_curso'])
	if request.method == 'POST':#Interactuamos con el usuario
		if request.form['submit_button'] == "Loggedout":
			return redirect('')
		elif request.form['submit_button'] == "Mis Cursos":
			return redirect('user/'+usuario)
		elif request.form['submit_button'] == "Perfil":
			return redirect('user/'+usuario)
	elif request.method == 'GET':
		return render_template('Course.html', nombre=lista[0], lecciones=lista[1], autor=lista[2])
	else:
		return render_template('Course.html', nombre=lista[0], lecciones=lista[1], autor=lista[2])



@app.route('/nuevocurso/<nombre>/<usuario>', methods=['GET','POST'])
def nuevocurso(nombre,usuario):#Esta ruta permite que se cree un nuevo curso
	formleccion = forms.formleccion(request.form)#Instanciamo formulario para pedir informaioon
	name = nombre.replace(' ','_')
	datos = coleccion.find({'email':usuario})
	lista = []
	for i in datos:
		lista.append(i['username'])
		lista.append(i['tipo'])
	if lista[1]=='M':#Evaluamos si el usuario es de tipo maestro, ya que solo ellos tienen el derecho de crear cursos
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
			formulario = forms.infoCurso(request.form)#Formulario para leccion
			if request.method == 'POST':
				if request.form['submit_button'] == 'Hecho':
					Maestro.CrearCurso(name, formulario.departamento.data, usuario)#Llamamos metodo estatico que crea curso
					return redirect('curso/'+name+'/'+usuario)
				elif request.form['submit_button'] == 'Guardar':
					ids = Maestro.CrearCurso(name, formulario.departamento.data, usuario)#Llamamos metodo estatico que crerara curso
					Leccion(formleccion.titulo.data,formleccion.contenido.data,ids)#Agregara leccion
					return redirect('editcurso/'+name+'/'+usuario)
				elif request.form['submit_button'] == "Loggedout":
					return redirect('')
				elif request.form['submit_button'] == "Mis Cursos":
					return redirect('user/'+usuario)
				elif request.form['submit_button'] == "Perfil":
					return redirect('user/'+usuario)
			elif request.method == 'GET':
				return render_template('cursoMaestro.html', nombre=nombre, formulario=formulario, lecciones=[], formleccion=formleccion)
			return render_template('cursoMaestro.html', nombre=nombre, formulario=formulario, lecciones=lista_cursos[1], formleccion=formleccion)
	else:
		return redirect('curso/'+usuario)

@app.route('/editcurso/<nombre>/<usuario>', methods=['GET','POST'])
def editcurso(nombre,usuario):#Ruta para editar curso
	formleccion = forms.formleccion(request.form)
	datos = db.Cursos.find({'nombre':nombre})#Tomamdos datos
	lista = []
	for i in datos:
		lista.append(i['nombre'])
		lista.append(i['lecciones'])
		lista.append(i['autor'])
		lista.append(i['id_curso'])
	lecciones = lista[1]
	if lista[2] == usuario:
		formulario = forms.infoCurso(request.form)#Este formulario se llenara con los datos dle usuario
		if request.method == 'POST':
			if request.form['submit_button'] == 'Hecho':
				Curso.actualizar(nombre, formulario.departamento.data,lecciones)#Actualizamos con el metodo
				return redirect('curso/'+nombre+'/'+usuario)
			elif request.form['submit_button'] == 'Guardar':
				ids = lista[3]
				Leccion(formleccion.titulo.data,formleccion.contenido.data,ids)#ACTUALIZAMOS CON NUEVA LECCION
				return redirect('editcurso/'+nombre+'/'+usuario)
			elif request.form['submit_button'] == "Loggedout":
				return redirect('')
			elif request.form['submit_button'] == "Mis Cursos":
				return redirect('user/'+usuario)
			elif request.form['submit_button'] == "Perfil":
				return redirect('user/'+usuario)
		elif request.method == 'GET':
			return render_template('cursoMaestro.html', nombre=nombre, formulario=formulario, lecciones=lista[1],formleccion=formleccion)
		return render_template('cursoMaestro.html', nombre=nombre, formulario=formulario, lecciones=lista[1],formleccion=formleccion)
	else:
		return redirect('curso/'+nombre+'/'+usuario)


@app.errorhandler(404)#Programamos defensivamente
def page_not_found(e):
	return render_template('error.html')

if __name__ == '__main__':
	#app.run(host="192.168.1.11" port=5000)   #Corre el sistema y nos permite que al actualizar esta se actualice automaticamente
	app.run(port=5000)