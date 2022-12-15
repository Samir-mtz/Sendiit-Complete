#########################################################################################
####################################    Librerias   #####################################
#########################################################################################
from flask import Flask, render_template, request, redirect, url_for, flash
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
from models.ModelLocation import ModelRepartidor

# Entities:
from models.entities.User import User
from models.entities.Locker import Locker
from models.entities.Location import Location

app = Flask(__name__)
csrf = CSRFProtect()
db = MySQL(app)

#########################################################################################
############################ Configuracion de servicio e-mail ###########################
#########################################################################################
app.config['MAIL_SERVER']='smtp.gmail.com'
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

#Nos sirve para ver que usario esta logeado
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


#########################################################################################
############################ Funciones de routeo de direcciones #########################
#########################################################################################

# Ruta raíz
@app.route('/')
def index():
    DATA = {
            'title' : 'Principal',
            'stylesheet' : 'inicio.css',
            }
    return render_template('index.html', data=DATA)

# Ruta raíz
@app.route('/conocenos')
def conocenos():
    DATA = {
            'title' : 'Conócenos',
            'stylesheet' : 'Conocenos.css',
            }
    return render_template('conocenos.html', data=DATA)

# Ruta raíz
@app.route('/sucursales')
def sucursales():
    DATA = {
            'title' : 'Sucursales',
            'stylesheet' : 'Sucursales.css',
            }
    return render_template('Sucursales.html', data=DATA)

@app.route('/sucursales/valle')
def sucursalesValle():
    DATA = {
            'title' : 'Colonia del valle',
            'stylesheet' : 'Maps.css',
            }
    return render_template('Valle.html', data=DATA)

@app.route('/sucursales/lindavista')
def sucursalesLindavista():
    DATA = {
            'title' : 'Colonia lindavista',
            'stylesheet' : 'Maps.css',
            }
    return render_template('Lindavista.html', data=DATA)


@app.route('/sucursales/satelite')
def sucursalesSatelite():
    DATA = {
            'title' : 'Satélite',
            'stylesheet' : 'Maps.css',
            }
    return render_template('Satelite.html', data=DATA)


@app.route('/sucursales/aragon')
def sucursalesAragon():
    DATA = {
            'title' : 'Colonia aragón',
            'stylesheet' : 'Maps.css',
            }
    return render_template('aragon.html', data=DATA)

#########################################################################################
##################################### Usuario cliente ###################################
#########################################################################################

# Inicio de sesion
@app.route('/login', methods=['GET', 'POST'])
def login():
    DATA = {
            'title' : 'Iniciar sesion',
            'stylesheet' : 'ingresar.css',
            }
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
                    confirmed_user = ModelUser.consulta_email(db, logged_user.email)
                    print(confirmed_user.tipo)
                    if confirmed_user.confirmed: # En caso de no ser confirmado reenvia un correo para confirmar
                        if confirmed_user.tipo=='usuario':
                            print('si entro')
                            return redirect(url_for('home'))
                        elif confirmed_user.tipo =='admin':
                            return redirect(url_for('admin'))
                        else:                                                                                                       
                            # flash("algo salio mal.")
                            return redirect(url_for('index'))
                    else:
                        logout_user()
                        token = generate_confirmation_token(logged_user.email)
                        return redirect(url_for('resend_confirmation', email = token))
                
                else:
                    flash("Usuario y/o contraseña incorrectos.")
                    return render_template('ingresar.html', data=DATA)

            else:
                flash("Usuario y/o contraseña incorrectos.")
                return render_template('ingresar.html', data=DATA)
        
        else:
            return render_template('ingresar.html', data=DATA)
    
    else:
        return redirect(url_for('home'))
        
        # return  render_template('ingresar.html', data=DATA)

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
            'title' : 'Home',
            'stylesheet' : 'bienvenida.css',
            }
    # print(current_user)
    user = ModelUser.consulta_email(db, current_user.email)
    print(user.tipo)
    if user.tipo == 'usuario':
        return render_template('home.html', data=DATA)
    elif user.tipo == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('index'))



# Registro de una nueva cuenta
@app.route('/registro', methods=['GET', 'POST'])
def register():
    DATA = {
            'title' : 'Registrar nueva cuenta',
            'stylesheet' : 'registrar.css',
            }

    if request.method == 'POST':
        if current_user.is_active == True:
            logout_user()

        if ModelUser.check_email(db, request.form['email'])==False: # ¿El correo no esta registrado?
            user = User(1, request.form['email'], 
                        request.form['password'], 
                        request.form['nombre'], 
                        request.form['telefono'],
                        request.form['direccion']
                        )
            execution = ModelUser.register(db, user) # Registralo en la BD
            
            if execution != None: # Se registro con exito entonces tengo sus datos
                token = generate_confirmation_token(user.email)

                # Envio de correo
                confirm_url = url_for('confirm_email', token=token, _external=True)
                template = render_template('correoValidaciones.html', confirm_url=confirm_url)
                subject = "Activación de cuenta - Sendiit"

                msg = Message(
                                subject,
                                recipients=['jairosotoy@gmail.com'], # Cambiar al correo de usuario
                                html=template,
                                sender="sendiitadsscrumios@gmail.com"
                            )
                mail.send(msg)
                
                # login_user(execution) # Marco sus datos como logeado para que vea verificacion
                logout_user()
                return render_template('validacionCorreo.html',
                                        data = {
                                                    'title' : 'Confirmacion de correo',
                                                    'stylesheet' : 'validacionCorreo.css',
                                                },
                                        nombre = user.nombre,
                                        email = user.email
                                    )
            
            else:
                flash("Algo salió mal, intenta de nuevo")
                return render_template('ingresar.html',
                                        data = {
                                                    'title' : 'Iniciar sesion',
                                                    'stylesheet' : 'ingresar.css',
                                                }
                                        )
            
        else:
            flash("El correo ingresado ya ha sido registrado")
            return render_template('registrar.html', data=DATA)    
    
    else:
        return render_template('registrar.html', data=DATA)


# Envio de confirmacion de correo
@app.route('/confirm/<token>')
# @login_required
def confirm_email(token):
    try:
        email = confirm_token(token) # Regresa el email!
    
    except:
        flash('Algo salió mal. Por favor intenta de nuevo')
        return redirect(url_for('login')) # En caso de cuenta creada pero no confirmada
    
    # print(email)
    user = ModelUser.consulta_email(db, email)
    if user!=None:
    
        if user.confirmed:
            flash('Tu cuenta ya está confirmada. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
    
        else:
            print('llego')
            ModelUser.confirm_user(db, email)
            # flash('Cuenta Confirmada, inicia sesión.', 'success')
            # return redirect(url_for('login')) # Pantalla de succes confirmation!
            return render_template('ingresarVerificado.html',
                                data = {
                                            'title' : 'Sucess',
                                            'stylesheet' : 'ingresarVerificado.css',
                                        }
                                ) # En caso de cuenta creada pero no confirmada
    
    else: #Codigo expiro
        return render_template('tokenError.html',
                                data = {
                                            'title' : 'Token no encontrado',
                                            'stylesheet' : 'tokenError.css',
                                        }
                                ) # En caso de cuenta creada pero no confirmada


# Reenvío de correo
@app.route('/resend/<email>')
def resend_confirmation(email):
    hash_email= confirm_token(email)
    token = generate_confirmation_token(hash_email)
    # Envio de correo
    confirm_url = url_for('confirm_email', token=token, _external=True)
    template = render_template('correoValidaciones.html', confirm_url=confirm_url)
    subject = "Activación de cuenta - Sendiit"

    msg = Message(
                    subject,
                    recipients=['jairosotoy@gmail.com'], # Cambiar al correo de usuario
                    html=template,
                    sender="sendiitadsscrumios@gmail.com"
                )
    mail.send(msg)

    flash('Tu cuenta sigue son confirmar, hemos enviado un nuevo correo de confirmación.')
    
    return render_template('ingresar.html', 
                            data = {
                            'title' : 'Iniciar sesion',
                            'stylesheet' : 'ingresar.css',
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
        template = render_template('correoValidaciones.html', confirm_url=confirm_url)
        subject = "Activación de cuenta - Sendiit"

        msg = Message(
                        subject,
                        recipients=['jairosotoy@gmail.com'], # Cambiar al correo de usuario
                        html=template,
                        sender="sendiitadsscrumios@gmail.com"
                    )
        mail.send(msg)

        flash('Se ha enviado un nuevo correo de confirmación.')
        return render_template('validacionCorreo.html',
                                            data = {
                                                        'title' : 'Confirmacion de correo',
                                                        'stylesheet' : 'validacionCorreo.css',
                                                    },
                                            nombre = nombre,
                                            email = email
                            )
    except: #Intenta ingresar con un correo no registrado
        flash('Error. Usuario no registrado')
        return redirect(url_for('register'))


#########################################################################################
################################## Usuario administrador ################################
#########################################################################################
# Ruta raíz
@app.route('/admin')
@login_required
def admin():
    DATA = {
            'title' : 'Catalogos',
            'stylesheet' : '../static/css/Catalogos.css',
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
            'title' : 'Lockers',
            'stylesheet' : '../static/css/tablalockers.css',
            }
    list_lockers = ModelLocker.consultAll(db)
    if list_lockers != None:
        return render_template('TablaLockers.html', data=DATA, lockers = list_lockers)
    else:
        return render_template('TablaLockers.html', data=DATA, lockers = [])


# Lockers - agregar
@app.route('/admin/lockers/agregar')
def lockersAgregar():
    DATA = {
            'title' : 'Agregar Locker',
            'stylesheet' : '../../static/css/AgregarLocker.css',
            }
    list_locations = ModelLocation.consultAll(db)

    return render_template('AgregarLocker.html', data=DATA, locations = list_locations)

# Salvar datos post, insertamos, y redireccionamos a admin lockers

# Lockers - actualizar
@app.route('/admin/lockers/<int:id_locker>')
def lockersActualizar(id_locker):
    DATA = {
            'title' : 'Agregar Locker',
            'stylesheet' : '../../static/css/EditarLockers.css',
            }
    
    list_locations = ModelLocation.consultAll(db)
    current = ModelLocker.consult_by_id(db, id_locker)
    
    return render_template('EditarLockers.html', data=DATA, locations = list_locations, locker = current)
    
# Lockers - eliminar
@app.route('/admin/lockers/agregado', methods=['GET', 'POST'])
def lockersAgregado():
    ubicacion = request.form['ubicacion']
    direccion = request.form['direccion']
    categoria = request.form['modelo-puertas']
    cantidad = int(request.form['cantidad'])
    cantidadS = 0
    cantidadM = 0
    cantidadL = 0

    if categoria == 13:
        cantidadS = 4 * cantidad
        cantidadM = 5 * cantidad
        cantidadL = 4 * cantidad
    elif categoria == 12:
        cantidadS = 5 * cantidad
        cantidadM = 4 * cantidad
        cantidadL = 3 * cantidad
    else:
        cantidadS = 4 * cantidad
        cantidadM = 3 * cantidad
        cantidadL = 1 * cantidad

    cursor = db.connection.cursor()
    cursor.execute('INSERT INTO lockers (ubicacion, direccion, categoria, cantidadS, cantidadM, cantidadL, disponibilidad) VALUES (%s,%s,%s,%s,%s,%s,%s)',
    (ubicacion, direccion, categoria, cantidadS, cantidadM, cantidadL, 0))
    db.connection.commit()
    return redirect(url_for('lockersAgregar'))


# Lockers - eliminar
@app.route('/admin/lockers/actualizado', methods=['GET', 'POST'])
def lockersActualizado():
    id_recibido = request.form['id']
    # ubicacion = request.form['ubicacion']
    direccion = request.form['direccion']
    # categoria = request.form['modelo-puertas']
    # cantidad = request.form['cantidad']
    # cantidadS = 0
    # cantidadM = 0
    # cantidadL = 0

    # if categoria == 13:
    #     cantidadS = 4 * cantidad
    #     cantidadM = 5 * cantidad
    #     cantidadL = 4 * cantidad
    # if categoria == 12:
    #     cantidadS = 5 * cantidad
    #     cantidadM = 4 * cantidad
    #     cantidadL = 3 * cantidad
    # if categoria == 8:
    #     cantidadS = 4 * cantidad
    #     cantidadM = 3 * cantidad
    #     cantidadL = 1 * cantidad
    # locker = {
    #     'ubicacion':ubicacion,
    #     'direccion':direccion,
    #     'categoria':categoria,
    #     'cantidadS':cantidadS,
    #     'cantidadM':cantidadM,
    #     'cantidadL':cantidadL,
    # } 

    cursor = db.connection.cursor()
    # sql = "UPDATE lockers SET ubicacion='"+locker.ubicacion+ "' WHERE id="+id_recibido
    cursor.execute('UPDATE lockers SET direccion = "'+direccion+'" WHERE id = '+id_recibido)
    db.connection.commit()
    return redirect(url_for('lockers'))

    # try:
    #     ModelLocker.update(db, id_recibido, locker)    
    #     return redirect(url_for('lockers'))
    # except:
    #     return redirect(url_for('admin'))
    
        
# Lockers - eliminar
@app.route('/admin/lockers/eliminar', methods=['GET', 'POST'])
def lockersEliminar():
    # DATA = {
    #         'title' : 'Agregar Locker',
    #         'stylesheet' : '../../static/css/AgregarLocker.css',
    #         }
    # ModelLocker.delete(db, id_locker)  
    # return redirect(url_for('lockers'))
    id_recibido = request.form['id']
    cursor = db.connection.cursor()
    # sql = "UPDATE lockers SET ubicacion='"+locker.ubicacion+ "' WHERE id="+id_recibido
    cursor.execute('DELETE FROM lockers WHERE id = '+id_recibido)
    db.connection.commit()  
    return redirect(url_for('lockers'))
    # return render_template('AgregarLocker.html', data=DATA)

# Lockers - modificar estado
@app.route('/admin/lockers/modificar-estado', methods=['GET', 'POST'])
def lockersModificarEstado():
    # DATA = {
    #         'title' : 'Agregar Locker',
    #         'stylesheet' : '../../static/css/AgregarLocker.css',
    #         }

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


#########################################################################################
################################## Usuario repartidor ###################################
#########################################################################################
@app.route('/repartidor/datos')
def datosRepartidor():
    repartidor = ModelUser.infoRepartidor(db, current_user.email)

    return render_template('#', repartidor = repartidor)

@app.route('/repartidor/pendientes', methods=['GET', 'POST'])
def listaDePaquetes():
    list_lockers = ModelRepartidor.paquetesAll(db, current_user.id)
    if list_lockers != None:
        return render_template('TablaLockers.html', data=DATA, lockers = list_lockers)
    else:
        return render_template('TablaLockers.html', data=DATA, lockers = [])






#############################################################################################################
############################# Funciones de redireccionamineto despues de un error ###########################
#############################################################################################################

#En caso de que no este logeado y quiera entrar al sistema redirige al login
def status_401(error):
    flash('Para acceder, por favor inicia sesión.')
    return redirect(url_for('login'))


#En caso de que el usuario acceda a una pagina no definida
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