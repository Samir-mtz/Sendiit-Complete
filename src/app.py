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

# Entities:
from models.entities.User import User

app = Flask(__name__)
csrf = CSRFProtect()
db = MySQL(app)

#########################################################################################
############################ Configuracion de servicio e-mail ###########################
#########################################################################################
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jairosotoy@gmail.com'
app.config['MAIL_USERNAME'] = 'jairosotoy@gmail.com'
app.config['MAIL_PASSWORD'] = "seewrbhlwlaphzud"
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
            'stylesheet' : 'index.css',
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
                
                    if confirmed_user.confirmed: # En caso de no ser confirmado reenvia un correo para confirmar
                        return redirect(url_for('home'))
                    else:
                        logout_user()
                        return redirect(url_for('resend_confirmation', email = logged_user.email))
                
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
            'stylesheet' : 'home.css',
            }
    # print(current_user)
    return render_template('home.html', data=DATA)


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
                                recipients=['armando@tecuani.me'], # Cambiar al correo de usuario
                                html=template,
                                sender="sendiit.ads@gmail.com"
                            )
                mail.send(msg)
                
                #login_user(execution) # Marco sus datos como logeado para que vea verificacion
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
                flash("Algo salio mal, intenta de nuevo")
                return render_template('ingresar.html',
                                        data = {
                                                    'title' : 'Iniciar sesion',
                                                    'stylesheet' : 'ingresar.css',
                                                }
                                        )
            
        else:
            flash("Ese email ya esta registrado")
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
        flash('Algo salio mal. Por favor intenta de nuevo')
        return redirect(url_for('login')) # En caso de cuenta creada pero no confirmada
    
    # print(email)
    user = ModelUser.consulta_email(db, email)
    if user!=None:
    
        if user.confirmed:
            flash('Tu cuenta ya esta confirmada. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
    
        else:
            print('llego')
            ModelUser.confirm_user(db, email)
            flash('Cuenta Confirmada, inicia sesión.', 'success')
            return redirect(url_for('login')) # Pantalla de succes confirmation!
    
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
    token = generate_confirmation_token(email)
    
    # Envio de correo
    confirm_url = url_for('confirm_email', token=token, _external=True)
    template = render_template('correoValidaciones.html', confirm_url=confirm_url)
    subject = "Activación de cuenta - Sendiit"

    msg = Message(
                    subject,
                    recipients=['armando@tecuani.me'], # Cambiar al correo de usuario
                    html=template,
                    sender="sendiit.ads@gmail.com"
                )
    mail.send(msg)

    flash('Tu cuenta no esta confirmada, hemos enviado un nuevo correo de confirmación.')
    
    return render_template('ingresar.html', 
                            data = {
                            'title' : 'Iniciar sesion',
                            'stylesheet' : 'ingresar.css',
                        })


# Pantalla confirmar correo
# @app.route('/confirmarCorreo')
# def confirmarCorreo():
#     DATA = {
#             'title' : 'Confirmacion de correo',
#             'stylesheet' : 'validacionCorreo.css',
#             }

#     return render_template('validacionCorreo.html', data=DATA)


# Verificacion del usuario 
# @app.route('/verificacion')
# @login_required
# def verificacion():
#     return render_template('verificacion.html')



#########################################################################################
############################# Funciones de redireccionamineto ###########################
#########################################################################################

#En caso de que no este logeado y quiera entrar al sistema redirige al login
def status_401(error):
    flash('No estas Logeado. Por favor, inicia sesión.')
    return redirect(url_for('login'))


#En caso de que el usuario acceda a una pagina no definida
def status_404(error):
    return "<h1>Página no encontrada</h1>", 404
    # return render_template('error404.html'), 404



# This forces the app to start at '/'
if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()