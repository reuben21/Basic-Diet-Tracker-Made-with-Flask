from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import pymysql
from datetime import datetime
import time

try:
    host="localhost";user="root";dbname="diettracker"
    conn = pymysql.connect(host, user=user,port=3306,passwd="reuben", db=dbname)
    cursor=conn.cursor()
except Exception as e:
    print(e)
app = Flask(__name__)

app.config['MYSQL_USER'] = 'reuben21'
app.config['MYSQL_PASSWORD'] = 'reuben'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'diettracker'

mysql = MySQL(app)

# Important SQL Lines Below
# Basic Lines
# cur = mysql.connection.cursor()
# cur.execute('')
# mysql.connection.commit()


@app.route('/',methods=['GET', 'POST'])
def index():
	host="localhost";user="root";dbname="diettracker"
	conn = pymysql.connect(host, user=user,port=3306,passwd="reuben", db=dbname)
	if request.method == 'POST':

		date=request.form['date']
		# pytime=date.toPyDate()
		dt=datetime.strptime(date,'%Y-%m-%d')
		database_date=datetime.strftime(dt,"%Y-%m-%d")
		pretty_date=datetime.strftime(dt,'%B %d,%Y')
		
		args=(database_date)
		
		cursor=conn.cursor()
		cursor.execute("INSERT INTO diettracker.log_date (entry_date) VALUES (%s)",database_date)
		conn.commit()
		conn.close()
	conn1 = pymysql.connect(host, user=user,port=3306,passwd="reuben", db=dbname)
	cur=conn1.cursor()
	cur.execute("SELECT entry_date from log_date order by entry_date desc")
	result=cur.fetchall()
	conn1.commit()
	conn1.close()

	pretty_results=[]

	for i in result:
		single_date={}
		# d=datetime.strptime(,'%Y-%m-%d')
		print(i[0])
		single_date['entry_date']=datetime.strftime(i[0],'%B %d,%Y')
		pretty_results.append(single_date)
	print(pretty_results)
	return render_template('home.html',results=pretty_results)

@app.route('/view')
def view():
	return render_template('day.html')

@app.route('/food',methods=['GET', 'POST'])
def food():
	if request.method == 'POST':
		food_name=request.form['food-name']
		protein_no=request.form['protein']
		carbohydrates_no=request.form['carbohydrates']
		fat_no=request.form['fat']
		calories=(int(protein_no)*4)+(int(carbohydrates_no)*4)+(int(fat_no)*9)
		cur = mysql.connection.cursor()
		args=(str(food_name),protein_no,carbohydrates_no,fat_no,calories)
		print(args)
		cur.execute("INSERT INTO food (name,protein,carbohydrates,fat,calories) VALUES (%s,%s,%s,%s,%s)",args)
		mysql.connection.commit()

		
	cur1 = mysql.connection.cursor()
	cur1.execute("SELECT name,protein,carbohydrates,fat,calories from food")
	results=cur1.fetchall()
	
	mysql.connection.commit()
	return render_template('add_food.html',results=results)
if __name__=='__main__':
	app.run(debug=True)
