from main import app
from flask_mysqldb import MySQL
mysql = MySQL()
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'India@2021'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'bus_booking'

mysql.init_app(app)
