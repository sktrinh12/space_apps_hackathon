from flaskext.mysql import MySQL

mysql=MySQL()

def create_connection(app):
    app.config['MYSQL_DATABASE_USER'] = 'sktrinh12'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'bon78952'
    app.config['MYSQL_DATABASE_DB'] = 'sktrinh12$chemitryuser'
    app.config['MYSQL_DATABASE_HOST'] = 'sktrinh12.mysql.pythonanywhere-services.com'
    mysql.init_app(app)
    conn = mysql.connect()
    cursor = conn.cursor()
    return cursor,conn