###TO DO
#Hacer formula de precios

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
from flask import jsonify
import shutil

# Clases
# Models:
from models.ModelUser import ModelUser
from models.ModelLoker import ModelLocker
from models.ModelLocation import ModelLocation
from models.ModelRepartidor import ModelRepartidor
from models.ModelEnvio import ModelEnvio
from models.ModelTarjeta import ModelTarjeta
from models.ModelMapbox import ModelMapbox

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


@app.route('/tamanos/<origen>/<destino>')
def jsontamanos(origen, destino):
    return jsonify(ModelLocker.checkDisponibilidad(db, origen, destino))

@app.route('/json')
def jsonroute():
    return jsonify(ModelLocker.consultAllDisponibles(db))

@app.route('/json/<ubicacion>')
def jsonroutedestino(ubicacion):
    return jsonify(ModelLocker.consultDestinos(db, ubicacion))

@app.route('/coordenadas')
def coordenadas():
    return jsonify(ModelLocker.consultaCoordenadas(db))

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
            email = request.form['email']
            password = request.form['password']
            user = User(1, email, password)
            logged_user = ModelUser.login(db, user)
            # print(logged_user.email)
            # ¿Puede loggearse?
            if logged_user != None:

                if logged_user.password:
                    login_user(logged_user)
                    confirmed_user = ModelUser.consulta_email(
                        db, logged_user.email)
                    # print(confirmed_user.tipo)
                    
                    if confirmed_user.confirmed:  # En caso de no ser confirmado reenvia un correo para confirmar
                        
                        if confirmed_user.tipo == 'usuario':
                            # print('si entro')
                            return redirect(url_for('homeCliente'))
                    
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
                            return redirect(url_for('resend_confirmation', email=email))
                        elif confirmed_user.tipo == 'repartidor':
                            if confirmed_user.confirmed_on == None:
                                logout_user()
                                return redirect(url_for('resend_confirmation_repartidor', email=email))
                            else:
                                flash("Su usuario ha sido deshabilitado")
                                return render_template('ingresar.html')
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
        return redirect(url_for('homeCliente'))

# Cerrar sesion


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Home principal de usuario
@app.route('/homeCliente')
@login_required
def homeCliente():
    user = ModelUser.consulta_email(db, current_user.email)
    # print(user.tipo)
    if user.tipo == 'usuario':
        return render_template('InicioCliente.html')
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
                    recipients=[''+request.form['email']],
                    html=template,
                    sender="sendiitadsscrumios@gmail.com"
                )
                mail.send(msg)
                # login_user(execution) # Marco sus datos como logeado para que vea verificacion
                logout_user()
                return render_template('validacionCorreo.html', nombre=user.nombre, email=user.email)
            else:
                flash("Algo salió mal, intenta de nuevo")
                return render_template('ingresar.html')
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
        # En caso de cuenta creada pero no confirmada
        flash('Algo salió mal. Por favor intenta de nuevo')
        return redirect(url_for('login'))

    # print(email)
    user = ModelUser.consulta_email(db, email)
    if user != None:
        if user.confirmed:
            flash('Tu cuenta ya está confirmada. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
        else:
            # print('llego')
            ModelUser.confirm_user(db, email)
            return render_template('ingresarVerificado.html')  # En caso de cuenta creada pero no confirmada
    else:  # Codigo expiro
        return render_template('tokenError.html')  # En caso de cuenta creada pero no confirmada


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

    flash('Tu cuenta sigue sin confirmar, hemos enviado un nuevo correo de confirmación.')
    return render_template('ingresar.html')


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
        return render_template('validacionCorreo.html', nombre=nombre, email=email)
    except:  # Intenta ingresar con un correo no registrado
        flash('Error. Usuario no registrado')
        return redirect(url_for('register'))

@app.route('/recuperar', methods = ['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        try:
            email = request.form['email']
            verificar = ModelUser.check_email(db, email)
            if verificar == True:
                token = generate_confirmation_token(email)
                confirm_url = url_for('confirm_email_restablecer', token=token, _external=True)
                template = render_template('correoRecuperarContrasena.html', confirm_url=confirm_url)
                subject = "Recuperación de cuenta - Sendiit"
                msg = Message(subject, recipients=[email], html=template, sender="sendiitadsscrumios@gmail.com")
                mail.send(msg)
                return render_template('validacionCorreoRecuperar.html', email=email)
            else:
                flash('El usuario ingresado no está registrado en el sistema')
                return render_template('recuperar.html')
        except:
            flash('Error al verificar datos')
            return render_template('recuperar.html')
    else:
        return render_template('recuperar.html')

# Envio de confirmacion de correo
@app.route('/confirmRestablecer/<token>')
def confirm_email_restablecer(token):
    try:
        email = confirm_token(token)
    except:
        # En caso de cuenta creada pero no confirmada
        flash('Algo salió mal. Por favor intenta de nuevo')
        return redirect(url_for('login'))

    user = ModelUser.consulta_email(db, email)
    if user != None:
        return render_template('restablecer.html', usuario = user)  # En caso de cuenta creada pero no confirmada
    else:  # Codigo expiro
        return render_template('tokenErrorContrasena.html')  # En caso de cuenta creada pero no confirmada

@app.route('/resendEmailRecuperacion', methods=['GET', 'POST'])
def resend_email_recuperacion():
    try:
        email = request.form['email']
        token = generate_confirmation_token(email)
        confirm_url = url_for('confirm_email_restablecer', token=token, _external=True)
        template = render_template('correoRecuperarContrasena.html', confirm_url=confirm_url)
        subject = "Recuperación de cuenta - Sendiit"
        msg = Message(subject, recipients=[email], html=template, sender="sendiitadsscrumios@gmail.com")
        mail.send(msg)
        flash('Se ha enviado un nuevo correo de recuperación de cuenta.')
        return render_template('validacionCorreoRecuperar.html', email=email)
    except:  # Intenta ingresar con un correo no registrado
        flash('Ha ocurrido un error en el proceso, inténtalo de nuevo más tarde')
        return redirect(url_for('login'))

@app.route('/contrasenaRestablecido', methods = ['POST'])
def contrasenaRestablecido():
    try:
        id_usuario = request.form['id']
        contrasena = request.form['password']
        confirmed_on = request.form['confirmed']
        print(confirmed_on)
        if confirmed_on == 'None':
            print('Here')
            ModelUser.update_contrasena_repartidor(db, id_usuario, contrasena)
        else:
            ModelUser.update_contrasena(db, id_usuario, contrasena)
        return render_template('ingresarRecuperado.html')
    except:
        flash('Algo salió mal. Por favor intenta de nuevo')
        return redirect(url_for('login'))

# Reenvío de correo
@app.route('/resendRepartidor/<email>')
def resend_confirmation_repartidor(email):
    # hash_email = confirm_token(email)
    token = generate_confirmation_token(email)
    # Envio de correo
    confirm_url = url_for('confirm_email_restablecer', token=token, _external=True)
    template = render_template('correoValidacionesRepartidor.html', confirm_url=confirm_url)
    subject = "Activación de cuenta - Sendiit"

    msg = Message(subject, recipients=[email], html=template, sender="sendiitadsscrumios@gmail.com")
    mail.send(msg)

    flash('Tu cuenta sigue sin confirmar, hemos enviado un nuevo correo de cambio de contraseña.')
    return render_template('ingresar.html')


@app.route('/user/tarjetas', methods=['GET', 'POST'])
@login_required
def userTarjetas():
    list_tarjetas = ModelTarjeta.consultAll(db, current_user.id)
    return render_template('tarjetasUsuario.html', tarjetas = list_tarjetas)


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


@app.route('/user/tarjetas/<int:id_tarjeta>')
def tarjetasActualizar(id_tarjeta):
    try:
        current = ModelTarjeta.consult_by_id(db, id_tarjeta)
        return render_template('EditarTarjeta.html', tarjeta=current)
    except:
        return render_template('EditarTarjeta.html', tarjeta={})

@app.route('/user/tarjetas/actualizado', methods=['GET', 'POST'])
def tarjetasActualizado():
    id_recibido = request.form['id']
    nombre = request.form['nombre']
    numtarjeta = request.form['numtarjeta']
    expiracion = request.form['mes'] + "-" + request.form['year']
    cvv = request.form['cvv']
    
    try:
        ModelTarjeta.update(db, id_recibido, nombre, numtarjeta, expiracion, cvv)
        flash("Tarjeta actualizado con éxito")
        return redirect(url_for('userTarjetas'))
    except:
        flash("Ha ocurrido un error al actualizar valores de tarjeta")
        return redirect(url_for('userTarjetas'))


@app.route('/user/tarjetas/eliminar', methods=['GET', 'POST'])
def tarjetasEliminar():
    id_recibido = request.form['id']
    try:
        ModelTarjeta.delete(db, id_recibido)
        flash("Tarjeta eliminada con éxito")
        return redirect(url_for('userTarjetas'))
    except:
        flash("Ha ocurrido un error al eliminar tarjeta")
        return redirect(url_for('userTarjetas'))

@app.route('/user/formularioEnvio', methods=['GET', 'POST'])    
@login_required
def formularioEnvio():
    user = ModelUser.consulta_email(db, current_user.email)
    # print(user.tipo)
    if user.tipo == 'admin':
        return redirect(url_for('admin'))
    elif user.tipo == 'repartidor':
        return redirect(url_for('homeRepartidor'))
    if user.tipo == 'usuario':    
        if request.method == 'POST':
            
            destino = request.form['destino']
            origen = request.form['origen']
            tamano = request.form['tamano']
            fragil = request.form['fragil']
            nombre = request.form['nombre']
            email = request.form['email']
            telefono = request.form['telefono']
            costo = request.form['costo']
            estado = 'POR DEPOSITARSE EN LOCKER POR EL CLIENTE'
            idusuario = current_user.id
            datos = Envio(origen, destino, tamano, fragil, estado, nombre, email, telefono, costo, idusuario)

            ModelEnvio.register(db, datos)
            return render_template('PagoExitoso.html')
        
        ###Funcionalidad del mapbox
        lockers = ModelMapbox.consultaCoordenadas(db)
        shutil.copy("src/static/js/origen.js", "src/static/js/mapbox2.js")
        destFile = r"src/static/js/mapbox2.js"
        with open(destFile, 'a', encoding="utf-8") as f:

            f.write("\nmap.on('load', () => {\n\
            // make an initial directions request that\n\
            // starts and ends at the same location\n\
            map.addSource('places', {\n\
                'type': 'geojson',\n\t\
                'data': {\n\t\t\
                    'type': 'FeatureCollection',\n\t\t\t\
                    'features': [")
            for i in range(len(lockers)):
                f.write(f"""
                        {{
                        'type': 'Feature',
                        'properties': {{
                            'description':
                                '<strong>{lockers[i][0]}</strong><p>{lockers[i][1]}</p>',
                            'icon': 'post'
                        }},
                        'geometry': {{
                            'type': 'Point',
                            'coordinates': [{lockers[i][2]}, {lockers[i][3]}]
                        }}
                    }}
                    """)
                if i!=len(lockers):
                    f.write(",\n\t\t\t\t\t\t\t")
            
            f.write("\
                                ]\n\t\t\t\
                            }\n\t\t\
                        });\n\t\
                        map.addLayer({\n\t\
                            'id': 'places',\n\t\t\
                            'type': 'symbol',\n\t\t\
                            'source': 'places',\n\t\t\
                            'layout': {\n\t\t\
                                'icon-image': ['get', 'icon'],\n\t\t\t\
                                'icon-size': 0.25,\n\t\t\t\
                                'icon-allow-overlap': true\n\t\t\t\
                            }\n\t\t\
                        });\n\
                    });\n\
            ")

            f.write("\nlet coordinatesPoints = new Map();")
            for i in range(len(lockers)):
                f.write(f"""
                    \ncoordinatesPoints.set('{lockers[i][0]}',[{lockers[i][2]}, {lockers[i][3]}])
                """)
            f.write("\nfunction convertMyRoute(inicio, fin){\n\
                        getRoute(coordinatesPoints.get(inicio), coordinatesPoints.get(fin))\n\
                    }")
        shutil.copy("src/static/js/mapbox2.js", "src/static/js/mapboxfinal.js")
        ##Fin funcionalidad Map Box
        ##Cargamos tarjetas
        listTarjetas = ModelTarjeta.consultAll(db, current_user.id)
        if listTarjetas != None:
            return render_template('formulariosPaquete.html', tarjetas=listTarjetas)
        return render_template('formulariosPaquete.html', tarjetas=[])
    else:
        return redirect(url_for('index'))

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
        datos = Envio(origen, destino, tamano, fragil, estado, nombre, email, telefono, costo, idusuario)
        ModelEnvio.register(db, datos)
        return render_template('PagoExitoso.html')
    listTarjetas = ModelTarjeta.consultAll(db, current_user.id)

    return render_template('formularioPago.html', tarjetas=listTarjetas)


@app.route('/user/ordenGenerada', methods=['GET', 'POST'])
@login_required
def ordenGenerada():
    last_delivery = ModelEnvio.consultLast(db)
    sender = ModelUser.consulta_telefono(db, current_user.id)
    # print(last_delivery)
    # print(sender)
    return render_template('OrdenGenerada.html', datos=last_delivery, sender=sender)


@app.route('/user/pagoExitoso')
@login_required
def pagoExitoso():
    return render_template('PagoExitoso.html')


@app.route('/user/pagoFracasado')
@login_required
def pagoFracasado():
    return render_template('PagoFracasado.html')

@app.route('/user/rastrearEnvio/<id>')
@login_required
def userRastrear(id):
    if(current_user.tipo == None):
        envio = ModelEnvio.rastreoEnvio(id)
        if envio.estado == "POR DEPOSITARSE EN LOCKER POR EL CLIENTE":
            return render_template('estatus_1.html', envio)
        elif estado.estado == "EN ESPERA DEL REPARTIDOR":
            return render_template('estatus_2.html', envio)

        elif estado.estado == "EN CAMINO":
            return render_template('estatus_3.html', envio)

        elif estado.estado == "ENTREGADO EN LOCKER DESTINO":
            return render_template('estatus_4.html', envio)

        elif estado.estado == "RECOGIDO":
            return render_template('estatus_5.html', envio)

        return render_template('PagoFracasado.html', envio)
    else:
        envio = ModelEnvio.rastreoEnvio(id)
        if envio.estado == "POR DEPOSITARSE EN LOCKER POR EL CLIENTE":
            return render_template('estatusCliente_1.html', envio)
        elif estado.estado == "EN ESPERA DEL REPARTIDOR":
            return render_template('estatusCliente_2.html', envio)

        elif estado.estado == "EN CAMINO":
            return render_template('estatusCliente_3.html', envio)

        elif estado.estado == "ENTREGADO EN LOCKER DESTINO":
            return render_template('estatusCliente_4.html', envio)

        elif estado.estado == "RECOGIDO":
            return render_template('estatusCliente_5.html', envio)

        return render_template('PagoFracasado.html', envio)

#########################################################################################
################################## Usuario administrador ################################
#########################################################################################
# Ruta raíz
@app.route('/admin')
@login_required
def admin():
    user = ModelUser.consulta_email(db, current_user.email)
    if user.tipo == 'admin':
        return render_template('Catalogos.html')
    else:
        return redirect(url_for('home'))

# Administracion de lockers
@app.route('/admin/lockers', methods = ['GET', 'POST'])
def lockers():
    if request.method == 'GET': # Por get
        try:
            list_lockers = ModelLocker.consultAll(db)
            return render_template('TablaLockers.html', lockers=list_lockers)
        except:
            flash("Ha ocurrido un error al consultar lockers")
            return render_template('TablaLockers.html', lockers=[])
    if request.method == 'POST': # Por post
        try:
            dato = request.form['dato_consulta']
            list_lockers = ModelLocker.consult_to_search(db, dato)
            flash("Resultados de búsqueda para '"+dato+"'")
            return render_template('TablaLockers.html', lockers=list_lockers)
        except:
            return render_template('TablaLockers.html', lockers=[])
        

@app.route('/admin/lockers/agregar')
def lockersAgregar():
    return render_template('agregarLockers.html')

@app.route('/admin/lockers/agregado', methods=['POST'])
def lockersAgregado():
    ubicacion = request.form['Ubicacion']
    direccion = request.form['Direccion']
    cantidad = request.form['Cantidad']
    latitud = request.form['Latitud']
    longitud = request.form['Longitud']
    cantidadS = 5 * int(cantidad)
    cantidadM = 6 * int(cantidad)
    cantidadL = 3 * int(cantidad)
    disponibilidad = cantidadS + cantidadM + cantidadL

    try:
        ModelLocker.register(db, ubicacion, direccion, cantidadS, cantidadM, cantidadL, disponibilidad, latitud, longitud)
        flash("Locker con ubicación '" + ubicacion + "' agregado con éxito")
        return redirect(url_for('lockers'))
    except:
        flash("Ha ocurrido un error al agregar locker")
        return redirect(url_for('lockers'))

@app.route('/admin/lockers/modificar-estado', methods=['GET', 'POST'])
def lockersModificarEstado():
    try:
        id_recibido = request.form['id']
        estado_recibido = int(request.form['confirmed'])
        estado_recibido = 1 - estado_recibido
        ModelLocker.modificar_estado(db, id_recibido, estado_recibido)
        currentLocker = ModelLocker.consult_by_id(db, id_recibido)
        flash(f"Estado de locker {currentLocker.ubicacion} actualizado con éxito")
        return redirect(url_for('lockers'))
    except:
        flash("Ha ocurrido un error al actualizar el estado locker")
        return redirect(url_for('lockers'))

@app.route('/admin/lockers/actualizar', methods=['GET','POST'])
def lockersActualizar():
    try:
        id_locker = request.form['id']
        current = ModelLocker.consult_by_id(db, id_locker)
        cantidad = str(current.cantidadS/5)
        i=0
        nolockers = ''
        while cantidad[i] != '.' and i < len(cantidad):
            nolockers += cantidad[i]
            i+=1
        return render_template('EditarLockers.html', locker=current, cantidad=nolockers)
    except:
        return render_template('EditarLockers.html', locker={}, cantidad='')

@app.route('/admin/lockers/actualizado', methods=['POST'])
def lockersActualizado():
    id_recibido = request.form['id']
    direccion = request.form['Direccion']
    cantidad = request.form['Cantidad']
    latitud = request.form['Latitud']
    longitud = request.form['Longitud']
    cantidadS = 5 * int(cantidad)
    cantidadM = 6 * int(cantidad)
    cantidadL = 3 * int(cantidad)
    try:
        ModelLocker.update(db, id_recibido, direccion, cantidadS, cantidadM, cantidadL, latitud, longitud)
        currentLokcer = ModelLocker.consult_by_id(db, id_recibido)
        flash(f"Locker con ubicación '{currentLokcer.ubicacion}' actualizado con éxito")
        return redirect(url_for('lockers'))
    except:
        flash("Ha ocurrido un error al actualizar valores del locker")
        return redirect(url_for('lockers'))
    
@app.route('/admin/lockers/eliminar', methods=['POST'])
def lockersEliminar():
    try:
        id_recibido = request.form['id']
        currentLokcer = ModelLocker.consult_by_id(db, id_recibido)
        ModelLocker.delete(db, id_recibido)
        flash(f"Locker con ubicación {currentLokcer.ubicacion} eliminado con éxito")
        return redirect(url_for('lockers'))
    except:
        flash("Ha ocurrido un error al eliminar locker")
        return redirect(url_for('lockers'))


# Administracion de repartidores
@app.route('/admin/repartidores', methods = ['GET', 'POST'])
def repartidores():
    if request.method == 'GET':
        try:
            list_repartdores = ModelUser.consultRepartidoresAll(db)
            return render_template('tablaRepartidores.html', repartidores=list_repartdores)
        except:
            flash("Ha ocurrido un error al consultar reprtidores")
            return render_template('tablaRepartidores.html', repartidores=[])
    if request.method == 'POST': # Por post
        try:
            dato = request.form['dato_consulta']
            list_repartdores = ModelUser.consult_to_search_repartidor(db, dato)
            flash("Resultados de búsqueda para '"+dato+"'")
            return render_template('tablaRepartidores.html', repartidores=list_repartdores)
        except:
            return render_template('tablaRepartidores.html', repartidores=[])
    
@app.route('/admin/repartidores/agregar')
def repartidoresAgregar():
    return render_template('agregarRepartidor.html')

@app.route('/admin/repartidores/agregado', methods=['POST'])
def repartidoresAgregado():
    try:
        email = request.form['email']
        password = request.form['password']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        sucursal =request.form['sucursal']  
        
        if ModelUser.check_email(db, email) == False:
            execution = ModelUser.registerRepartidor(db, email, password, nombre, telefono, direccion, sucursal)  # Registralo en la BD
            if execution != None:  # Se registro con exito entonces tengo sus datos
                token = generate_confirmation_token(email)
                
                confirm_url = url_for('confirm_email_restablecer', token=token, _external=True)
                template = render_template('correoValidacionesRepartidor.html', confirm_url=confirm_url)
                subject = "Activación de cuenta - Sendiit"
                
                msg = Message(subject, recipients=[email], html=template, sender="sendiitadsscrumios@gmail.com")
                
                mail.send(msg)        
                
                flash("Repartidor "+ nombre +" agregado con exito y en espera de activación")
                return redirect(url_for('repartidores'))
            else:
                flash("Algo salió mal, intenta de nuevo")
                return redirect(url_for('repartidores'))
        else:
            flash("Ese email ya esta registrado")
            return render_template('agregarRepartidor.html')
    except:
        flash("Algo salió mal, intenta de nuevo")
        return redirect(url_for('repartidores'))

@app.route('/admin/repartidores/modificar-estado', methods=['POST'])
def repartidoresModificarEstado():    
        try:
            id_recibido = request.form['id']
            currentRepartidor = ModelUser.consult_repartidor_by_id(db, id_recibido)
            if currentRepartidor.confirmed_on == None:
                flash(f"No es posible modificar estado del repartidor {currentRepartidor.nombre}. La cuenta no ha sido activada")
                return redirect(url_for('repartidores'))
            else:
                estado_recibido = int(request.form['confirmed'])
                estado_recibido = 1 - estado_recibido
                ModelUser.modificar_estado(db, id_recibido, estado_recibido)
                flash(f"Estado de repartidor {currentRepartidor.nombre} actualizado con éxito")
                return redirect(url_for('repartidores'))
        except:
            flash("Ha ocurrido un error al actualizar el estado repartidor")
            return redirect(url_for('repartidores'))

@app.route('/admin/repartidores/editar', methods=['GET','POST'])
def repartidoresActualizar():
    try:
        id_repartidor = request.form['id']
        current = ModelUser.consult_repartidor_by_id(db, id_repartidor)
        return render_template('editarRepartidores.html', repartidor = current)
    except:
        flash("Ha ocurrido un error al obtener datos del repartidor")
        return render_template('editarRepartidores.html', repartidor = {})

@app.route('/admin/repartidores/actualizado', methods=['GET', 'POST'])
def repartidoresActualizado():
    try:
        id_recibido = request.form['id']
        nombre = request.form['Nombre']
        email = request.form['Email']
        telefono = request.form['Telefono']
        direccion = request.form['Direccion']
        ModelUser.update_cliente(db, id_recibido,nombre, email, telefono, direccion)
        flash(f"Repartidor {nombre} actualizado con éxito")
        return redirect(url_for('repartidores'))
    except:
        flash("Ha ocurrido un error al actualizar valores del repartidor")
        return redirect(url_for('repartidores'))

@app.route('/admin/repartidores/eliminar', methods=['GET', 'POST'])
def repartidoresEliminar():
    try:
        id_recibido = request.form['id']
        currentRepartidor = ModelUser.consult_repartidor_by_id(db, id_recibido)
        ModelUser.delete(db, id_recibido)
        flash(f"Repartidor {currentRepartidor.nombre} eliminado con éxito")
        return redirect(url_for('repartidores'))
    except:
        flash("Ha ocurrido un error al eliminar al repartidor")
        return redirect(url_for('repartidores'))

# Administracion de clientes
@app.route('/admin/clientes', methods = ['GET', 'POST'])
def clientes():
    if request.method == 'GET':
        try:
            list_clientes = ModelUser.consultClientesAll(db)
            return render_template('tablaClientes.html', clientes=list_clientes)
        except:
            flash("Ha ocurrido un error al consultar clientes")
            return render_template('tablaClientes.html', clientes=[])
    if request.method == 'POST': # Por post
        try:
            dato = request.form['dato_consulta']
            list_clientes = ModelUser.consult_to_search_cliente(db, dato)
            flash("Resultados de búsqueda para '"+dato+"'")
            return render_template('tablaClientes.html', clientes=list_clientes)
        except:
            return render_template('tablaClientes.html', clientes=[])

@app.route('/admin/clientes/actualizar', methods=['GET','POST'])
def clientesActualizar():
    try:
        id_recibido = request.form['id']
        current = ModelUser.consult_cliente_by_id(db, id_recibido)
        return render_template('editarUsuarios.html', cliente = current)
    except:
        flash("Ha ocurrido un error al obtener datos del cliente")
        return render_template('editarUsuarios.html', cliente = current)

@app.route('/admin/clientes/actualizado', methods=['GET', 'POST'])
def clientesActualizado():
    try:
        id_recibido = request.form['id']
        nombre = request.form['Nombre']
        email = request.form['Email']
        telefono = request.form['Telefono']
        direccion = request.form['Direccion']
        ModelUser.update_cliente(db, id_recibido,nombre, email, telefono, direccion)
        flash(f"Usuario {nombre} actualizado con éxito")
        return redirect(url_for('clientes'))
    except:
        flash("Ha ocurrido un error al actualizar valores del cliente")
        return redirect(url_for('clientes'))

@app.route('/admin/clientes/eliminar', methods=['GET','POST'])
def clientesEliminar():
    try:
        id_recibido = request.form['id']
        currentUser = ModelUser.consult_cliente_by_id(db, id_recibido)
        ModelUser.delete(db, id_recibido)
        flash(f"Usuario {currentUser.nombre} eliminado con éxito")
        return redirect(url_for('clientes'))
    except:
        flash("Ha ocurrido un error al eliminar al cliente")
        return redirect(url_for('clientes'))


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
        usuario = ModelUser.get_by_id(db,current_user.id)

        if estado=="EN ESPERA DEL REPARTIDOR":
            list_paquetes = ModelRepartidor.paquetesRecolectar(db, usuario.sucursal)
        elif estado=="EN CAMINO":
            list_paquetes = ModelRepartidor.paquetesEntregar(db, usuario.sucursal)
        fly = 1
    else:
        usuario = ModelUser.get_by_id(db,current_user.id)
        list_paquetes = ModelRepartidor.paquetesAll(db, usuario.sucursal)
    # print(list_paquetes)
    if list_paquetes != None:
        return render_template('pendientesRepartidor.html', paquetes=list_paquetes, fly=fly)
    else:
        return render_template('pendientesRepartidor.html', paquetes=[], fly=fly)


@app.route('/repartidor/rutaEnvio')
def rutaEnvio():
    repartidor = ModelUser.infoRepartidor(db, current_user.email)
    return render_template('RutaEnvio.html', repartidor=repartidor)

@app.route('/repartidor/modificar-estado', methods=['GET', 'POST'])
def repartidorModificarEstado():
    try:
        id_recibido = request.form['id']
        estado = ModelEnvio.consultaEstado(db, id_recibido)
        if estado == "EN ESPERA DEL REPARTIDOR":
            new_estado = "EN CAMINO"
        elif estado == "EN CAMINO":
            new_estado = "ENTREGADO EN LOCKER DESTINO"
        ModelEnvio.ChangeStatus(db, id_recibido, new_estado)
        flash("Estado de locker modificado con éxito")
        return redirect(url_for('listaDePaquetes'))
    except:
        flash("Ha ocurrido un error al actualizar el estado del paquete")
        return redirect(url_for('listaDePaquetes'))

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
