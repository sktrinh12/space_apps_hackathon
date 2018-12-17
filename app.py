from flask import Flask,flash,render_template,redirect,url_for,request,session,send_file,send_from_directory, jsonify
from dbconnect import create_connection
from wtforms import Form,BooleanField,StringField,PasswordField,TextAreaField,validators
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc
from functools import wraps
from content_mgmt import Content
from flask_mail import Mail, Message
import os

TOPIC_DICT = Content()
MAIL_USERNAME ='sktrinh12@gmail.com'
app = Flask(__name__,instance_path='/home/sktrinh12/ChemTools/protected')
app.config.update(
    #DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD='Trsp9228' )
app.secret_key = 'bon78952' #needs this or flash does not work
mail = Mail(app)

class RegistrationForm(Form):
    username = StringField('Username',[validators.Length(min=4,max=20)])
    email = StringField('Email Address',[validators.Length(min=6,max=50)])
    password = PasswordField('New Password',[validators.DataRequired(),validators.EqualTo('confirm',message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the <a href="/tos/">Terms of Service </a> and the <a href="/privacy/"> Privacy Notice </a> (Last updated 8-Dec-2018)',[validators.DataRequired()])

class SendEmailForm(Form):
    topic = TextAreaField('topic',[validators.Length(min=2,max=100)])
    body = TextAreaField('body',[validators.Length(max=500)])

@app.route('/')
def main():
    return redirect(url_for('dashboard'))

@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html",TOPIC_DICT=TOPIC_DICT)

@app.errorhandler(404)
def page_not_found(e):
    try:
        gc.collect()
        rule = request.path #grab url user attempted to visit
        if any(txtstr in rule for txtstr in ['feed','favicon','wp-content','wp-login','wp-logout']):
            pass
        else:
            errorlogging = open('/home/sktrinh12/ChemTools/static/fourohfour/404errorlogs.txt','a') #log url sites to this directory
            errorlogging.write((str(rule)+'\n'))
        #flash(str(rule))
        return render_template('404.html')
    except Exception as e:
        return(str(e))

@app.errorhandler(405)
def method_not_found(e):
    return render_template('405.html')

def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('You need to login first!')
            return redirect(url_for('login_page'))
    return wrap

@app.route('/blog/')
@login_required
def blog():
    try:
        replies = {'Susu' : 'Cool post',
                    'Chom' : '+1',
                    'Bon' : 'ku',
                    'python' : 'py-nice!'}
        return render_template('blog.html',replies=replies)
    except Exception as e:
        return(str(e))

@app.route('/logout/')
@login_required #can't click logout unless logged in
def logout():
    session.clear()
    flash('You have been logged out!')
    gc.collect()
    return redirect(url_for('dashboard'))

@app.route('/jinjaman/')
def jinjaman():
    try:
        gc.collect()
        data = [15, '15', 'Python is good','Python, Java, php, SQL, C++','<p><strong>Hey there!</strong></p>']
        return render_template('jinja-templating.html',data=data)
    except Exception as e:
        return(str(e))

@app.route('/converters/')
@app.route('/converters/<string:thread>/<int:page>/')
def converterexample(thread='test',page=1):
    try:
        gc.collect()
        return render_template("converterexample.html",thread=thread,page=page)
    except Exception as e:
        return(str(e))

@app.route('/login/', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        c, conn = create_connection(app)
        if request.method == "POST":
            data = c.execute('SELECT * FROM users WHERE username = (%s)', thwart(request.form['username']))
            data = c.fetchone()[2] #hash pwd of username [usrnm, email, pwd]

            if sha256_crypt.verify(request.form['password'],data): #returns boolean, equivalent starting data
                session['logged_in'] = True
                session['username'] = request.form['username']

                flash('you are now logged in!')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid credentials, try again'
        gc.collect()

        return render_template("login.html", error = error)

    except Exception as e:
        #flash(e)
        error = 'Invalid credentials, try again'
        return render_template('login.html',error = error)

@app.route('/register/', methods=['GET','POST'])
def register_page():
    try:
        form = RegistrationForm(request.form) #render the form
        if request.method =='POST' and form.validate(): #the user is making a post (clicking submit) & all the validators are checked
            username = form.username.data #textfield
            email = form.email.data
            password = sha256_crypt.encrypt(str(form.password.data)) #password hashing
            c, conn = create_connection(app)
            x = c.execute("SELECT * FROM users WHERE username = (%s)",(thwart(username),))
            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html',form=form)
            else:
                c.execute("INSERT INTO users (username,password,email) VALUES (%s,%s,%s)",
                            (thwart(username),thwart(password),thwart(email)))
                conn.commit()
                flash("Thanks for registering!")
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] =True
                session['username'] = username
                return redirect(url_for('dashboard'))
        return render_template("register.html",form=form)
    except Exception as e:
        return (str(e))

@app.route('/send-mail/', methods=['GET','POST'])
@login_required
def send_mail():
    error =''
    try:
        emailform = SendEmailForm(request.form)
        if request.method == 'POST' and emailform.validate():
            c, conn = create_connection(app)
            emailRecipt = c.execute('SELECT email FROM users WHERE username = (%s)', session['username'])
            emailRecipt = c.fetchone()[0]
            msg = Message(f"Mail sent from {request.base_url} - topic: {emailform.topic.data}!",
                            sender=MAIL_USERNAME,
                            recipients=[emailRecipt])
            msg.body = emailform.body.data
            msg.html = render_template('sendEmail.html', username=session['username'],emailRecipt=emailRecipt,baseurl=request.base_url)
            mail.send(msg)
            flash('Email Sent! :)')
        gc.collect()
        return render_template('sendEmailForm.html',form=emailform,error=error)

    except Exception as e:
        #flash(e)
        error='The minimum or maximum amount of characters for Topic/Body were not met'
        return render_template('sendEmailForm.html',error=error)

@app.route('/file-downloads/')
def file_downloads():
    try:
        return render_template('downloads.html')
    except Exception as e:
        return str(e)

@app.route('/return-file/')
def return_file():
    try:
        return send_file('/home/sktrinh12/ChemTools/static/images/Dopamine.png', attachment_filename='Dopamine.png')
    except Exception as e:
        return str(e)

def special_requirement(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        try:
            if 'sktrinh12' == session['username']:
                return f(*args,**kwargs)
            else:
                return redirect(url_for('dashboard'))
        except:
            flash('You do not have vision privledges!')
            return redirect(url_for('dashboard'))
    return wrap

@app.route('/protected/<path:filename>')
@special_requirement
def protected(filename):
    try:
        return send_from_directory(os.path.join(app.instance_path,''),filename)
    except:
        return redirect(url_for('main'))

@app.route('/_background_process/') #the underscore flags it as a background process only, not for user interface
def background_process():
    try:
        lang = request.args.get('proglang')
        if str(lang).lower() == 'python':
            return jsonify(result='You are wise!')
        else:
            return jsonify(result='Try again!')
    except Exception as e:
        return(str(e))

@app.route('/interactive/')
def interactive():
    try:
        return render_template('interactive.html')
    except Exception as e:
        return(str(e))

@app.route('/_bkgProcSmrtSrch/')
def bkgProcSmrtSrch():
    try:
        query = request.args.get('smrtsrch')
        if query:
            return jsonify(result='Good')
    except Exception as e:
        return(str(e))