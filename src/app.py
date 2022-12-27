#########################################################################################
####################################    Librerias   #####################################
#########################################################################################
from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import config
from flask_mail import Mail, Message
from models.token import generate_confirmation_token, confirm_token

# Clases
# Models:
from models.ModelUser import ModelUser
from models.ModelLoker import ModelLocker
from models.ModelLocation import ModelLocation
from models.ModelRepartidor import ModelRepartidor
from models.ModelEnvio import ModelEnvio
from models.ModelTarjeta import ModelTarjeta

# Entities:
from models.entities.User import User
from models.entities.Locker import Locker
from models.entities.Location import Location
from models.entities.Envio import Envio
from models.entities.Tarjeta import Tarjeta

app = Flask(__name__)
csrf = CSRFProtect()
db = MySQL(app)
#########################################################################################
############################ Configuracion de servicio e-mail ###########################
#########################################################################################
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sendiitadsscrumios@gmail.com'
app.config['MAIL_USERNAME'] = 'sendiitadsscrumios@gmail.com'
app.config['MAIL_PASSWORD'] = "xeqesdzdiuknempi"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
login_manager_app = LoginManager(app)

#########################################################################################
####################################### Funciones #######################################
#########################################################################################

# Nos sirve para ver que usario esta logeado


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

#########################################################################################
############################ Funciones de routeo de direcciones #########################
#########################################################################################

@app.route('/json')
def jsonroute():
    return ModelLocker.consultAllDisponibles(db)

# Ruta raíz


@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/conocenos')
def conocenos():
    return render_template('Conocenos.html')

@app.route('/sucursales')
def sucursales():
    return render_template('Sucursales.html')

@app.route('/sucursales/valle')
def sucursalesValle():
    return render_template('Valle.html')


@app.route('/sucursales/lindavista')
def sucursalesLindavista():
    return render_template('Lindavista.html')


@app.route('/sucursales/satelite')
def sucursalesSatelite():
    return render_template('Satelite.html')


@app.route('/sucursales/aragon')
def sucursalesAragon():
    return render_template('Aragon.html')

#########################################################################################
##################################### Usuario cliente ###################################
#########################################################################################

# Inicio de sesion


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_active == False:
        # Mandamos formulario
        if request.method == 'POST':
            user = User(1, request.form['email'], request.form['password'])
            logged_user = ModelUser.login(db, user)
            # print(logged_user.email)
            # ¿Puede loggearse?
            if logged_user != None:

                if logged_user.password:
                    login_user(logged_user)
                    confirmed_user = ModelUser.consulta_email(
                        db, logged_user.email)
                    print(confirmed_user.tipo)
                    
                    if confirmed_user.confirmed:  # En caso de no ser confirmado reenvia un correo para confirmar
                        
                        if confirmed_user.tipo == 'usuario':
                            # print('si entro')
                            return redirect(url_for('home'))
                    
                        elif confirmed_user.tipo == 'admin':
                            return redirect(url_for('admin'))
                    
                        elif confirmed_user.tipo == 'repartidor':
                            return redirect(url_for('homeRepartidor'))
                    
                        else:
                            # flash("algo salio mal.")
                            return redirect(url_for('index'))
                    else:
                        if confirmed_user.tipo == 'usuario':
                            logout_user()
                            token = generate_confirmation_token(
                                logged_user.email)
                            return redirect(url_for('resend_confirmation', email=token))
                        else:
                            flash("Su usuario ha sido deshabilitado")
                            return render_template('ingresar.html')

                else:
                    flash("Usuario y/o contraseña incorrectos.")
                    return render_template('ingresar.html')

            else:
                flash("Usuario y/o contraseña incorrectos.")
                return render_template('ingresar.html')

        else:  # Se pide por get

            return render_template('ingresar.html')

    else:
        return redirect(url_for('home'))

# Cerrar sesion


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Home principal de usuario


@app.route('/home')
@login_required
def home():
    DATA = {
        'title': 'Home',
        'stylesheet': 'bienvenida.css',
    }
    # # print(current_user)
    user = ModelUser.consulta_email(db, current_user.email)
    print(user.tipo)
    if user.tipo == 'usuario':
        return render_template('home.html', data=DATA)
    elif user.tipo == 'admin':
        return redirect(url_for('admin'))
    elif user.tipo == 'repartidor':
        return redirect(url_for('homeRepartidor'))
    else:
        return redirect(url_for('index'))


# Registro de una nueva cuenta
@app.route('/registro', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        if current_user.is_active == True:
            logout_user()

        # ¿El correo no esta registrado?
        if ModelUser.check_email(db, request.form['email']) == False:
            user = User(1, request.form['email'],
                        request.form['password'],
                        request.form['nombre'],
                        request.form['telefono'],
                        request.form['direccion']
                        )
            execution = ModelUser.register(db, user)  # Registralo en la BD

            if execution != None:  # Se registro con exito entonces tengo sus datos
                token = generate_confirmation_token(user.email)

                # Envio de correo
                confirm_url = url_for(
                    'confirm_email', token=token, _external=True)
                template = render_template(
                    'correoValidaciones.html', confirm_url=confirm_url)
                subject = "Activación de cuenta - Sendiit"

                msg = Message(
                    subject,
                    # Cambiar al correo de usuario
                    recipients=[''+request.form['email']],
                    html=template,
                    sender="sendiitadsscrumios@gmail.com"
                )
                mail.send(msg)

                # login_user(execution) # Marco sus datos como logeado para que vea verificacion
                logout_user()
                return render_template('validacionCorreo.html',
                                       data={
                                           'title': 'Confirmacion de correo',
                                           'stylesheet': 'validacionCorreo.css',
                                       },
                                       nombre=user.nombre,
                                       email=user.email
                                       )

            else:
                flash("Algo salió mal, intenta de nuevo")
                return render_template('ingresar.html',
                                       data={
                                           'title': 'Iniciar sesion',
                                           'stylesheet': 'ingresar.css',
                                       }
                                       )

        else:
            flash("El correo ingresado ya ha sido registrado")
            return render_template('registrar.html')

    else:
        return render_template('registrar.html')


# Envio de confirmacion de correo
@app.route('/confirm/<token>')
# @login_required
def confirm_email(token):
    try:
        email = confirm_token(token)  # Regresa el email!

    except:
        flash('Algo salió mal. Por favor intenta de nuevo')
        # En caso de cuenta creada pero no confirmada
        return redirect(url_for('login'))

    # print(email)
    user = ModelUser.consulta_email(db, email)
    if user != None:

        if user.confirmed:
            flash('Tu cuenta ya está confirmada. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))

        else:
            print('llego')
            ModelUser.confirm_user(db, email)
            # flash('Cuenta Confirmada, inicia sesión.', 'success')
            # return redirect(url_for('login')) # Pantalla de succes confirmation!
            return render_template('ingresarVerificado.html',
                                   data={
                                       'title': 'Sucess',
                                       'stylesheet': 'ingresarVerificado.css',
                                   }
                                   )  # En caso de cuenta creada pero no confirmada

    else:  # Codigo expiro
        return render_template('tokenError.html',
                               data={
                                   'title': 'Token no encontrado',
                                   'stylesheet': 'tokenError.css',
                               }
                               )  # En caso de cuenta creada pero no confirmada


# Reenvío de correo
@app.route('/resend/<email>')
def resend_confirmation(email):
    hash_email = confirm_token(email)
    token = generate_confirmation_token(hash_email)
    # Envio de correo
    confirm_url = url_for('confirm_email', token=token, _external=True)
    template = render_template(
        'correoValidaciones.html', confirm_url=confirm_url)
    subject = "Activación de cuenta - Sendiit"

    msg = Message(
        subject,
        recipients=[''+email],  # Cambiar al correo de usuario
        html=template,
        sender="sendiitadsscrumios@gmail.com"
    )
    mail.send(msg)

    flash('Tu cuenta sigue son confirmar, hemos enviado un nuevo correo de confirmación.')

    return render_template('ingresar.html',
                           data={
                               'title': 'Iniciar sesion',
                               'stylesheet': 'ingresar.css',
                           })


# No llego ningun correo
# @app.route('/resendEmail/<email>?<nombre>')
@app.route('/resendEmail', methods=['GET', 'POST'])
def resend_email():

    # if ModelUser.check_email(db, request.form['email']) == True: # ¿El correo esta registrado?
    try:
        email = request.form['email']
        nombre = request.form['nombre']
        token = generate_confirmation_token(email)

        # Envio de correo
        confirm_url = url_for('confirm_email', token=token, _external=True)
        template = render_template(
            'correoValidaciones.html', confirm_url=confirm_url)
        subject = "Activación de cuenta - Sendiit"

        msg = Message(
            subject,
            # Cambiar al correo de usuario
            recipients=[''+request.form['email']],
            html=template,
            sender="sendiitadsscrumios@gmail.com"
        )
        mail.send(msg)

        flash('Se ha enviado un nuevo correo de confirmación.')
        return render_template('validacionCorreo.html',
                               data={
                                   'title': 'Confirmacion de correo',
                                   'stylesheet': 'validacionCorreo.css',
                               },
                               nombre=nombre,
                               email=email
                               )
    except:  # Intenta ingresar con un correo no registrado
        flash('Error. Usuario no registrado')
        return redirect(url_for('register'))


@app.route('/user/agregarTarjeta', methods=['GET', 'POST'])
@login_required
def agregarTarjeta():
    if request.method == 'POST':
        nombre = request.form['inputNombre']
        numtarjeta = request.form['inputNumero']
        expiracion = request.form['mes'] + "-" + request.form['year']
        cvv = request.form['inputCCV']
        tarjeta = Tarjeta(numtarjeta, expiracion, nombre, current_user.id, cvv)
        ModelTarjeta.register(db, tarjeta)

    return render_template('AgregarTarjeta.html')


@app.route('/user/formularioEnvio', methods=['GET', 'POST'])
@login_required
def formularioEnvio():
    if request.method == 'POST':
        envio = {
            "destino": request.form['destino'],
            "origen": request.form['origen'],
            "tamano": request.form['tamano'],
            "fragil": request.form['fragil'],
            "nombre": request.form['nombre'],
            "email": request.form['email'],
            "telefono": request.form['telefono'],
            "costo": request.form['costo'],
            "estado": 'EN ESPERA DE ENTREGA',
            "idusuario": current_user.id}
        # g.envio = Envio(origen, destino, tamano, fragil, estado, nombre, email, telefono, costo, idusuario)
        # print(g.envio)
        # ModelEnvio.register(db, envio)
        listTarjetas = ModelTarjeta.consultAll(db, current_user.id)
        if listTarjetas != None:
            return render_template('formularioPago.html', envio=envio, tarjetas=listTarjetas)
        else:
            return render_template('formularioPago.html', envio=envio, tarjetas=[])

    return render_template('FormularioEnvio.html')


@app.route('/user/formularioPago', methods=['GET', 'POST'])
@login_required
def formularioPago():
    if request.method == 'POST':
        origen = request.form['origen']
        destino = request.form['destino']
        tamano = request.form['tamano']
        fragil = request.form['fragil']
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        costo = request.form['costo']
        estado = request.form['estado']
        idusuario = request.form['idusuario']
        datos = Envio(origen, destino, tamano, fragil, estado,
                      nombre, email, telefono, costo, idusuario)
        ModelEnvio.register(db, datos)
        return render_template('PagoExitoso.html')
    listTarjetas = ModelTarjeta.consultAll(db, current_user.id)
    print(listTarjetas[0].numtarjeta)

    return render_template('formularioPago.html', tarjetas=listTarjetas)


@app.route('/user/ordenGenerada', methods=['GET', 'POST'])
@login_required
def ordenGenerada():
    last_delivery = ModelEnvio.consultLast(db)
    sender = ModelUser.consulta_telefono(db, current_user.id)
    print(last_delivery)
    print(sender)
    return render_template('OrdenGenerada.html', datos=last_delivery, sender=sender)


@app.route('/user/pagoExitoso')
@login_required
def pagoExitoso():
    return render_template('PagoExitoso.html')


@app.route('/user/pagoFracasado')
@login_required
def pagoFracasado():
    return render_template('PagoFracasado.html')

#########################################################################################
################################## Usuario administrador ################################
#########################################################################################
# Ruta raíz


@app.route('/admin')
@login_required
def admin():
    DATA = {
        'title': 'Catalogos',
        'stylesheet': '../static/css/Catalogos.css',
    }
    user = ModelUser.consulta_email(db, current_user.email)
    if user.tipo == 'admin':
        return render_template('Catalogos.html', data=DATA)
    else:
        return redirect(url_for('home'))

# Lockers - tabla
@app.route('/admin/lockers')
def lockers():
    DATA = {
        'title': 'Lockers',
        'stylesheet': '../static/css/tablalockers.css',
    }

    try:
        list_lockers = ModelLocker.consultAll(db)
        return render_template('TablaLockers.html', data=DATA, lockers=list_lockers)
    except:
        return render_template('TablaLockers.html', data=DATA, lockers=[])
    
# Lockers - formulario registrar
@app.route('/admin/lockers/agregar')
def lockersAgregar():
    DATA = {
        'title': 'Agregar Locker',
        'stylesheet': '../../static/css/AgregarLocker.css',
    }

    try:    
        list_locations = ModelLocation.consultAll(db)
        return render_template('AgregarLocker.html', data=DATA, locations=list_locations)
    except:
        return render_template('AgregarLocker.html', data=DATA, locations=[])

# Salvar datos post, insertamos, y redireccionamos a admin lockers

# Lockers - actualizar
@app.route('/admin/lockers/<int:id_locker>')
def lockersActualizar(id_locker):
    DATA = {
        'title': 'Agregar Locker',
        'stylesheet': '../../static/css/EditarLockers.css',
    }
    try:
        list_locations = ModelLocation.consultAll(db)
        current = ModelLocker.consult_by_id(db, id_locker)
        return render_template('EditarLockers.html', data=DATA, locations=list_locations, locker=current)
    except:
        return render_template('EditarLockers.html', data=DATA, locations=[], locker={})

# Lockers - registrar
@app.route('/admin/lockers/agregado', methods=['GET', 'POST'])
def lockersAgregado():
    ubicacion = request.form['ubicacion']
    direccion = request.form['direccion']
    cantidad = request.form['cantidad']
    cantidadS = 5 * int(cantidad)
    cantidadM = 6 * int(cantidad)
    cantidadL = 3 * int(cantidad)
    disponibilidad = cantidadS + cantidadM + cantidadL

    try:
        ModelLocker.register(db, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad)
        flash("Locker con ubicación " + ubicacion + " agregado con éxito")
        return redirect(url_for('lockersAgregar'))
    except:
        flash("Ha ocurrido un error al agregar locker")
        return redirect(url_for('lockersAgregar'))


# Lockers - eliminar
@app.route('/admin/lockers/actualizado', methods=['GET', 'POST'])
def lockersActualizado():
    id_recibido = request.form['id']
    direccion = request.form['direccion']
 
    try:
        ModelLocker.update(db, id_recibido, direccion)
        flash("Locker actualizado con éxito")
        return redirect(url_for('lockers'))
    except:
        flash("Ha ocurrido un error al actualizar valores del locker")
        return redirect(url_for('lockers'))


# Lockers - eliminar
@app.route('/admin/lockers/eliminar', methods=['GET', 'POST'])
def lockersEliminar():
    try:
        id_recibido = request.form['id']
        ModelLocker.delete(db, id_recibido)
        flash("Locker eliminado con éxito")
        return redirect(url_for('lockers'))
    except:
        flash("Ha ocurrido un error al eliminar locker")
        return redirect(url_for('lockers'))
    
# Lockers - modificar estado


@app.route('/admin/lockers/modificar-estado', methods=['GET', 'POST'])
def lockersModificarEstado():
    id_recibido = request.form['id']
    cursor = db.connection.cursor()
    sql_consulta = f"SELECT activo from lockers WHERE id={id_recibido}"
    cursor.execute(sql_consulta)
    estado = cursor.fetchone()
    estadoFin = -1
    if estado[0] == 0:
        estadoFin = 1
    else:
        estadoFin = 0
    sql = f"UPDATE lockers SET activo={estadoFin} WHERE id={id_recibido}"
    cursor.execute(sql)
    db.connection.commit()

    return redirect(url_for('lockers'))

# Lockers - tabla


@app.route('/admin/repartidores')
def repartidores():
    list_repartdores = ModelUser.consultRepartidoresAll(db)
    if list_repartdores != None:

        return render_template('altaRepartidores.html', repartidores=list_repartdores)
    else:
        return render_template('altaRepartidores.html', repartidores=[])


@app.route('/admin/repartidores/agregar', methods=['GET', 'POST'])
def repartidoresAgregar():
    # ModelUser.registerRepartidor(db)

    if request.method == 'POST':

        # ¿El correo no esta registrado?
        if ModelUser.check_email(db, request.form['email']) == False:
            user = User(1, request.form['email'],
                        request.form['password'],
                        request.form['nombre'],
                        request.form['telefono'],
                        request.form['direccion']
                        )
            execution = ModelUser.registerRepartidor(
                db, user)  # Registralo en la BD

            if execution != None:  # Se registro con exito entonces tengo sus datos
                # flash("Repartidor Agregado con exito")
                return render_template('agregarRepartidor.html')
            else:
                flash("Algo salió mal, intenta de nuevo")
                return render_template('agregarRepartidor.html')

        else:
            flash("Ese email ya esta registrado")
            return render_template('agregarRepartidor.html')

    else:
        return render_template('agregarRepartidor.html')
    # return render_template('agregarRepartidor.html')


# @app.route('/admin/lockers/agregar')
# def lockersAgregar():
#     DATA = {
#             'title' : 'Agregar Locker',
#             'stylesheet' : '../../static/css/AgregarLocker.css',
#             }
#     list_locations = ModelLocation.consultAll(db)

#     return render_template('AgregarLocker.html', data=DATA, locations = list_locations)


@app.route('/admin/repartidores/modificar-estado', methods=['GET', 'POST'])
def repartidoresModificarEstado():
    id_recibido = request.form['id']
    cursor = db.connection.cursor()
    sql_consulta = f"SELECT confirmed from user WHERE id={id_recibido}"
    cursor.execute(sql_consulta)
    estado = cursor.fetchone()
    estadoFin = -1
    if estado[0] == 0:
        estadoFin = 1
    else:
        estadoFin = 0
    sql = f"UPDATE user SET confirmed={estadoFin} WHERE id={id_recibido}"
    cursor.execute(sql)
    db.connection.commit()

    return redirect(url_for('repartidores'))


@app.route('/admin/repartidores/eliminar', methods=['GET', 'POST'])
def repartidoresEliminar():
    id_recibido = request.form['id']
    cursor = db.connection.cursor()
    cursor.execute('DELETE FROM user WHERE id = '+id_recibido)
    db.connection.commit()
    return redirect(url_for('repartidores'))
#########################################################################################
################################## Usuario repartidor ###################################
#########################################################################################


@app.route('/repartidor')
@login_required
def homeRepartidor():
    DATA = {
        'title': 'Home',
        'stylesheet': '../static/css/InicioRepartidor',
    }
    user = ModelUser.consulta_email(db, current_user.email)
    if user.tipo == 'repartidor':
        return render_template('InicioRepartidor.html', data=DATA)
    else:
        return redirect(url_for('home'))


@app.route('/repartidor/datos')
def datosRepartidor():
    repartidor = ModelUser.infoRepartidor(db, current_user.email)

    return render_template('InfoGeneral.html', repartidor=repartidor)


@app.route('/repartidor/pendientes', methods=['GET', 'POST'])
def listaDePaquetes():
    fly = 0
    if request.method == 'POST' and request.form['estado'] != 'ELEGIR ESTADO':
        estado = request.form['estado']
        list_paquetes = ModelRepartidor.paquetesAllCondition(
            db, estado, current_user.id)
        fly = 1
    else:
        list_paquetes = ModelRepartidor.paquetesAll(db, current_user.id)
    # print(list_paquetes)
    if list_paquetes != None:
        return render_template('pendientesRepartidor.html', paquetes=list_paquetes, fly=fly)
    else:
        return render_template('pendientesRepartidor.html', paquetes=[], fly=fly)


@app.route('/repartidor/rutaEnvio')
def rutaEnvio():
    repartidor = ModelUser.infoRepartidor(db, current_user.email)
    return render_template('RutaEnvio.html', repartidor=repartidor)


#############################################################################################################
############################# Funciones de redireccionamineto despues de un error ###########################
#############################################################################################################

# En caso de que no este logeado y quiera entrar al sistema redirige al login
def status_401(error):
    flash('Para acceder, por favor inicia sesión.')
    return redirect(url_for('login'))


# En caso de que el usuario acceda a una pagina no definida
def status_404(error):
    # return "<h1>Página no encontrada</h1>", 404
    return render_template('error404.html')


# This forces the app to start at '/'
if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
