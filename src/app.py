from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import config
from flask_mail import Mail, Message
from models.token import generate_confirmation_token, confirm_token

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'armando.samir.mtzi@gmail.com'
app.config['MAIL_USERNAME'] = 'armando.samir.mtzi@gmail.com'
app.config['MAIL_PASSWORD'] = "tpxaktlzgmsbehow"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
login_manager_app = LoginManager(app)

#Nos sirve para ver que usario esta logeado
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)
####

# A cada función se le pasa como argumento extra en la función render_template:
#  el nombre de la página y el no,bre del css a tomar
@app.route('/')
def index():
    DATA = {
        'title' : 'Principal',
        'stylesheet' : 'index.css',
    }
    return render_template('index.html', data=DATA)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # TITLE = 'Iniciar sesion'
    # STYLESHEET = 'ingresar.css'
    DATA = {
        'title' : 'Iniciar sesion',
        'stylesheet' : 'ingresar.css',
    }
    if request.method == 'POST':
        # print(request.form['email'])
        # print(request.form['password'])
        user = User(1, request.form['email'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            
            if logged_user.password:
                login_user(logged_user)
                confirmed_user = ModelUser.consulta_email(db, logged_user.email)
                if confirmed_user.confirmed: ##En caso de no ser confirmado reenvia un correo para confirmar
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('resend_confirmation'))
            else:
                flash("contraseña incorrectos")
                return render_template('ingresar.html', data=DATA)
        else:
            flash("Usuario  incorrectos")
            return render_template('ingresar.html', data=DATA)
    else:
        return render_template('ingresar.html', data=DATA)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    DATA = {
        'TITLE' : 'Home',
        'STYLESHEET' : 'home.css',
    }
    return render_template('home.html', data=DATA)

#Funciones de Registro
@app.route('/registro', methods=['GET', 'POST'])
def register():
    DATA = {
        'title' : 'Registrar nueva cuenta',
        'stylesheet' : 'registrar.css',
    }
    if request.method == 'POST':

        if ModelUser.check_email(db, request.form['email'])==False: #¿El correo no esta registrado?

            user = User(1, request.form['email'], request.form['password'], request.form['nombre'], 
                            request.form['telefono'], request.form['direccion'])
            execution = ModelUser.register(db, user) #Registralo en la BD
            if execution != None: #Se registro con exito entonces tengo sus datos
                # token = generate_confirmation_token(user.email)
                token = generate_confirmation_token(user.email)

                ####Envio de correo
                confirm_url = url_for('confirm_email', token=token, _external=True)
                template = render_template('email.html', confirm_url=confirm_url)
                subject = "Por favor Confirma tu correo - Sendiit"

                msg = Message(
                    subject,
                    recipients=['jairosotoy@gmail.com'],###Cambiar al correo de usuario
                    html=template,
                    sender="armando.samir.mtzi@gmail.com"
                )
                mail.send(msg)
                #################

                login_user(execution) #Marco sus datos como logeado para que vea verificacion
                return render_template('validacionCorreo.html', data = {
                                                                        'title' : 'Confirmacion de correo',
                                                                        'stylesheet' : 'validacionCorreo.css',
                                                                        }
                                    )
                # return redirect(url_for('/confirmarCorreo')) #Renderizo verificacion
            else:
                flash("Algo salio mal, intenta de nuevo")
                return render_template('ingresar.html')
            
        else:
            flash("Ese email ya esta registrado")
            return render_template('registrar.html', data=DATA)    
    else:
        return render_template('registrar.html', data=DATA)

    
@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token) #Regresa el email!
    except:
        flash('Algo salio mal. Por favor intenta de nuevo')
        return redirect(url_for('login'))#En caso de cuenta creada pero no confirmada
    user = ModelUser.consulta_email(db, email)
    if user!=None:
        if user.confirmed:
            flash('Account already confirmed. Please login.', 'success')
            return redirect(url_for('login'))
        else:
            ModelUser.confirm_user(db, email)
            return redirect(url_for('login'))#Pantalla de succes confirmation!
    else: #Codigo expiro
        flash('Tu codigo de verificacion es incorrecto o ha expirado')
        return redirect(url_for('login'))#En caso de cuenta creada pero no confirmada

@app.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    template = render_template('email.html', confirm_url=confirm_url)
    subject = "Por favor confirma tu cuenta"

    msg = Message(
                    subject,
                    recipients=['jairosotoy@gmail.com'],########Cambiar al correo de usuario
                    html=template,
                    sender="armando.samir.mtzi@gmail.com"
                )
    mail.send(msg)

    flash('Tu cuenta no esta confirmada, hemos enviado un nuevo correo de confirmación.')
    return redirect(url_for('login'))

@app.route('/confirmarCorreo')
def confirmarCorreo():
    DATA = {
        'title' : 'Confirmacion de correo',
        'stylesheet' : 'validacionCorreo.css',
    }
    return render_template('validacionCorreo.html', data=DATA)

@app.route('/verificacion')
@login_required
def verificacion():
    return render_template('verificacion.html')

#En caso de que no este logeado y quiera entrar al sistema redirige al login
def status_401(error):
    return redirect(url_for('login'))

#En caso de que el usuario acceda a una pagina no definida
def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


# This forces the app to start at '/'
if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run("0.0.0.0", port=5000)